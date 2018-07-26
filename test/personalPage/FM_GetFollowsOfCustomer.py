#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PersonalPage_GetFollowsOfCustomer_001
# 用例标题:
# 预置条件:
# 测试步骤:
#   1.跟随者设置跟随交易员
#   2.跟随者的正在跟随交易员
#   3.取消跟随
#   4.跟随者正在跟随和历史跟随查询是否存在
# 预期结果:
#   1.200  SUCCESS
# 脚本作者: Yangyang
# 写作日期: 20171113
#=========================================================

import sys
import unittest
import json
sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import Auth
import FMCommon
import Follow
import PersonalPage
import Account


userData = FMCommon.loadWebAPIYML()
userDataAccountUrl=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()
userDataFollUrl=FMCommon.loadFollowYML()
userDataPersonalPageUrl=FMCommon.loadPersonalPageYML()

'''检查正在跟随和历史跟随的跟随者'''
class GetFollowsOfCustomer(unittest.TestCase):

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

        datas = {"account": userData['followAccount'], "password": userData['followPasswd'], "remember": "false"}
        signinRes = Auth.signin(userData['hostName'] + userDataAuthUrl['signin_url'], userData['headers'], datas)
        # 登录成功，返回200 ok
        self.assertEqual(signinRes.status_code, userData['status_code_200'])
        # #保存登录时的token，待登出使用
        self.token = json.loads(signinRes.text)['data']['token']
        self.headers = {'content-type': 'application/json','Authorization': 'Bearer ' + self.token}
        #保存userID
        self.followUserID = str(json.loads(signinRes.text)['data']['id'])
        # 获取AccountIndex
        accIndexUrl = userData['hostName']+userDataAccountUrl['getAccount_url']
        accIndexRes = Account.getAccount(accIndexUrl, headers=self.headers)
        # print(u'获取当前登录账户的AccountIndex Url: '+accIndexUrl)

        FMCommon.printLog(accIndexRes.text)
        # 请求成功 返回200
        self.assertEqual(accIndexRes.status_code, userData['status_code_200'])
        # self.accountIndex = json.loads(accIndexRes.text)['data']['AccountIndex']

    '''获取交易员账号的正在跟随跟随者列表（个人展示页）'''

    def test_CreateFollOfGetFollowing(self):
        '''创建跟随获取交易员账号正在跟随列表'''
        createFollUrl = userData['hostName']+userDataFollUrl['createFollow_url'] + \
            self.tradeUserID+'_'+userData['pgAccountIndex']
        params={'accountIndex':userData['pgAccountIndex'],'strategy':userData['follStrategy'],
                'setting':userData['follSetting'],'direction':userData['follDirection']}
        createFollRes = Follow.createFollow(createFollUrl, headers=self.headers,datas=params,interfaceName='CreateFollow')
        # print(u'创建跟随的Url: ' + createFollUrl)
        FMCommon.printLog(createFollRes.text)
        # 请求成功 返回200
        self.assertEqual(createFollRes.status_code,userData['status_code_200'])

        follOfCustomerUrl = userData['hostName']+userDataPersonalPageUrl['getFollowsOfCustomer_url1'] +\
            self.followUserID+'_' + \
            str(userData['pgAccountIndex'])+userDataPersonalPageUrl['getFollowsOfCustomer_url2']
        # print(u'获取正在跟随交易员的跟随者列表Url: ' + follOfCustomerUrl)

        follOfTrdRes = PersonalPage.getFollowsOfCustomer(follOfCustomerUrl, headers=self.headers, isFollowing=userData['isFollowing'])

        FMCommon.printLog(follOfTrdRes.text)
        # 请求成功 返回 200
        self.assertEqual(follOfTrdRes.status_code, userData['status_code_200'])
        # 判断跟随者是否存在列表中
        self.assertIn(self.tradeNickName, str(json.loads(follOfTrdRes.text)['data']['items']))
        self.assertIn(self.tradeUserID, str(json.loads(follOfTrdRes.text)['data']['items']))

    ''' 取消跟随，并获取正在跟随和历史跟随中是否存在该跟随者'''

    def test_DeleteFollOfGetHisFollow(self):
        # 取消跟随
        # api/v1/trade/follows/:trader_index

        deleteFollUrl = userData['hostName']+userDataFollUrl['createFollow_url']+self.tradeUserID+'_'+userData['pgAccountIndex']+'?accountIndex='\
            + str(userData['pgAccountIndex'])
        deleteFollRes = Follow.deleteFollow(deleteFollUrl, headers=self.headers)

        # print(u'取消跟随 Url: ' + deleteFollUrl)

        FMCommon.printLog(deleteFollRes.text)

        # 请求成功 返回200
        '''取消跟随成功'''
        self.assertEqual(deleteFollRes.status_code,userData['status_code_200'])

        # 获取交易员账号的正在跟随真实跟随者列表（个人展示页）

        followingUrl = userData['hostName']+userDataPersonalPageUrl['getFollowsOfCustomer_url1'] +\
            self.followUserID+'_' + \
            str(userData['pgAccountIndex'])+userDataPersonalPageUrl['getFollowsOfCustomer_url2']

        followingRes = PersonalPage.getFollowsOfCustomer(followingUrl, headers=self.headers, isFollowing=userData['isFollowing'])
        # print(u'获取取消跟随后的正在跟随交易员的跟随者列表Url: ' + followingUrl)

        FMCommon.printLog(followingRes.text)
        # 请求成功 返回 200
        '''查询取消跟随后，正在跟随中是否存在该用户'''
        self.assertEqual(followingRes.status_code, userData['status_code_200'])

        '''获取交易员账号的跟随者列表（个人展示页）历史跟随'''
        followingUrl = userData['hostName']+userDataPersonalPageUrl['getFollowsOfCustomer_url1'] +\
            self.followUserID+'_' + \
            str(userData['pgAccountIndex'])+userDataPersonalPageUrl['getFollowsOfCustomer_url2']

        followingRes = PersonalPage.getFollowsOfCustomer(followingUrl, headers=self.headers, isFollowing=userData['isFollowingFalse'])

        # print(u'获取历史跟随的 Url: ' + followingUrl)

        FMCommon.printLog(followingRes.text)

        # 请求成功 返回 200
        self.assertEqual(followingRes.status_code, userData['status_code_200'])

    def tearDown(self):
        # 退出
        print('退出！')
        tradeSignout = Auth.signout(userData['hostName'] + userDataAuthUrl['signout_url'], datas = self.tradeHeaders)
        self.assertEqual(tradeSignout.status_code, userData['status_code_200'])
        signoutRes = Auth.signout(userData['hostName'] + userDataAuthUrl['signout_url'], datas = userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()
