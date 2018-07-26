# -*- coding:utf-8 -*
import sys,yaml,time
import unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,TradeOnline,Auth,Follow,Account
from socketIO_client import SocketIO

userData = FMCommon.loadWebAPIYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()

userDataFollow=FMCommon.loadFollowYML()
userDataAuth=FMCommon.loadAuthYML()

class GetCustomers(unittest.TestCase):
    def setUp(self):
        # 跟随者登录
        datas = {"account": userData['wfollowAccount'], "password": userData['wfollowpasswd'], "remember": "false"}
        loginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(loginRes.status_code, userData['status_code_200'])
        self.token = json.loads(loginRes.text)['data']['token']
        self.followerUserId = json.loads(loginRes.text)['data']['id']

        # 交易员登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.traderToken = json.loads(traderLoginRes.text)['data']['token']
        self.traderUserId = json.loads(traderLoginRes.text)['data']['id']

    def test_GetCustomers(self):
        # '''登录->建立跟随->获取正在跟随->获取跟随者概要->取消跟随->获取历史跟随'''
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})
        self.traderHeaders = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.traderToken})

        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=self.traderHeaders, brokerID=5)

        # 获取跟随者的accountindex
        self.followerAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=5)

        # 新建一个跟随,固定手数跟随
        params = {"accountIndex": int(self.followerAccountIndex[0]), "strategy": "fixed", "setting": 1.5,
                  "direction": "positive"}
        getFollowsRes = Follow.createFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0], headers=userData['headers'], datas=params)
        self.assertEqual(getFollowsRes.status_code, userData['status_code_200'])

        # 获取正在跟随
        getFollowingRes = Follow.getFollowersnew(userData['hostName'] + userDataFollow["getFollowingFollowers"], self.traderHeaders)
        self.assertEqual(getFollowingRes.status_code, userData['status_code_200'])
        self.assertIn(str(self.followerUserId), str(json.loads(getFollowingRes.content)['data']['items']))

        #获取跟随者概要
        getFollowerSummaryRes =Follow.getFollowerSummarynew(userData['hostName'] + userDataFollow["getFollowerSummary"],
                                                            self.traderHeaders, printLogs=1)
        self.assertEqual(getFollowerSummaryRes.status_code, userData['status_code_200'])
        #至少有一个人跟随
        self.assertTrue(int(json.loads(getFollowerSummaryRes.content)["data"]["following"]["count"]) > 0)

        # 取消跟随
        cancelFollowRes = Follow.DeleteFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0] + "?accountIndex=" + self.followerAccountIndex[0],
            userData['headers'])
        self.assertEqual(cancelFollowRes.status_code, userData['status_code_200'])
        time.sleep(2)

        #获取历史跟随，存在此跟随者
        getHistoryFollowingRes = Follow.getFollowersnew(userData['hostName'] + userDataFollow["getHistoryFollowers"],
                                                        self.traderHeaders)
        self.assertEqual(getHistoryFollowingRes.status_code, userData['status_code_200'])
        self.assertIn(str(self.followerUserId), str(json.loads(getHistoryFollowingRes.content)['data']['items']))

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.traderToken
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(GetCustomers))
    unittest.TextTestRunner(verbosity=2).run(suite)







