#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_searchBlogByKeyWord
# 用例标题: 社区搜索（用户，微博）
# testcase001：根据关键字搜索微博
    #1、登录账号A
    #2、根据关键字搜索微博

# testcase002：
    #1、登录账号A
    #2、根据关键字搜索用户

# testcase003：
    #1、注册账号A，
    #2、登录账号B，搜索该昵称

import sys,requests,unittest,yaml,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,newSocial,FMCommon,Http,time

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadnewSocialYML()
authData=FMCommon.loadAuthYML()

class SearchBlogByKeyWord(unittest.TestCase):
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

    def test_searchBlogByKeyWord(self):
        '''根据关键字搜索微博'''
        key="黄金"
        searchRes=newSocial.searchByKeyWord(userData['hostName']+socialData['searchBlogByKeyWord_url']+key)
        #断言返回200，code=0，搜索成功
        self.assertEqual(searchRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(searchRes.text)['code'],userData['code_0'],"搜索出错")

    def test_searchUserByKeyWord001(self):
        '''根据关键字搜索用户'''
        key=self.nickName
        searchRes=newSocial.searchByKeyWord(userData['hostName']+socialData['searchUserByKeyWord_url']+key)
        #断言返回200，code=0，搜索成功
        self.assertEqual(searchRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(searchRes.text)['code'],userData['code_0'])
        #nickname存在于搜索出来的用户列表中
        searchUserList=json.loads(searchRes.text)['data']['Items']
        userNickNameList=[]
        for i in searchUserList:
            userNickNameList.append(i['BaseInfo']['NickName'])
        self.assertIn(self.nickName,userNickNameList,"搜索出错")


    def tearDown(self):
        #退出登录
        signOutRes=Auth.signout(userData['hostName']+ authData['signout_url'],datas = self.headers)
        self.assertEqual(signOutRes.status_code,userData['status_code_200'])



if __name__=='__main__':
    unittest.main()