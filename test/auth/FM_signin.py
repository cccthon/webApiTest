#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_WebAPI_Auth_signin_001_001
# 用例标题: 通过账号登录followme系统
# 预置条件: 
# 测试步骤:
#   1.调用接口：sigin,传入账号，密码，请求url，header发起post请求
# 预期结果:
#   1.登录成功，返回当前账户信息
#   2.检查响应码为：200，nickname正确
# 脚本作者: shencanhui
# 写作日期: 20171030
#=========================================================
import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
import Auth,FMCommon,Account
from socketIO_client import SocketIO
from base64 import b64encode

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()

class Signin(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_signin(self):

        '''登录followme系统'''
        datas = {"account":webAPIData['account'], "password":webAPIData['passwd'], "remember":"false"}
        signinRes = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], datas)
        '''登录成功，返回200 ok'''
        self.assertEqual(signinRes.status_code, webAPIData['status_code_200'])
        #保存登录时的token，待登出使用
        self.token = json.loads(signinRes.text)['data']['token']
        #规整headers 
        webAPIData['headers'][webAPIData['Authorization']] = webAPIData['Bearer'] + self.token

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        signoutRes = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = webAPIData['headers'])
        self.assertEqual(signoutRes.status_code, webAPIData['status_code_200'])

if __name__ == '__main__':
    unittest.main()

