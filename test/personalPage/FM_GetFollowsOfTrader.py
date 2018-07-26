#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PersonalPage_GetFollowsOfTrader_001
# 用例标题:
# 预置条件:
# 测试步骤:
#   1.跟随者设置跟随交易员
#	2.查新交易员正在跟随列表是否包含该跟随者
#   3.取消跟随
#   4.正在跟随和历史跟随查询是否存在
# 预期结果:
#   1.200  SUCCESS
# 脚本作者: Yangyang
# 写作日期: 20171113
#=========================================================

import sys, unittest,json
sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import Auth,FMCommon,Follow,PersonalPage,Account,FollowManage

userData = FMCommon.loadWebAPIYML()
userDataAccountUrl=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()
userDataFollUrl=FMCommon.loadFollowYML()
userDataPersonalPageUrl=FMCommon.loadPersonalPageYML()


class GetFollowsOfTrader(unittest.TestCase):
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

        datas = {"account":userData['followAccount'], "password":userData['followPasswd'], "remember":"false"}
        signinRes = Auth.signin(userData['hostName'] + userDataAuthUrl['signin_url'], userData['headers'], datas)
        #登录成功，返回200 ok
        self.assertEqual(signinRes.status_code, userData['status_code_200'])
        # #保存登录时的token，待登出使用
        self.token = json.loads(signinRes.text)['data']['token']
        self.headers={'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}

         # 获取AccountIndex
        accIndexUrl=userData['hostName']+userDataAccountUrl['getAccount_url']
        accIndexRes=Account.getAccount(accIndexUrl,headers=self.headers)
        # print(u'获取当前登录账户的AccountIndex Url: '+accIndexUrl)

        FMCommon.printLog(accIndexRes.text)
        #请求成功 返回200
        self.assertEqual(accIndexRes.status_code,userData['status_code_200'])
        # self.accountIndex=json.loads(accIndexRes.text)['data']['AccountIndex']

    '''创建跟随关系获取交易员的跟随者列表'''
    def test_CreateFollowOfgetFollowersOfTrader(self):
        createFollUrl=userData['hostName']+userDataFollUrl['createFollow_url']+self.tradeUserID+'_'+userData['pgAccountIndex']

        params = {'accountIndex': userData['pgAccountIndex'], 'strategy': userData['follStrategy'],
                  'setting': userData['follSetting'], 'direction': userData['follDirection']}
        createFollRes = Follow.createFollow(createFollUrl, headers=self.headers, datas=params,
                                            interfaceName='CreateFollow')

        # print('Create follow Url: ' + createFollUrl)
        FMCommon.printLog(createFollRes.text)
        #请求成功 返回200
        self.assertEqual(createFollRes.status_code,userData['status_code_200'])

        #获取交易员账号的正在跟随跟随者列表（个人展示页）
        followersOfTraderUrl=userData['hostName']+userDataPersonalPageUrl['getFollowersOfTrader_url1']+self.tradeUserID+'_'+userData['pgAccountIndex']+userDataPersonalPageUrl['getFollowersOfTrader_url2']
        followersOfTraderRes=PersonalPage.getFollowersOfTrader(followersOfTraderUrl,headers=self.headers,isFollowing=userData['isFollowing'])
        # print('Followers Of trader Url: ' + followersOfTraderUrl)

        FMCommon.printLog(followersOfTraderRes.text)
        #请求成功 返回 200
        self.assertEqual(followersOfTraderRes.status_code,userData['status_code_200'])

        # self.assertIn(userData['follNickName'],str(json.loads(followersOfTraderRes.text)['data']['items']))
        # self.assertIn(userData['follUserid'],str(json.loads(followersOfTraderRes.text)['data']['items']))

    def test_DeleteFollowOfgetFollowersOfTrader(self):

        deleteFollUrl=userData['hostName']+userDataFollUrl['createFollow_url']+self.tradeUserID+'_'+userData['pgAccountIndex']+'?accountIndex='\
                      + str(userData['pgAccountIndex'])
        # print('Url: ' + deleteFollUrl)
        deleteFollRes=Follow.deleteFollow(deleteFollUrl,headers=self.headers)

        FMCommon.printLog(deleteFollRes.text)
        #请求成功 返回200
        self.assertEqual(deleteFollRes.status_code,userData['status_code_200'])

        #获取交易员账号的正在跟随真实跟随者列表（个人展示页）
        follOfTrdUrl=userData['hostName']+userDataPersonalPageUrl['getFollowersOfTrader_url1']+self.tradeUserID+'_'+userData['pgAccountIndex']+userDataPersonalPageUrl['getFollowersOfTrader_url2']
        follOfTrdRes=PersonalPage.getFollowersOfTrader(follOfTrdUrl,headers=self.headers,isFollowing=userData['isFollowing'])
        # print('Url: ' + follOfTrdUrl)

        FMCommon.printLog(follOfTrdRes.text)
        #请求成功 返回 200
        self.assertEqual(follOfTrdRes.status_code,userData['status_code_200'])

        # self.assertNotIn(userData['follNickName'],str(json.loads(follOfTrdRes.text)['data']['items']))
        # self.assertNotIn(userData['follUserid'],str(json.loads(follOfTrdRes.text)['data']['items']))

        #获取交易员账号的跟随者列表（个人展示页）正在跟随
        url=userData['hostName']+userDataPersonalPageUrl['getFollowersOfTrader_url1']+self.tradeUserID+'_'+userData['pgAccountIndex']+userDataPersonalPageUrl['getFollowersOfTrader_url2']
        res=PersonalPage.getFollowersOfTrader(url,headers=self.headers,isFollowing=userData['isFollowingFalse'])
        FMCommon.printLog(res.text)

        #请求成功 返回 200
        self.assertEqual(res.status_code,userData['status_code_200'])

        # self.assertIn(userData['follNickName'],str(json.loads(res.text)['data']['items']))
        # self.assertIn(userData['follUserid'],str(json.loads(res.text)['data']['items']))


    def tearDown(self):
        #退出
        print('退出！')
        tradeSignout = Auth.signout(userData['hostName'] + userDataAuthUrl['signout_url'], datas = self.tradeHeaders)
        self.assertEqual(tradeSignout.status_code, userData['status_code_200'])
        signoutRes = Auth.signout(userData['hostName'] + userDataAuthUrl['signout_url'], datas = userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])
if __name__ == '__main__':
    unittest.main()