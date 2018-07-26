# -*- coding:utf-8 -*
import requests,json,gc,sys,yaml,time
import unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,TradeOnline,Auth,Account,Trade
from socketIO_client import SocketIO

userData = FMCommon.loadWebAPIYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()
userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()
userDataSocial=FMCommon.loadSocialYML()

class DeletePending(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        loginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(loginRes.status_code, userData['status_code_200'])
        self.token = json.loads(loginRes.text)['data']['token']

    def test_DeletePending(self):
        '''登录->切换到MT4账号->获取交易token->新建一个挂单->删除挂单->退出登录'''
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        # 获取accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=5)
        # 切换到MT4账号
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 userData['headers'], self.tradeAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])

        # 获取交易token
        getTokenRes = requests.get(userData['hostName'] + userDataAccount["getToken_url"], headers=userData['headers'], data="")
        FMCommon.printLog('getTokenRes: ' + getTokenRes.text)
        self.assertEqual(getTokenRes.status_code, userData['status_code_200'])
        tradeToken = str(json.loads(getTokenRes.content)["data"]["Token"]).replace("=", "@")

        # 开仓获取开仓价格
        openParam = {userDataWebSocket['orderParam_cmd']: userDataWebSocket['order_cmd'],
                     userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                     userDataWebSocket['orderParam_symbol']: "AUDCAD",
                     userDataWebSocket['orderParam_volume']: 1}
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken}, openParam)
        if(openPositionRes["code"]==userDataWebSocket['ws_code_0']):
            self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
            self.orderID = openPositionRes["order"]["order_id"]
            self.price = openPositionRes["order"]["price"]
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

        # 订单止损止盈 取audcad的l,a,b
        tpspParamRes_sl = TradeOnline.OnlineTradeEvent_sl.tradeEvent_sl(self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'],{'token': "" + tradeToken})
        l = tpspParamRes_sl['AUDCAD']['l']
        # 买价
        a = tpspParamRes_sl['AUDCAD']['a']
        # 卖价
        b = tpspParamRes_sl['AUDCAD']['b']

        # 委托价格
        pendPrice = round(self.price - 0.001, 5)
        # 止盈 止盈值>= bid价格 + stop_level
        setTP = round(pendPrice + l * 0.00001, 5)
        # 止损 止损值>= bid价格 - stop_level
        setSL = round(pendPrice - l * 0.00001, 5)
        print("setTP:", setTP)
        print("setSL:", setSL)

        # 建立挂单（买），设置止损止盈
        createPendParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_213'],
                           userDataWebSocket['pendingParam_price']: pendPrice,
                           userDataWebSocket['orderParam_symbol']: "AUDCAD",
                           userDataWebSocket['pendingParam_volume']: 1,
                           userDataWebSocket['orderParam_sl']: setSL,
                           userDataWebSocket['orderParam_tp']: setTP
                           }
        createPendingRes = TradeOnline.OnlineTradeEvent.tradeEvent(
            self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken},createPendParam)
        if(createPendingRes["code"]==userDataWebSocket['ws_code_0']):
            self.assertEqual(createPendingRes["rcmd"], userDataWebSocket['ws_code_213'])
            self.assertEqual(createPendingRes["order"]["symbol"], "AUDCAD")
            self.assertEqual(createPendingRes["order"]["volume"], 1)
            self.assertNotEqual(0, createPendingRes["order"]["tp"], "止盈设置不成功")
            self.assertNotEqual(0, createPendingRes["order"]["sl"], "止损设置不成功")
            self.pendOrder = createPendingRes["order"]["order_id"]
        if (createPendingRes["code"] == 8):
            print("")

        time.sleep(2)
        # 删除挂单
        deletePendParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_214'],
                           userDataWebSocket['orderParam_ticket']: self.pendOrder}
        deletePendRes = TradeOnline.OnlineTradeEvent.tradeEvent(
            self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken},deletePendParam)
        self.assertEqual(deletePendRes["code"], userDataWebSocket['ws_code_0'])
        self.assertEqual(deletePendRes["rcmd"], userDataWebSocket['ws_code_214'])
        self.assertEqual(deletePendRes["order"]["order_id"], self.pendOrder)

        time.sleep(2)
        # 平仓
        closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_211'],
                      userDataWebSocket['orderParam_ticket']: self.orderID,
                      userDataWebSocket['orderParam_volume']: 1}
        closeOrderRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
                                                                userDataWebSocket['ws_port'],
                                                                {'token': "" + tradeToken}, closeOrder)
        if(closeOrderRes["code"]==userDataWebSocket['ws_code_0']):
            self.assertEqual(closeOrderRes["rcmd"], userDataWebSocket['ws_code_211'])
            self.assertEqual(closeOrderRes['order']["order_id"], self.orderID)
            self.assertEqual(closeOrderRes["order"]["volume"], 1)
        if(closeOrderRes["code"]==13):
            print("订单不存在!")

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(DeletePending))
    unittest.TextTestRunner(verbosity=2).run(suite)


