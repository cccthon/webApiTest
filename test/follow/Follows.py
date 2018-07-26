# -*- coding:utf-8 -*
import requests,json,gc,sys,yaml
import unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
sys.path.append("../../test/follow")
import FMCommon,TradeOnline,Auth,Follow,Account,Trade

userData = FMCommon.loadWebAPIYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()
userDataFollow=FMCommon.loadFollowYML()
userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()

class Follows(unittest.TestCase):
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

    def test_Follows(self):
        '''登录->新建一个跟随->获取指定交易员存在的跟随关系->修改一个跟随->取消跟随'''
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})
        self.traderHeaders = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.traderToken})

        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=self.traderHeaders, brokerID=5)
        
        # 获取跟随者的accountindex
        self.followerAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=5)

        # 新建一个跟随,固定手数跟随
        params = {"accountIndex": int(self.followerAccountIndex[0]), "strategy": "fixed", "setting": 1.5, "direction": "positive"}
        getFollowsRes = Follow.createFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_"+self.tradeAccountIndex[0],
            headers=userData['headers'],datas=params)
        FMCommon.printLog('getFollowsRes: ' + getFollowsRes.text)
        self.assertEqual(getFollowsRes.status_code, userData['status_code_200'])

        # 跟随者切换账户
        Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'], userData['headers'],
                              self.followerAccountIndex[0])

        # 获取跟随者交易token
        demotoken = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], userData['headers'])
        self.assertEqual(demotoken.status_code, userData['status_code_200'])
        followerMT4Account = str(json.loads(demotoken.content)["data"]["MT4Account"])


        # 获取指定交易员存在的跟随关系
        getTraderFollowRes = Follow.getFollow(userData['hostName'] + userDataFollow["Follow_Url"],
                                              str(self.traderUserId) + "_"+self.tradeAccountIndex[0],
                                              self.followerAccountIndex[0], userData['headers'])
        FMCommon.printLog('getTraderFollowRes: ' + getTraderFollowRes.text)
        self.assertEqual(getTraderFollowRes.status_code, userData['status_code_200'])
        FollowAccount = json.loads(getTraderFollowRes.text)['data']['follow']['FollowAccount']
        self.assertEqual(FollowAccount, followerMT4Account, "没有包含此跟随者")

        # 修改一个跟随(修改跟随策略)
        params = {"accountIndex": int(self.followerAccountIndex[0]), "strategy": "ratio","setting": 2,"direction": "positive"}
        updateFollowRes = Follow.updateFollow(
            userData['hostName'] + userDataFollow["Follow_Url"]+str(self.traderUserId)+"_"
            +self.tradeAccountIndex[0] , userData['headers'], datas=params)
        FMCommon.printLog('updateFollowRes: ' + updateFollowRes.text)
        self.assertEqual(updateFollowRes.status_code, userData['status_code_200'])

        # 取消跟随
        cancelFollowRes = Follow.DeleteFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0] + "?accountIndex=" + self.followerAccountIndex[0],
            userData['headers'])
        FMCommon.printLog('cancelFollowRes: ' + cancelFollowRes.text)
        self.assertEqual(cancelFollowRes.status_code, userData['status_code_200'])


    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(Follows))
    unittest.TextTestRunner(verbosity=2).run(suite)
