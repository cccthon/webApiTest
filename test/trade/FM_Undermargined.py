# -*- coding:utf-8 -*
import sys,yaml,time
import unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,TradeOnline,Auth,Trade,Account,Order
from socketIO_client import SocketIO

userData = FMCommon.loadWebAPIYML()
order = FMCommon.loadOrderYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()

userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()

userDataSocial=FMCommon.loadSocialYML()
class undermargined(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.token = json.loads(traderLoginRes.text)['data']['token']

    def test_undermargined(self):
        '''保证金不足'''
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})

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
        tradeToken = str(json.loads(getTokenRes.content)["data"]["Token"]).replace("=", "@")
        print("tradeToken:", tradeToken)

        # 开仓
        openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                     userDataWebSocket['orderParam_symbol']: "AUDCAD",
                     userDataWebSocket['orderParam_volume']: 1}
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(
            self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken}, openParam)
        if(openPositionRes["code"]==userDataWebSocket['ws_code_0']):
            self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
            self.assertEqual(openPositionRes["order"]["volume"], 1)
            self.orderID = openPositionRes["order"]["order_id"]
            # 获取当前用户的交易订单
            params = {userData['orderStatus']: userData['orderStatus_open']}
            getOrders = Order.getOrders(userData['hostName'] + order['getOrders_url'], userData['headers'],
                                        params=params)
            self.assertEqual(getOrders.status_code, userData['status_code_200'])
            ordersIDList = Order.getOrdersID(getOrders)
            self.assertIn(self.orderID, ordersIDList)

            time.sleep(2)
            # 平仓
            closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_211'],
                          userDataWebSocket['orderParam_ticket']: self.orderID,
                          userDataWebSocket['orderParam_volume']: 1}
            closeOrderRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
                                                                    userDataWebSocket['ws_port'],
                                                                    {'token': "" + tradeToken}, closeOrder)
            self.assertEqual(closeOrderRes["code"], userDataWebSocket['ws_code_0'])
            self.assertEqual(closeOrderRes["rcmd"], userDataWebSocket['ws_code_211'])
            self.assertEqual(closeOrderRes['order']["order_id"], self.orderID)
            self.assertEqual(closeOrderRes["order"]["volume"], 1)
        if(openPositionRes["code"]==4):
            print("保证金不足！")
        if(openPositionRes["code"] == 10):
            print("市场关闭！")

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.makeSuite(undermargined)
    unittest.TextTestRunner(verbosity=2).run(suite)


