#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_Emailregister
# 用例标题: 邮箱注册Followme帐号
# 预置条件:
# 测试步骤:
#   1. 登录  2.邮箱注册  3.获取邮箱验证码  4.验证邮箱验证码
#   5.设置昵称  6.注销
# 预期结果:
#   1.检查响应码为：200
# 脚本作者:
# 写作日期:
#=========================================================

import sys,unittest,json,requests,gc,redis,re

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import FMCommon,Account,Auth

userData = FMCommon.loadWebAPIYML()
userDataAccountUrl=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()

class Emailregister(unittest.TestCase):
    def setUp(self):
        pass

    def test_Emailregister(self):
        '''1.登录Followme系统'''


        pass
    def tearDown(self):

       pass


if __name__ == '__main__':
    unittest.main()