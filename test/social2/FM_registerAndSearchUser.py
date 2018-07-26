 #========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_registerAndSearchUser
# 用例标题: 注册账号后，社区搜索用户
# testcase001：
    #1、注册账号A，
    #2、登录账号B，搜索该昵称
    #3、断言，注册账号的昵称存在于搜索列表的用户中

import sys,requests,unittest,yaml,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,newSocial,FMCommon,Http,re,redis,Account

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadnewSocialYML()
authData=FMCommon.loadAuthYML()
accountData=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()

class SearchBlogByKeyWord(unittest.TestCase):
    def setUp(self):
        # 获取图形验证码
        captchaUrl = userData['hostName'] + userDataAuthUrl['getCaptcha_url']
        self.user_token = Account.getTokenForCaptcha(captchaUrl)
        self.header = {'content-type': 'application/json', 'Authorization': 'Bearer ' + str(self.user_token)}

        # 读取图形验证码
        self.ccap = Account.getCaptchaForRedis(self.user_token)
        # 根据图形验证码获取短信验证码
        smsUrl = userData['hostName'] + userDataAuthUrl['getSMSScode_url'] + userData[
            'registerAccount'] + '&captcha=' + self.ccap
        print(smsUrl)
        '''获取短信验证码成功'''
        self.smsCode = Account.getSMSCodeForRedis(smsUrl, headers=self.header, userToken=str(self.user_token),
                                                  registerAccount=userData['registerAccount'])

        # OA登录
        getUserTokenRes = Auth.getUserToken(
            userData['hostNameSwagger'] + userDataAuthUrl['loginOA_url'] + userData['oaClientId']
            + "&userName=" + userData['oaUsername'] + "&password=" + userData['oapassword'],
            userData['headersOA'], interfaceName="getUserToken")

        self.assertEqual(getUserTokenRes.status_code, userData['status_code_200'])
        self.tokenOA = json.loads(getUserTokenRes.text)['accessToken']

        '''登录OA成功'''
        self.headerOA = {'content-type': 'application/json', 'Accept': 'application/json',
                         'Authorization': 'Bearer ' + str(self.tokenOA)}

        '''注册场景验证'''
        #注册
        url=userData['hostName']+userDataAuthUrl['register_url']
        res=Auth.register(url,headers=self.header,account=userData['registerAccount'],
                              password=userData['registerPwd'],platform=userData['platform'],captcha=str(self.ccap),
                              smscode=self.smsCode,invite=userData['invite'],oauth2=userData['oauth2'])
        FMCommon.printLog(res.text)

        #请求成功，返回200 ok
        '''注册成功'''
        self.assertEqual(res.status_code,userData['status_code_200'])
        self.userId=json.loads(res.text)['data']['id']

    def test_registerAndSearchUser(self):
        pass
        '''注册账号后，社区搜索该用户'''

        #社区搜索刚注册的用户昵称
        # searchRes=newSocial.searchByKeyWord(userData['hostName']+socialData['searchUserByKeyWord_url']+self.nickName)
        # #断言返回200，code=0，搜索成功
        # self.assertEqual(searchRes.status_code,userData['status_code_200'])
        # self.assertEqual(json.loads(searchRes.text)['code'],userData['code_0'])
        # #nickname存在于搜索出来的用户列表中
        # searchUserList=json.loads(searchRes.text)['data']['Items']
        # userNickNameList=[]
        # for i in searchUserList:
        #     userNickNameList.append(i['BaseInfo']['NickName'])
        # self.assertIn(self.nickName,userNickNameList,"搜索出错")

    def tearDown(self):
        #清空测试环境
        logOutUrl = userData['hostNameOA'] + userDataAuthUrl['getCloseAccount_url'] + str(self.userId)
        print(self.header)
        print(logOutUrl)
        logRes = Auth.logOut(logOutUrl, headers=self.headerOA, interfaceName='CloseAccount')
        '''注销成功'''
        self.assertEqual(logRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()

