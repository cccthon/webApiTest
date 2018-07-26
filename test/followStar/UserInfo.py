import sys,unittest,json,requests,gc,redis,re,time

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import FMCommon,FollowStar

userData = FMCommon.loadWebAPIYML()
userDataFollowStar = FMCommon.loadFollowStarYML()

class UserInfo(unittest.TestCase):
    def setUp(self):
        # 1.登录followstar
        datas = {"account": '13444444401', "password": '123456'}
        followstarloginRES = FollowStar.loginFStar(userData['hostPyramid']+userDataFollowStar['followStarLogin_url'],
                                                   userData['headers'],datas,interfaceName='followStarLogin')
        self.assertEqual(followstarloginRES.status_code, userData['status_code_200'])
        self.userId = json.loads(followstarloginRES.text)['data']['userId']
        self.FollowStarToken = json.loads(followstarloginRES.text)['data']['token']
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.FollowStarToken

    def test_UserInfo(self):
        pass

    def tearDown(self):
        # 登出
        FollowStarLogoutRES = userDataFollowStar.FollowStarLogout(userData['hostPyramid'] + userDataFollowStar['FollowStarLogout_url'],
                                                                  userData['headers'], interfaceName='FollowStarLogout')
        self.assertEqual(FollowStarLogoutRES.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()
