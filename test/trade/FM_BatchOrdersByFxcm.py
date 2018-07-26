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

class BatchOrdersByFxcm(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.token = json.loads(traderLoginRes.text)['data']['token']

    def test_BatchOrdersByFxcm(self):
        '''登录->切换到福汇账号->获取交易token->连续开仓>连续平仓->退出登录'''
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        # 获取交易员的accountindex
        self.tradeAccountIndex_fxcm = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=4)
        # 切换到MT4账号
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 userData['headers'],self.tradeAccountIndex_fxcm[0])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])

        # 获取交易token
        getTokenRes = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], userData['headers'])
        FMCommon.printLog('getTokenRes: ' + getTokenRes.text)
        self.assertEqual(getTokenRes.status_code, userData['status_code_200'])
        tradeToken = str(json.loads(getTokenRes.content)["data"]["Token"]).replace("=", "@")

        # 循环开仓
        openOrderList = []
        count = 0
        while count < 2:
            openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                         userDataWebSocket['orderParam_symbol']: "EUR/AUD",
                         userDataWebSocket['orderParam_volume']: 1000}
            openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken}, openParam)
            if (openPositionRes["code"] == userDataWebSocket['ws_code_0']):
                self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
                self.assertEqual(openPositionRes["order"]["volume"], 1000)
                self.assertEqual(openPositionRes["order"]["symbol"], "EUR/AUD")
                self.orderID = openPositionRes["order"]["order_id"]
                openOrderList.append(self.orderID)
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
            else:
                print("其它错误")
            count = count+1

        time.sleep(2)
        # 循环平仓
        for i in openOrderList:
            closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_211'],
                          userDataWebSocket['orderParam_ticket']: i,
                          userDataWebSocket['orderParam_volume']: 1000}
            closeOrderRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
                                                                    userDataWebSocket['ws_port'],
                                                                    {'token': "" + tradeToken}, closeOrder)
            self.assertEqual(closeOrderRes["code"], userDataWebSocket['ws_code_0'])
            self.assertEqual(closeOrderRes["rcmd"], userDataWebSocket['ws_code_211'])
            self.assertEqual(closeOrderRes['order']["order_id"], i)
            self.assertEqual(closeOrderRes["order"]["volume"], 1000)
            print(i)

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(BatchOrdersByFxcm))
    unittest.TextTestRunner(verbosity=2).run(suite)
