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

class BatchOrders(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.token = json.loads(traderLoginRes.text)['data']['token']

    def test_BatchOrders(self):
        '''登录->切换到MT4账号->获取交易token->批量开仓>批量平仓->退出登录'''
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token

        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=5)

        # 切换到MT4账号
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 userData['headers'],self.tradeAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])

        # 获取交易token
        getTokenRes = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], userData['headers'])
        FMCommon.printLog('getTokenRes: ' + getTokenRes.text)
        self.assertEqual(getTokenRes.status_code, userData['status_code_200'])
        MT4Account = str(json.loads(getTokenRes.content)["data"]["MT4Account"])
        tradeToken = str(json.loads(getTokenRes.content)["data"]["Token"]).replace("=", "@")

        # 循环开仓
        openOrderList = []
        count = 0
        while count < 2:
            openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                         userDataWebSocket['orderParam_symbol']: "AUDCAD",
                         userDataWebSocket['orderParam_volume']: 1}
            openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken}, openParam)
            if (openPositionRes["code"] == userDataWebSocket['ws_code_0']):
                self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
                self.assertEqual(openPositionRes["order"]["volume"], 1)
                self.assertEqual(openPositionRes["order"]["symbol"], "AUDCAD")
                self.assertEqual(str(openPositionRes["order"]["login"]), MT4Account)
                self.orderID = openPositionRes["order"]["order_id"]
                openOrderList.append(self.orderID)
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
            count = count + 1

        time.sleep(2)

        # 循环平仓
        for i in openOrderList:
            closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_211'],
                          userDataWebSocket['orderParam_ticket']: i,
                          userDataWebSocket['orderParam_volume']: 1}
            closeOrderRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
                                                                    userDataWebSocket['ws_port'],
                                                                    {'token': "" + tradeToken}, closeOrder)
            self.assertEqual(closeOrderRes["code"], userDataWebSocket['ws_code_0'])
            self.assertEqual(closeOrderRes["rcmd"], userDataWebSocket['ws_code_211'])
            self.assertEqual(closeOrderRes['order']["order_id"], i)
            self.assertEqual(closeOrderRes["order"]["volume"], 1)
            self.assertEqual(str(openPositionRes["order"]["login"]), MT4Account)
            print(i)

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(BatchOrders))
    unittest.TextTestRunner(verbosity=2).run(suite)
