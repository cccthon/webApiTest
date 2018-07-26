#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_WebAPI_RiskControl_getRiskControl_001_001
# 用例标题: 获取跟随者风控全局设置
# 预置条件: 
# 测试步骤:
#   1.调用接口：getRiskControl,请求url，header发起get请求
# 预期结果:
#   1.风控设置返回成功
#   2.检查响应码为：200
# 脚本作者: shencanhui
# 写作日期: 20171113
#=========================================================
import sys,unittest,json,requests
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
import FMCommon,Auth,RiskControl,Follow,Social
from socketIO_client import SocketIO
from base64 import b64encode

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
riskControlData = FMCommon.loadRiskControlYML()

class GetRiskControl(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        datas = {"account":webAPIData['followAccount'], "password":webAPIData['followPasswd'], "remember":"false"}
        signinRes = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], datas)
        #登录成功，返回200 ok
        self.assertEqual(signinRes.status_code, webAPIData['status_code_200'])
        # #保存登录时的token，待登出使用
        self.token = json.loads(signinRes.text)['data']['token']
        #规整headers
        webAPIData['headers'][webAPIData['Authorization']] = webAPIData['Bearer'] + self.token

    # def test_getUserID(self):
    #     '''获取tradeIndex设置信息'''
    #     getUserID = Follow.getUserID(params = json.dumps({"keyword":webAPIData['nickName']}))
    #     print('UserID: ', getUserID)

    def test_getRiskControl_withDefaultIndex(self):
        '''获取风控设置信息''' 
        getRiskControlRes = RiskControl.getRiskControl(webAPIData['hostName'] + riskControlData['riskcontrol_url'], headers = webAPIData['headers'])
        self.assertEqual(getRiskControlRes.status_code, webAPIData['status_code_200'])

    def test_getRiskControl_withSpecialIndex(self):
        '''通过accountindex,获取某一个账户的风控设置信息'''
        getRiskControlRes = RiskControl.getRiskControl(webAPIData['hostName'] + riskControlData['riskcontrol_url'], headers = webAPIData['headers'], accountIndex = "3")
        self.assertEqual(getRiskControlRes.status_code, webAPIData['status_code_200'])

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        signoutRes = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = webAPIData['headers'])
        self.assertEqual(signoutRes.status_code, webAPIData['status_code_200'])

if __name__ == '__main__':
    unittest.main()

