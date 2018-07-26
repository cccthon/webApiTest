#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_WebAPI_Social_attentionUser_001
# 用例标题: 关注用户
#流程：
    #1、登录
    #2、关注用户
    #3、检查关注列表
    #4、取消关注
    #5、查看关注列表


import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,Social,FMCommon,Http

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadSocialYML()
authData=FMCommon.loadAuthYML()


class AttentionUser(unittest.TestCase):
    def setUp(self):
        # 登录账号A获取headers
        signinParams = {"account": userData['account'], "password": userData['passwd'], "remember": False}
        signinRes = Auth.signin(userData['hostName'] + authData['signin_url'],datas=signinParams,headers=userData['headers'] )
        self.assertEqual(signinRes.status_code, userData['status_code_200'])
        self.token = json.loads(signinRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})
        #取出用户id
        self.FansUserId=json.loads(signinRes.text)['data']['id']

        #登录账号获取需要关注的userid
        signinParams = {"account": userData['followAccount'], "password": userData['followPasswd'], "remember": False}
        #登录用户B检查粉丝列表数据
        signinFansRes = Auth.signin(userData['hostName'] + authData['signin_url'],datas=signinParams,headers=userData['headers'])
        self.assertEqual(signinFansRes.status_code, userData['status_code_200'])
        fansToken = json.loads(signinFansRes.text)['data']['token']
        self.userId=json.loads(signinFansRes.text)['data']['id']
        self.fansHeaders=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+ fansToken})

        #前置条件：用户A没有关注用户B,没有关注则执行关注，否则，不操作
        #获取用户A的关注列表
        attentionParam={"pageIndex":1,"pageSize":10}
        getMyAttentionsRes=Social.getMyAttentions(userData['hostName']+socialData['getMyAttentions_url'],datas=json.dumps(attentionParam),headers=self.headers)
        self.assertEqual(getMyAttentionsRes.status_code,userData['status_code_200'])
        MYattentionUserList=json.loads(getMyAttentionsRes.text)['data']['Items']
        MyAttentionUserId_list = []
        for i in MYattentionUserList:
            MyAttentionUserId_list.append(i['Id'])
        if self.userId not in MyAttentionUserId_list:
            # 用户A关注用户B
            attentionUserRes = Social.attentionUser(userData['hostName'] + socialData['attentionUser_url1'] + str(self.userId) + socialData['attentionUser_url2'], headers=self.headers)
            self.assertEqual(attentionUserRes.status_code, userData['status_code_200'])
            self.assertEqual(json.loads(attentionUserRes.text)['data']['Bmsg'],True,'关注用户失败')
        else:
            pass


    def test_atentionUser001(self):
        '''用户A关注用户B后，检查A的关注列表'''

        #获取用户A的关注列表
        attentionParam={'pageIndex':1,'pageSize':15}
        getMyAttentionsRes=Social.getMyAttentions(userData['hostName']+socialData['getMyAttentions_url'],datas=json.dumps(attentionParam),headers=self.headers)
        self.assertEqual(getMyAttentionsRes.status_code,userData['status_code_200'])

        #断言，A关注B成功后，用B的userid存在与A的关注列表中，即关注成功
        MYattentionUserList=json.loads(getMyAttentionsRes.text)['data']['Items']
        MyAttentionUserId_list = []
        for i in MYattentionUserList:
            MyAttentionUserId_list.append(i['Id'])
        self.assertIn(int(self.userId),MyAttentionUserId_list,'关注列表无最新关注的人')


    def test_attentionUser002(self):
        '''用户A关注用户B，检查用户B的粉丝列表'''

        #检查用户B的粉丝列表
        fanParams={'pageIndex':1,'pageSize':15}
        MyFansRes=Social.getMyFans(userData['hostName']+socialData['getMyFans_url'],datas=fanParams,headers=self.fansHeaders)
        self.assertEqual(MyFansRes.status_code,userData['status_code_200'])

        #获取用户B的粉丝列表
        MyFansList = json.loads(MyFansRes.text)['data']['Items']

        #断言，A关注B成功后，用户A存在于用户B粉丝列表中
        MyFansIdList=[]
        for x in MyFansList:
            MyFansIdList.append(x['Id'])
        self.assertIn(self.FansUserId,MyFansIdList,'粉丝列表没有显示最新的粉丝用户')


    def tearDown(self):
        # 清空测试环境
        # 取消关注
        delattentionUserRes = Social.attentionUser(userData['hostName'] + socialData['attentionUser_url1'] + str(self.userId) + socialData['attentionUser_url2'],headers=self.headers)
        self.assertEqual(delattentionUserRes.status_code, userData['status_code_200'])

        #退出登录
        signout = Auth.signout(userData['hostName']+ authData['signout_url'],datas=self.headers)
        self.assertEqual(signout.status_code, userData['status_code_200'])

        #退出登录
        signout = Auth.signout(userData['hostName']+ authData['signout_url'],datas=self.fansHeaders)
        self.assertEqual(signout.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()