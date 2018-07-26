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
orderData = FMCommon.loadOrderYML()

class DeleteOrders(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.token = json.loads(traderLoginRes.text)['data']['token']

    def test_DeleteOrders(self):
        '''登录->切换到MT4账号->获取交易token->检查持仓单列表是否有单，如果有单批量平仓>退出登录'''
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

        '''获取当前用户的所有交易订单，并平掉'''
        params = {userData['orderStatus']: userData['orderStatus_open'], "view": "TRADER"}
        getOrders = Order.getOrders(userData['hostName'] + orderData['getOrders_url'], userData['headers'],
                                    params=params)
        # 获取订单成功，返回200 ok
        self.assertEqual(getOrders.status_code, userData['status_code_200'])
        ordersIDList = Order.getOrdersID(getOrders)
        print("ordersIDList:", ordersIDList)

        time.sleep(2)
        # 平掉当前用户所有订单,如果有
        # #web sockets批量平仓
        closeParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_219'],
                      userDataWebSocket['orderParam_tickets']: ordersIDList}
        closePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
                                                                   userDataWebSocket['ws_port'],
                                                                   {'token': tradeToken}, closeParam)
        if(closePositionRes["code"]==userDataWebSocket['ws_code_0']):
            # 校验code等于0，为及时单平仓成功
            # 校验rcmd等于210，为及时单开仓
            self.assertEqual(closePositionRes["rcmd"], userDataWebSocket['ws_code_219'])
            # 校验平掉的单号，为本测试及时单开仓的单号
            self.assertEqual(closePositionRes['success_tickets'], ordersIDList)
        if (closePositionRes["code"] == 13):
            print("订单不存在!")

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(DeleteOrders))
    unittest.TextTestRunner(verbosity=2).run(suite)
