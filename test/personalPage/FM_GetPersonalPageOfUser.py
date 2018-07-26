import sys, unittest,json
import sys, unittest,json
sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import Auth,FMCommon,Follow,PersonalPage,Account

userData = FMCommon.loadWebAPIYML()
userDataAccountUrl=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()
userDataFollUrl=FMCommon.loadFollowYML()
userDataPersonalPageUrl=FMCommon.loadPersonalPageYML()

class GetTradeInfoOfTrader(unittest.TestCase):
    def setUp(self):
        #交易员登陆---------------------
        tradeDatas = {"account":userData['account'], "password":userData['passwd'], "remember":"false"}
        tradeSignin = Auth.signin(userData['hostName'] + userDataAuthUrl['signin_url'], userData['headers'], tradeDatas)
        #登录成功，返回200 ok
        self.assertEqual(tradeSignin.status_code, userData['status_code_200'])
        #保存账号的nickName,待获取userID使用
        self.tradeNickName = json.loads(tradeSignin.text)['data']['nickname']
        # #保存登录时的token，待登出使用
        self.tradeUserToken = json.loads(tradeSignin.text)['data']['token']
        #保存userID
        self.tradeUserID = str(json.loads(tradeSignin.text)['data']['id'])
        #规整headers
        self.tradeHeaders = dict(userData['headers'], **{userData['Authorization'] : userData['Bearer'] + self.tradeUserToken})

    def test_GetFollowersOfTrader_001(self):
        '''获取交易员账号的跟随者列表（个人展示页）'''
        #AccountIndex为空，自动切换当前账户
        # #GET 请求 api/v2/trade/traders/:account/followers
        #返回code=SUCCESS
    
        url=userData['hostName']+userDataPersonalPageUrl['getFollowersOfTrader_url1']+self.tradeUserID\
            +userDataPersonalPageUrl['getFollowersOfTrader_url2']
        res=PersonalPage.getFollowersOfTrader(url,headers=userData['headers'])
        # print('Url: '+ url)
        FMCommon.printLog(res.text)
        #请求成功 返回200 ok
        self.assertEqual(res.status_code, userData['status_code_200'])

    def test_GetFollowersOfTrader_002(self):
        '''获取交易员账号的跟随者列表（个人展示页）'''
        url=userData['hostName']+userDataPersonalPageUrl['getFollowersOfTrader_url1']+self.tradeUserID+'_'+userData['pgAccountIndex']+userDataPersonalPageUrl['getFollowersOfTrader_url2']
        res=PersonalPage.getFollowersOfTrader(url,headers=userData['headers'],isFollowing=userData['isFollowing'])
        # print('Url: ' + url)
        FMCommon.printLog(res.text)
        #请求成功 返回 200
        self.assertEqual(res.status_code,userData['status_code_200'])

        # print('FollowTotal: '+str(self.followTotal))

    def test_GetFollowersOfTrader_003(self):
        #获取交易员账号的跟随者列表（个人展示页）正在跟随
        url=userData['hostName']+userDataPersonalPageUrl['getFollowersOfTrader_url1']+self.tradeUserID+'_'+userData['pgAccountIndex']+userDataPersonalPageUrl['getFollowersOfTrader_url2']
        res=PersonalPage.getFollowersOfTrader(url,headers=userData['headers'],isFollowing=userData['isFollowingFalse'])

        # print('Url: ' + url)

        FMCommon.printLog(res.text)

        #请求成功 返回 200
        self.assertEqual(res.status_code,userData['status_code_200'])

    def test_GetFollowersOfTrader_004(self):
        #获取交易员账号的跟随者列表（个人展示页）
        url=userData['hostName']+userDataPersonalPageUrl['getFollowersOfTrader_url1']+self.tradeUserID+'_'+userData['pgAccountIndex']+userDataPersonalPageUrl['getFollowersOfTrader_url2']
        res=PersonalPage.getFollowersOfTrader(url,headers=userData['headers'])

        #print('Url: ' + url)

        FMCommon.printLog(res.text)

        #请求成功 返回 200
        self.assertEqual(res.status_code,userData['status_code_200'])


    # def test_GetGraphicsOfTrader_005(self):
    #     #获取交易账号的交易图表统计数据
    #     #api/v2/trade/traders/:account/graphics
    #     url=userData['hostName']+userDataPersonalPageUrl['getGraphicsOfTrader_url1']+self.tradeUserID+'_'+userData['pgAccountIndex']+userDataPersonalPageUrl['getGraphicsOfTrader_url2']
    #     res=PersonalPage.getGraphicsOfTrader(url,headers=userData['headers'])
    #
    #     # print('Url: '+url)
    #
    #     FMCommon.printLog(res.text)
    #
    #     #请求成功 返回 200
    #     self.assertEqual(res.status_code,userData['status_code_200'])

    def test_GetOrdersOfUserAccount_006(self):
        #获取某用户交易账号的订单（个人展示页）
        #api/v2/trade/accounts/:account/orders
        url=userData['hostName']+userDataPersonalPageUrl['getOrdersOfUserAccount_url1']+self.tradeUserID+'_'+userData['pgAccountIndex']+userDataPersonalPageUrl['getOrdersOfUserAccount_url2']
        res=PersonalPage.getGraphicsOfTrader(url,headers=userData['headers'])

        # print('Url: '+url)
        FMCommon.printLog(res.text)

        #请求成功 返回 200
        self.assertEqual(res.status_code,userData['status_code_200'])

    # def test_GetStatisticsOfTrader_007(self):
    #
    #     #获取交易员账号的交易统计数据
    #     #api/v2/trade/traders/:account/statistics
    #     url=userData['hostName']+userDataPersonalPageUrl['getStatisticsOfTrader_url1']+self.tradeUserID+'_'+userData['pgAccountIndex']+userDataPersonalPageUrl['getStatisticsOfTrader_url2']
    #     res=PersonalPage.getStatisticsOfTrader(url,headers=userData['headers'])
    #
    #     # print('Url: '+url)
    #     FMCommon.printLog(res.text)
    #
    #     #请求成功 返回 200
    #     self.assertEqual(res.status_code,userData['status_code_200'])

    def test_GetAccountsOfUser_008(self):
         '''获取用户的交易账号列表（个人展示页）'''
         #/api/v2/trade/users/:id/accounts
         url=userData['hostName']+userDataPersonalPageUrl['getAccountsOfUser_url1']+self.tradeUserID\
             +userDataPersonalPageUrl['getAccountsOfUser_url2']
         res=PersonalPage.getAccountsOfUser(url,headers=userData['headers'])
         FMCommon.printLog(res.text)

         #请求成功 返回 200
         self.assertEqual(res.status_code,userData['status_code_200'])

    def test_GetAttentionSymbols_009(self):
        '''获取某用户交易账号关注品种（个人展示页）'''
        #/api/v2/trade/accounts/:account/attention-symbols
        url=userData['hostName']+userDataPersonalPageUrl['getAttentionSymbols_url1']+self.tradeUserID+'_'+userData['pgAccountIndex']\
             +userDataPersonalPageUrl['getAttentionSymbols_url2']
        res=PersonalPage.getAccountsOfUser(url,headers=userData['headers'])
        FMCommon.printLog(res.text)

        #请求成功 返回 200
        self.assertEqual(res.status_code,userData['status_code_200'])

    def test_GetOrderSymbolsOfUserAccount_010(self):
        '''获取某用户交易账号的订单涉及到的交易品种列表（个人展示页） '''
        #api/v2/trade/accounts/:account/order-symbols
        url=userData['hostName']+userDataPersonalPageUrl['getOrderSymbolsOfUserAccount_url1']+self.tradeUserID+'_'+userData['pgAccountIndex']\
             +userDataPersonalPageUrl['getOrderSymbolsOfUserAccount_url2']
        res=PersonalPage.getAccountsOfUser(url,headers=userData['headers'])
        FMCommon.printLog(res.text)
        tradeSignout = Auth.signout(userData['hostName'] + userDataAuthUrl['signout_url'], datas = self.tradeHeaders)
        self.assertEqual(tradeSignout.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()