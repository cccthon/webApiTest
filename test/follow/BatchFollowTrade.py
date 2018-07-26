# -*- coding:utf-8 -*
import sys,yaml
import unittest,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
sys.path.append("../../test/follow")
import FMCommon,TradeOnline,Auth,Follow,Trade,Account,Order
from socketIO_client import SocketIO
import FollowOperation

userData = FMCommon.loadWebAPIYML()
order = FMCommon.loadOrderYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()
userDataFollow=FMCommon.loadFollowYML()
userDataAuth=FMCommon.loadAuthYML()
userDataTrade=FMCommon.loadTradeYML()
userDataAccount=FMCommon.loadAccountYML()

class BatchFollowTrade(unittest.TestCase):
    def setUp(self):
        '''跟随者登录'''
        #跟随者登录
        datas = {"account": 'testfollow@followme.com', "password": '123456', "remember": "false"}
        loginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(loginRes.status_code, userData['status_code_200'])
        self.token = json.loads(loginRes.text)['data']['token']

        # 交易员登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.traderToken = json.loads(traderLoginRes.text)['data']['token']
        self.traderUserId = json.loads(traderLoginRes.text)['data']['id']
        self.traderNickname = json.loads(traderLoginRes.text)['data']['nickname']

    def test_BatchFollowTrade(self):
        '''建立批量跟随->跟随下单->跟随平仓->查看跟随交易历史订单->取消跟随'''
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})
        self.traderHeaders = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.traderToken})
        # 创建200个跟随者跟随FMST005交易员，固定手数1.5手
        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=self.traderHeaders, brokerID=5)
        tradeAccountIndex = self.tradeAccountIndex[0]
        createfollowList =[]
        for i in range(2,3):
            follower =FollowOperation.Operation.createFollow(self.traderUserId, tradeAccountIndex, userData['headers'], i)
            createfollowList.append(follower)
            i = i
        print(i-1,"个跟随者：", createfollowList)

        #交易员切换账户
        Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'], self.traderHeaders,
                              tradeAccountIndex)

        # 获取交易员交易token
        traderTokenRes = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], self.traderHeaders)
        self.assertEqual(traderTokenRes.status_code, userData['status_code_200'])
        tradeToken = str(json.loads(traderTokenRes.content)["data"]["Token"]).replace("=", "@")

        # 交易员开仓
        openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                     userDataWebSocket['orderParam_symbol']: "EURCAD",
                     userDataWebSocket['orderParam_volume']: 1}
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(
            self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken}, openParam)
        FMCommon.printLog(openPositionRes)
        self.assertEqual(openPositionRes["code"], userDataWebSocket['ws_code_0'])
        self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
        self.assertEqual(openPositionRes["order"]["volume"], 1)
        self.orderID = openPositionRes["order"]["order_id"]
        self.login = openPositionRes["order"]["login"]

        # 交易员平仓
        closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_211'],
                      userDataWebSocket['orderParam_ticket']: self.orderID,
                      userDataWebSocket['orderParam_volume']: 1}
        closeOrderRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
                                                                userDataWebSocket['ws_port'],
                                                                {'token': "" + tradeToken}, closeOrder)
        FMCommon.printLog(closeOrderRes)
        self.assertEqual(closeOrderRes["code"], userDataWebSocket['ws_code_0'])
        self.assertEqual(closeOrderRes["rcmd"], userDataWebSocket['ws_code_211'])
        self.assertEqual(closeOrderRes['order']["order_id"], self.orderID)
        self.assertEqual(closeOrderRes["order"]["volume"], 1)

        # 查询交易员的历史订单
        time.sleep(5)
        params = {userData['orderStatus']: userData['orderStatus_close']}
        getOrders = Order.getOrders(userData['hostName'] + order['getOrders_url'], self.traderHeaders, params=params)
        self.assertEqual(getOrders.status_code, userData['status_code_200'])
        ordersIDList = Order.getOrdersID(getOrders)
        self.assertIn(self.orderID, ordersIDList)

        #  批量取消200个跟随者的跟随
        deletefollowList = []
        for j in range(2,3):
            follower = FollowOperation.Operation.deleteFollow(self.traderUserId, tradeAccountIndex, userData['headers'], j)
            deletefollowList.append(follower)
            j = j
        print("取消",j-1,"个跟随者：", deletefollowList)

        #  验证跟随者跟单成功
        sql = "SELECT count(1) from t_followorder where TraderAccount=" + str(self.login) + " and TraderTradeID=" + str(
            self.orderID)
        row = FollowOperation.Operation.operationCopytradingDB(sql)
        self.assertTrue(row['count(1)'] >= 1)

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.traderToken
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(BatchFollowTrade))
    unittest.TextTestRunner(verbosity=2).run(suite)