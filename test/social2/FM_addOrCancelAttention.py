#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_addOrCancelAttention
# 用例标题: 关注用户，分别检查关注列表和粉丝列表
# testcase0011：
    #1、登录
    #2、关注用户
    #3、检查关注列表

#testcase002:
    # 1、登录
    # 2、关注用户
    # 3、检查粉丝列表

import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,newSocial,FMCommon,Http

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadnewSocialYML()
authData=FMCommon.loadAuthYML()

class addOrCancelAttention(unittest.TestCase):
    def setUp(self):
        #登录账号A
        siginParams= {"account": userData['account'], "password": userData['passwd'], "remember": False}
        siginRes=Auth.signin(userData['hostName']+authData['signin_url'],headers = userData['headers'],datas = siginParams)
        #断言返回200登录成功
        self.assertEqual(siginRes.status_code,userData['status_code_200'])
        #获取headers
        self.token=json.loads(siginRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})
        self.userId=json.loads(siginRes.text)['data']['id']
        self.nickName=json.loads(siginRes.text)['data']['nickname']

        #登录账号B
        siginFollowParams= {"account": userData['followAccount'], "password": userData['followPasswd'], "remember": False}
        siginFollowRes=Auth.signin(userData['hostName']+authData['signin_url'],headers = userData['headers'],datas = siginFollowParams)
        #断言返回200登录成功
        self.assertEqual(siginFollowRes.status_code,userData['status_code_200'])
        #获取headers
        self.followToken=json.loads(siginFollowRes.text)['data']['token']
        self.followHeaders=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.followToken})
        self.followUserId=json.loads(siginFollowRes.text)['data']['id']
        self.followNickName = json.loads(siginFollowRes.text)['data']['nickname']

        #判断用户A当前是否关注了用户B，如果已经关注，不做操作，没有关注，执行关注
        #获取用户A的关注列表
        myAttentionsRes=newSocial.getMyAttentions(userData['hostName']+socialData['getMyAttentions_url'],headers = self.headers)
        #断言返回200,code=0,获取关注列表成功
        self.assertEqual(myAttentionsRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(myAttentionsRes.text)['code'],userData['code_0'])
        #获取关注列表用户
        attentionUserList=json.loads(myAttentionsRes.text)['data']['Items']
        userIdList = []
        for i in range(len(attentionUserList)):
            if attentionUserList[i]['UserInfo'] != None:
                userIdList.append(attentionUserList[i]['UserInfo']['BaseInfo']['UserId'])
        if self.followUserId not in userIdList:
            params={"toUserId":self.followUserId}
            attentionRes=newSocial.addOrCancelAttention(userData['hostName']+socialData['addOrCancelAttention_url'],datas = params, headers= self.headers)
            self.assertEqual(attentionRes.status_code,userData['status_code_200'])
            self.assertEqual(json.loads(attentionRes.text)['code'],0)
        else:
            pass


    def test_attentionUser001(self):
        '''关注用户，检查关注列表'''
        myAttentionsRes=newSocial.getMyAttentions(userData['hostName']+socialData['getMyAttentions_url'],headers = self.headers)
        #断言返回200,code=0,获取关注列表成功
        self.assertEqual(myAttentionsRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(myAttentionsRes.text)['code'],userData['code_0'])

        #获取关注列表用户
        attentionUserList=json.loads(myAttentionsRes.text)['data']['Items']
        userIdList = []
        for i in range(len(attentionUserList)):
            if attentionUserList[i]['UserInfo'] != None:
                userIdList.append(attentionUserList[i]['UserInfo']['BaseInfo']['UserId'])
        self.assertIn(self.followUserId,userIdList)

    def test_attentionUser002(self):
        '''关注用户，检查粉丝列表'''
        myFansRes=newSocial.getMyFans(userData['hostName']+socialData['getMyFans_url'],headers = self.followHeaders)
        #断言返回200，code=0，获取粉丝列表成功
        self.assertEqual(myFansRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(myFansRes.text)['code'],userData['code_0'])

        #检查用户A UserId存在于用户B粉丝列表UserId中
        fansUserList=json.loads(myFansRes.text)['data']['Items']
        userIdList=[]
        for i in range(len(fansUserList)):
            userIdList.append(fansUserList[i]['UserInfo']['BaseInfo']['UserId'])
        self.assertIn(self.userId,userIdList)

    def tearDown(self):
        #清空测试环境
        #取消关注
        params={"toUserId":self.followUserId}
        attentionRes=newSocial.addOrCancelAttention(userData['hostName']+socialData['addOrCancelAttention_url'],datas = params, headers= self.headers)
        self.assertEqual(attentionRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(attentionRes.text)['code'],0)

        #退出登录
        signOutRes=Auth.signout(userData['hostName']+ authData['signout_url'],datas = self.headers)
        self.assertEqual(signOutRes.status_code,userData['status_code_200'])

if __name__=='__main__':
    unittest.main()