# -*- coding:utf-8 -*
import requests,json,gc,sys,yaml,time
import unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,TradeOnline,Auth,Trade,Account,Order
from socketIO_client import SocketIO

userData = FMCommon.loadWebAPIYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()

userDataFollow=FMCommon.loadFollowYML()
userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()
userDataTrade=FMCommon.loadTradeYML()
order = FMCommon.loadOrderYML()

class CheckFullStop(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.token = json.loads(traderLoginRes.text)['data']['token']

    def test_CheckFullStop(self):
        '''及时价开仓买入带止损止盈'''
        #sl返回时字符编码问题
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token

        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=5)
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
        tpspParamRes_sl = TradeOnline.OnlineTradeEvent_sl.tradeEvent_sl(self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'],{'token': "" + tradeToken})
        l = tpspParamRes_sl['AUDCAD']['l']
        a = tpspParamRes_sl['AUDCAD']['a']
        b = tpspParamRes_sl['AUDCAD']['b']

        # 止盈 止盈值>= bid价格 + stop_level
        setTP = round(b + l * 0.00001, 5)
        setSL = round(b - l * 0.00001, 5)
        print("setTP:", setTP)
        print("setTP:", setSL)

        # 开仓买入,现价带止损止盈
        openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                     userDataWebSocket['orderParam_symbol']: "AUDCAD",
                     userDataWebSocket['orderParam_volume']: 1,
                     userDataWebSocket['orderParam_cmd']: 0,
                     userDataWebSocket['orderParam_sl']: setSL,
                     userDataWebSocket['orderParam_tp']: setTP
                     }
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(
            self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'],{'token': "" + tradeToken}, openParam)
        if (openPositionRes["code"] == userDataWebSocket['ws_code_0']):
            self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
            self.assertEqual(openPositionRes["order"]["volume"], 1)
            self.assertEqual(openPositionRes["order"]["symbol"], "AUDCAD")
            self.orderID = openPositionRes["order"]["order_id"]
            self.price = openPositionRes["order"]["price"]
            self.tp = openPositionRes["order"]["tp"]
            self.sl = openPositionRes["order"]["sl"]
            self.assertNotEqual(0, self.tp, "止盈设置不成功")
            self.assertNotEqual(0, self.sl, "止损设置不成功")
        if (openPositionRes["code"] == 4):
            print("保证金不足！")
        if (openPositionRes["code"] == 10):
            print("市场关闭！")
        if (openPositionRes["code"] == 300):
            print("服务器内部错误！")
        if (openPositionRes["code"] == 3):
            print("客户不存在！")
        if (openPositionRes["code"] == 7):
            print("获取价格失败！")
        if (openPositionRes["code"] == 9):
            print("手数错误！")
        if (openPositionRes["code"] == 18):
            print("此品种不能交易！")
        if (openPositionRes["code"] == 8):
            print("止损止盈价格错误！")


    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(CheckFullStop))
    unittest.TextTestRunner(verbosity=2).run(suite)


