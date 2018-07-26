# -*- coding:utf-8 -*
import requests,json,gc,sys,yaml
import unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
sys.path.append("../../test/follow")
import FMCommon,TradeOnline,Auth,Follow,Account,Trade,time
import FollowOperation

userData = FMCommon.loadWebAPIYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()
userDataFollow=FMCommon.loadFollowYML()
userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()
userDataTrade=FMCommon.loadTradeYML()

class MultiAccountFollowsPico(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['wfollowAccount'], "password": userData['wfollowpasswd'], "remember": "false"}
        loginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(loginRes.status_code, userData['status_code_200'])
        self.token = json.loads(loginRes.text)['data']['token']

        # 交易员登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.traderToken = json.loads(traderLoginRes.text)['data']['token']
        self.traderUserId = json.loads(traderLoginRes.text)['data']['id']

    def test_MultiAccountFollowsPico(self):
        '''不同经纪商账户跟随，福汇、kvb同时跟随福汇交易员交易（开仓，平仓，查询历史订单）'''
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})
        self.traderHeaders = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.traderToken})

        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=self.traderHeaders, brokerID=4)

        # 获取福汇跟随者的accountindex
        self.followerAccountIndex_fxcm = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=4)

        # 获取kvb跟随者的accountindex
        self.followerAccountIndex_kvb = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=5)

        # 建立福汇账户跟随者跟随,固定手数跟随
        params = {"accountIndex": int(self.followerAccountIndex_fxcm[0]), "strategy": "fixed", "setting": 1.5,
                  "direction": "positive"}
        getFollowsRes = Follow.createFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0],
            headers=userData['headers'], datas=params)
        FMCommon.printLog('getFollowsRes: ' + getFollowsRes.text)
        self.assertEqual(getFollowsRes.status_code, userData['status_code_200'])

        # 建立kvb账户跟随者跟随,固定手数跟随
        params = {"accountIndex": int(self.followerAccountIndex_kvb[0]), "strategy": "fixed", "setting": 1.5,
                  "direction": "positive"}
        getFollowsRes = Follow.createFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0],
            headers=userData['headers'], datas=params)
        FMCommon.printLog('getFollowsRes: ' + getFollowsRes.text)
        self.assertEqual(getFollowsRes.status_code, userData['status_code_200'])

        # 交易员切换账户
        Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'], self.traderHeaders,
                              self.tradeAccountIndex[0])

        # 获取交易员交易token
        traderTokenRes = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], self.traderHeaders)
        self.assertEqual(traderTokenRes.status_code, userData['status_code_200'])
        tradeToken = str(json.loads(traderTokenRes.content)["data"]["Token"]).replace("=", "@")

        # 交易员开仓
        openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                     userDataWebSocket['orderParam_symbol']: "AUD/CAD",
                     userDataWebSocket['orderParam_volume']: 1000}
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(
            self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken}, openParam)
        FMCommon.printLog(openPositionRes)
        self.assertEqual(openPositionRes["code"], userDataWebSocket['ws_code_0'])
        self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
        self.assertEqual(openPositionRes["order"]["volume"], 1000)
        self.orderID = openPositionRes["order"]["order_id"]

        # 交易员平仓
        closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_211'],
                      userDataWebSocket['orderParam_ticket']: self.orderID,
                      userDataWebSocket['orderParam_volume']: 1000}
        closeOrderRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
                                                                userDataWebSocket['ws_port'],
                                                                {'token': "" + tradeToken}, closeOrder)
        FMCommon.printLog(closeOrderRes)
        self.assertEqual(closeOrderRes["code"], userDataWebSocket['ws_code_0'])
        self.assertEqual(closeOrderRes["rcmd"], userDataWebSocket['ws_code_211'])
        self.assertEqual(closeOrderRes['order']["order_id"], self.orderID)
        self.assertEqual(closeOrderRes["order"]["volume"], 1000)

        # 查询交易员的历史订单
        time.sleep(userDataWebSocket['waitTime'])
        historyOrdersRes = Trade.getOrders(userData['hostName'] + userDataTrade["getOrders"], self.traderHeaders,
                                           userData['orderStatus_close'])
        self.assertEqual(historyOrdersRes.status_code, userData['status_code_200'])
        self.assertIn(str(self.orderID), str(json.loads(historyOrdersRes.content)["data"]["items"]))
        FMCommon.printLog('historyOrdersRes: ' + historyOrdersRes.text)

        # 切换福汇账户
        Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'], userData['headers'],
                              self.followerAccountIndex_fxcm[0])

        # 获取跟随者交易token
        demotoken = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], userData['headers'])
        self.assertEqual(demotoken.status_code, userData['status_code_200'])
        fxcmAccount = str(json.loads(demotoken.content)["data"]["MT4Account"])

        #  验证跟随者跟单成功
        sql = "SELECT TradeID from t_followorder where Account=" + fxcmAccount + " and TraderTradeID=" + str(
            self.orderID)
        row = FollowOperation.Operation.operationCopytradingDB(sql)

        # 查询跟随者的历史订单
        followerHistoryOrdersRes = Trade.getOrders(userData['hostName'] + userDataTrade["getOrders"],
                                                   userData['headers'],
                                                   userData['orderStatus_close'])
        self.assertEqual(followerHistoryOrdersRes.status_code, userData['status_code_200'])
        self.assertIn(str(row['TradeID']), str(json.loads(followerHistoryOrdersRes.content)["data"]["items"]))

        # 切换kvb账户
        Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'], userData['headers'],
                              self.followerAccountIndex_kvb[0])

        # 获取跟随者交易token
        demotoken = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], userData['headers'])
        self.assertEqual(demotoken.status_code, userData['status_code_200'])
        kvbAccount = str(json.loads(demotoken.content)["data"]["MT4Account"])

        #  验证跟随者跟单成功
        sql = "SELECT TradeID from t_followorder where Account=" + kvbAccount + " and TraderTradeID=" + str(
            self.orderID)
        row = FollowOperation.Operation.operationCopytradingDB(sql)

        # 查询跟随者的历史订单
        followerHistoryOrdersRes = Trade.getOrders(userData['hostName'] + userDataTrade["getOrders"],
                                                   userData['headers'],
                                                   userData['orderStatus_close'])
        self.assertEqual(followerHistoryOrdersRes.status_code, userData['status_code_200'])
        self.assertIn(str(row['TradeID']), str(json.loads(followerHistoryOrdersRes.content)["data"]["items"]))

        # 取消跟随
        cancelFollowRes = Follow.DeleteFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0] + "?accountIndex=" + self.followerAccountIndex_fxcm[0],
            userData['headers'])
        FMCommon.printLog('cancelFollowRes: ' + cancelFollowRes.text)
        self.assertEqual(cancelFollowRes.status_code, userData['status_code_200'])

        cancelFollowRes = Follow.DeleteFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0] + "?accountIndex=" + self.followerAccountIndex_kvb[0],
            userData['headers'])
        FMCommon.printLog('cancelFollowRes: ' + cancelFollowRes.text)
        self.assertEqual(cancelFollowRes.status_code, userData['status_code_200'])

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(MultiAccountFollowsPico))
    unittest.TextTestRunner(verbosity=2).run(suite)
