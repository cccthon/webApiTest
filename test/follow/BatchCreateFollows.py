import unittest,sys

sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
sys.path.append("../../test/follow")
import FMCommon,Auth,json,Account,Follow

userData = FMCommon.loadWebAPIYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()
userDataFollow=FMCommon.loadFollowYML()
userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()
userDataTrade=FMCommon.loadTradeYML()

class BatchCreateFollows(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['followAccount2'], "password": userData['folllowPasswd2'], "remember": "false"}
        loginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(loginRes.status_code, userData['status_code_200'])
        self.token = json.loads(loginRes.text)['data']['token']

        # 交易员登录
        datas = {"account": userData['accoount2'], "password": userData['passwd2'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.traderToken = json.loads(traderLoginRes.text)['data']['token']
        self.traderUserId = json.loads(traderLoginRes.text)['data']['id']

    '''交易员、跟随者登陆->'''
    def test_CreateFollow_001(self):
        '''不同经纪商账户跟随，福汇、kvb同时跟随kvbmini交易员交易（开仓，平仓，查询历史订单）'''
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})
        self.traderHeaders = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.traderToken})

        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=self.traderHeaders, brokerID=6)

        print(self.tradeAccountIndex)

        # 获取福汇跟随者的accountindex
        self.followerAccountIndex_fxcm = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=4)

        # 获取kvb跟随者的accountindex
        self.followerAccountIndex_kvb = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=5)

        # 获取模拟账户的accountindex
        self.followerAccountIndex_demo=Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=3, accountType=0)

        # 获取Fxpro跟随者的accountindex
        self.followerAccountIndex_Fxpro=Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=7)

        # 建立福汇账户跟随者跟随,固定手数跟随
        params = {"accountIndex": int(self.followerAccountIndex_fxcm[0]), "strategy": "ratio", "setting": 1,
                  "direction": "positive"}
        getFollowsRes = Follow.createFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0],
            headers=userData['headers'], datas=params)
        FMCommon.printLog('getFollowsRes: ' + getFollowsRes.text)
        self.assertEqual(getFollowsRes.status_code, userData['status_code_200'])

        # 建立kvb账户跟随者跟随,固定手数跟随
        params = {"accountIndex": int(self.followerAccountIndex_kvb[0]), "strategy": "fixed", "setting": 0.02,
                  "direction": "positive"}
        getFollowsRes = Follow.createFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0],
            headers=userData['headers'], datas=params)
        FMCommon.printLog('getFollowsRes: ' + getFollowsRes.text)
        self.assertEqual(getFollowsRes.status_code, userData['status_code_200'])

        # #建立模拟账户跟随，按比例1倍跟随
        print('demo: ',self.followerAccountIndex_demo)
        params = {"accountIndex": int(self.followerAccountIndex_demo[0]), "strategy": "ratio", "setting": 1,
                  "direction": "positive"}
        getFollowsRes = Follow.createFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0],
            headers=userData['headers'], datas=params)
        FMCommon.printLog('getFollowsRes: ' + getFollowsRes.text)
        self.assertEqual(getFollowsRes.status_code, userData['status_code_200'])

        # 建立FxPro跟随者跟随，按比例1.5倍
        params = {"accountIndex": int(self.followerAccountIndex_Fxpro[0]), "strategy": "ratio", "setting": 1.5,
                  "direction": "positive"}
        getFollowsRes = Follow.createFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
            self.tradeAccountIndex[0],
            headers=userData['headers'], datas=params)
        FMCommon.printLog('getFollowsRes: ' + getFollowsRes.text)
        self.assertEqual(getFollowsRes.status_code, userData['status_code_200'])

        #
        # # 取消跟随pico
        # cancelPicoFollowRes = Follow.DeleteFollow(
        #     userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
        #     self.tradeAccountIndex[0] + "?accountIndex=" + self.followerAccountIndex_pico[0],
        #     userData['headers'])
        # FMCommon.printLog('cancelFollowRes: ' + cancelPicoFollowRes.text)
        #
        # self.assertEqual(cancelPicoFollowRes.status_code, userData['status_code_200'])
        #
        # # 取消跟随
        # cancelFxcmFollowRes = Follow.DeleteFollow(
        #     userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
        #     self.tradeAccountIndex[0] + "?accountIndex=" + self.followerAccountIndex_fxcm[0],
        #     userData['headers'])
        # FMCommon.printLog('cancelFxcmFollowRes: ' + cancelFxcmFollowRes.text)
        # self.assertEqual(cancelFxcmFollowRes.status_code, userData['status_code_200'])
        #
        # # 取消跟随
        # cancelKVBFollowRes = Follow.DeleteFollow(
        #     userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
        #     self.tradeAccountIndex[0] + "?accountIndex=" + self.followerAccountIndex_kvb[0],
        #     userData['headers'])
        # FMCommon.printLog('cancelFxcmFollowRes: ' + cancelKVBFollowRes.text)
        # self.assertEqual(cancelKVBFollowRes.status_code, userData['status_code_200'])
        #
        # # 取消跟随
        # cancelDemoFollowRes = Follow.DeleteFollow(
        #     userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
        #     self.tradeAccountIndex[0] + "?accountIndex=" + self.followerAccountIndex_demo[0],
        #     userData['headers'])
        # FMCommon.printLog('cancelDemoFollowRes: ' + cancelDemoFollowRes.text)
        # self.assertEqual(cancelDemoFollowRes.status_code, userData['status_code_200'])
        #
        # # 取消跟随
        # cancelFxproFollowRes = Follow.DeleteFollow(
        #     userData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" +
        #     self.tradeAccountIndex[0] + "?accountIndex=" + self.followerAccountIndex_Fxpro[0],
        #     userData['headers'])
        # FMCommon.printLog('cancelFxproFollowRes: ' + cancelFxproFollowRes.text)
        # self.assertEqual(cancelFxproFollowRes.status_code, userData['status_code_200'])

    def tearDown(self):
         # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()