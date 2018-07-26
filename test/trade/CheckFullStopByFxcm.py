# -*- coding:utf-8 -*
import requests,json,gc,sys,yaml,time
import unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,TradeOnline,Auth,Trade,Account
from socketIO_client import SocketIO

userData = FMCommon.loadWebAPIYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()

userDataFollow=FMCommon.loadFollowYML()
userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()
userDataTrade=FMCommon.loadTradeYML()

class CheckFullStopByFxcm(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.token = json.loads(traderLoginRes.text)['data']['token']

    def test_CheckFullStopByFxcm(self):
        '''登录->切换到福汇账户->获取交易token->开仓>订单止损止盈->查看持仓订单->退出登录'''
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        
        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=4)
        
        # 切换到MT4账号
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 userData['headers'], self.tradeAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])

        # 获取交易token
        getTokenRes = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], userData['headers'])
        FMCommon.printLog('getTokenRes: ' + getTokenRes.text)
        self.assertEqual(getTokenRes.status_code, userData['status_code_200'])
        tradeToken = str(json.loads(getTokenRes.content)["data"]["Token"]).replace("=", "@")

        # 订单止损止盈 取audcad的l,a,b
        tpspParamRes_sl = TradeOnline.OnlineTradeEvent_sl.tradeEvent_sl(self, userDataWebSocket['ws_host'],
                                                                        userDataWebSocket['ws_port'],
                                                                        {'token': "" + tradeToken})
        l = tpspParamRes_sl['AUD/CAD']['l']
        a = tpspParamRes_sl['AUD/CAD']['a']
        b = tpspParamRes_sl['AUD/CAD']['b']
        print(a)
        print(b)
        # 止损 < 当前bid价格
        setSL = round(b - 0.0005,5)
        # 止盈 > 当前bid价格
        setTP = round(b + 0.0005,5)
        # 开仓买入,现价带止损止盈
        openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                     userDataWebSocket['orderParam_symbol']: "AUD/CAD",
                     userDataWebSocket['orderParam_volume']: 1000,
                     userDataWebSocket['orderParam_cmd']: 0,
                     userDataWebSocket['orderParam_sl']: setSL,
                     userDataWebSocket['orderParam_tp']: setTP
                     }
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken}, openParam)
        if (openPositionRes["code"] == 0):
            self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
            self.assertEqual(openPositionRes["order"]["volume"], 1000)
            self.assertEqual(openPositionRes["order"]["symbol"], "AUD/CAD")
            self.orderID = openPositionRes["order"]["order_id"]
            self.price = openPositionRes["order"]["price"]
            self.tp = openPositionRes["order"]["tp"]
            self.sl = openPositionRes["order"]["sl"]
            self.assertNotEqual(0, self.tp, "止盈设置不成功")
            self.assertNotEqual(0, self.sl, "止损设置不成功")
        elif (openPositionRes["code"] == 4):
            print("保证金不足！")
        elif (openPositionRes["code"] == 10):
            print("市场关闭！")
        elif (openPositionRes["code"] == 300):
            print("服务器内部错误！")
        elif (openPositionRes["code"] == 3):
            print("客户不存在！")
        elif (openPositionRes["code"] == 7):
            print("获取价格失败！")
        elif (openPositionRes["code"] == 9):
            print("手数错误！")
        elif (openPositionRes["code"] == 18):
            print("此品种不能交易！")
        elif (openPositionRes["code"] == 8):
            print("止损止盈价格错误！")
        else:
            print("其它错误")

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(CheckFullStopByFxcm))
    unittest.TextTestRunner(verbosity=2).run(suite)


