#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_FollowStarlogin
# 用例标题: 登录FollowStar系统
# 预置条件:
# 测试步骤:
#   1.登录FollowStar  2.退出
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: wangmingli
# 写作日期:
# 修改人：liujifeng
# 修改日期：20180712
#=========================================================
import sys,unittest,json,requests,gc,redis,re,time

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import FMCommon,FollowStar

userData = FMCommon.loadWebAPIYML()
userDataFollowStar = FMCommon.loadFollowStarYML()

class login(unittest.TestCase):
    def setUp(self):
        pass

    def test_login(self):
        # 1.登录FollowStar
        datas = {"account": '18088888802', "password": '123456'}
        followstarloginRES = FollowStar.loginFStar(userData['hostPyramid']+userDataFollowStar['followStarLogin_url'],
                                                   userData['headers'],datas,interfaceName='followStarLogin')
        self.assertEqual(followstarloginRES.status_code, userData['status_code_200'])
        self.userId = json.loads(followstarloginRES.text)['data']['userId']
        self.FollowStarToken = json.loads(followstarloginRES.text)['data']['token']
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.FollowStarToken

    def tearDown(self):
        # 2.登出
        FollowStarLogoutRES = FollowStar.FollowStarLogout(
            userData['hostPyramid'] + userDataFollowStar['FollowStarLogout_url'],
            userData['headers'], interfaceName='FollowStarLogout')
        self.assertEqual(FollowStarLogoutRES.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()
