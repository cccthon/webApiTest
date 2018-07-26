#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_RegisterSetNicknameAndLogin
# 用例标题:
# 预置条件:
# 测试步骤:
#   1.获取图形验证码-->获取短信验证码-->注册-->登录
#   2.获取短信验证码-->获取短信验证码-->注册-->设置昵称-->登录

# 预期结果:
#   1.200  SUCCESS
# 脚本作者: Yangyang
# 写作日期: 20171127

import sys,unittest,json,requests,gc,redis,re

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import FMCommon,Account,Auth

userData = FMCommon.loadWebAPIYML()
userDataAccountUrl=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()

url=''

'''注册、设置昵称、登录'''
class RegisterSetNicknameAndLogin(unittest.TestCase):

    def setUp(self):
        #获取图形验证码
        captchaUrl=userData['hostName']+userDataAuthUrl['getCaptcha_url']
        self.user_token=Account.getTokenForCaptcha(captchaUrl)
        self.header={'content-type': 'application/json', 'Authorization': 'Bearer ' + str(self.user_token)}

        #读取图形验证码
        self.ccap =Account.getCaptchaForRedis(self.user_token)
        #根据图形验证码获取短信验证码
        smsUrl=userData['hostName'] + userDataAuthUrl['getSMSScode_url'] + userData['registerAccount']+'&captcha='+ self.ccap
        print(smsUrl)
        '''获取短信验证码成功'''
        self.smsCode = Account.getSMSCodeForRedis(smsUrl, headers=self.header,userToken=str(self.user_token),registerAccount=userData['registerAccount'])

        # OA登录.0
        getUserTokenRes = Auth.getUserToken(userData['hostNameSwagger']+userDataAuthUrl['loginOA_url'] + userData['oaClientId']
                                            + "&userName=" + userData['oaUsername'] + "&password=" + userData['oapassword'],
                                            userData['headersOA'], interfaceName="getUserToken")

        self.assertEqual(getUserTokenRes.status_code, userData['status_code_200'])
        self.tokenOA = json.loads(getUserTokenRes.text)['accessToken']
        # '''登录OA'''
        # loginOAUrl=userData['hostNameOA']+userDataAuthUrl['loginOA_url']
        # loginOARes=Auth.loginOA(loginOAUrl,headers=userData['headersOA'],username=userData['usernameOA'],password=userData['passwordOA'])
        #
        # self.assertEqual(loginOARes.status_code,userData['status_code_200'])
        # self.tokenOA=json.loads(loginOARes.text)['Result']['Token']

        '''登录OA成功'''
        self.headerOA={'content-type': 'application/json', 'Accept' : 'application/json','Authorization': 'Bearer ' + str(self.tokenOA)}

    def test_registerAndLogin(self):
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

         #注册成功后登录
        datas = {"account":userData['registerAccount'], "password":userData['registerPwd'], "remember":"false"}
        signinRes = Auth.signin(userData['hostName'] + userDataAuthUrl['signin_url'], userData['headers'], datas)

        #登录成功，返回200 ok
        '''注册登录成功'''
        self.assertEqual(signinRes.status_code,userData['status_code_200'])

        token = json.loads(signinRes.text)['data']['token']
        header={'content-type': 'application/json', 'Accept' : 'application/json','Authorization': 'Bearer ' +str(token)}

        '''设置昵称'''
        params={'nickname':'FMTESTCI0001'}
        url=userData['hostName']+userDataAccountUrl['setUserNickname_url']+ str(self.userId)+'/nickname'
        nickNameRes=Account.setUserNickname(url,headers=header,datas=params)
        print("nickNameCode: ",nickNameRes.status_code)
        print(nickNameRes.status_code)
        self.assertEqual(nickNameRes.status_code,userData['status_code_200'])

        '''修改个人信息'''
        params={'RealName':userData['realName'],'AccountEmail':userData['registerEmail'],'IDType':1,'IDNo':'411122199107208047'}
        url=userData['hostName']+userDataAccountUrl['updateUserInfo_url']
        updateUserInfoRes=Account.updateUserInfo(url,headers=header,datas=params,interfaceName="UserDataAccount")
        print(updateUserInfoRes)
        self.assertEqual(updateUserInfoRes.status_code,userData['status_code_200'])

    def tearDown(self):

       logOutUrl=userData['hostNameOA']+userDataAuthUrl['getCloseAccount_url'] + str(self.userId)
       print(self.header)
       print(logOutUrl)
       logRes=Auth.logOut(logOutUrl,headers=self.headerOA,interfaceName='CloseAccount')
       '''注销成功'''
       self.assertEqual(logRes.status_code,userData['status_code_200'])


if __name__ == '__main__':
    unittest.main()