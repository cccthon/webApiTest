#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getHomeTradeDynamic
# 用例标题: 获取首页交易动态信息
# 预置条件: 
# 测试步骤:
#   1.不登录的情况下获取首页交易动态信息
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: shencanhui
# 写作日期: 20171211
#=========================================================
import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
import Auth,FMCommon,Common
from socketIO_client import SocketIO
from base64 import b64encode

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
commonData = FMCommon.loadCommonYML()

class GetHomeTradeDynamic(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_getHomeTradeDynamic(self):
        '''获取首页交易动态信息'''
        getHomeTradeDynamic = Common.getHomeTradeDynamic(webAPIData['hostName'] + commonData['getHomeTradeDynamic_url'])
        self.assertEqual(getHomeTradeDynamic.status_code, webAPIData['status_code_200'])

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

