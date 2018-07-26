# -*- coding:utf-8 -*
import sys,yaml
import unittest,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,TradeOnline,Auth,Follow,Account
from socketIO_client import SocketIO

userData = FMCommon.loadWebAPIYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()
userDataFollow=FMCommon.loadFollowYML()
userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()

class GetFollows(unittest.TestCase):
    def setUp(self):
        #登录
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


    def test_GetFollows(self):
        '''登录->建立跟随->获取当前跟随者账号的跟随概要'''
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})
        self.traderHeaders = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.traderToken})

        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=self.traderHeaders, brokerID=5)
        
        # 获取跟随者的accountindex
        self.followerAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=5)

        # 跟随者切换账户
        Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'], userData['headers'],
                              self.followerAccountIndex[0])

        # 新建一个跟随,固定手数跟随
        params = {"accountIndex": int(self.followerAccountIndex[0]), "strategy": "fixed", "setting": 1.5,
                  "direction": "positive"}
        getFollowsRes = Follow.createFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0], headers=userData['headers'], datas=params)
        self.assertEqual(getFollowsRes.status_code, userData['status_code_200'])

        #获取当前跟随者账号的跟随概要
        getFollowSummary =Follow.getFollowSummarynew(userData['hostName'] + userDataFollow['getFollowSummary'],userData['headers'])
        print("getFollowSummary:",getFollowSummary.content)
        self.assertEqual(getFollowSummary.status_code, userData['status_code_200'])
        #验证正在跟随人数大于0
        self.assertTrue(json.loads(getFollowSummary.content)['data']['following'] >= 1)
        #验证累计跟随手数
        self.assertTrue(json.loads(getFollowSummary.content)['data']['FollowStandardlots'] > 0)

        # 取消跟随
        cancelFollowRes = Follow.DeleteFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0] + "?accountIndex=" + self.followerAccountIndex[0],
            userData['headers'])
        FMCommon.printLog('cancelFollowRes: ' + cancelFollowRes.text)
        self.assertEqual(cancelFollowRes.status_code, userData['status_code_200'])


    def tearDown(self):
        #退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(GetFollows))
    unittest.TextTestRunner(verbosity=2).run(suite)