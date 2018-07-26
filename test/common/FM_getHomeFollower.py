#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getHomeFollower
# 用例标题: 获取首页的跟随者收益信息
# 预置条件: 
# 测试步骤:
#   1.不登录的情况下获取首页的跟随者收益信息
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

class GetHomeFollower(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_getHomeFollower(self):
        '''获取首页的跟随者收益信息'''
        getHomeFollower = Common.getHomeFollower(webAPIData['hostName'] + commonData['getHomeFollower_url'])
        self.assertEqual(getHomeFollower.status_code, webAPIData['status_code_200'])

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

