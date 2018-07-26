import sys,unittest,json,requests,gc,redis,re,time

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../test/followStar")

import FMCommon,FollowStar
import MysqlDBOperation


userData = FMCommon.loadWebAPIYML()
userDataFollowStar = FMCommon.loadFollowStarYML()

class MyTrade(unittest.TestCase):
    def setUp(self):
        # 1.登录followstar
        datas = {"account": '18088888802', "password": '123456'}
        followstarloginRES = FollowStar.loginFStar(userData['hostPyramid']+userDataFollowStar['followStarLogin_url'],
                                                   userData['headers'],datas,interfaceName='followStarLogin')
        self.assertEqual(followstarloginRES.status_code, userData['status_code_200'])
        self.userId = json.loads(followstarloginRES.text)['data']['userId']
        self.FollowStarToken = json.loads(followstarloginRES.text)['data']['token']

    def test_MyTrade(self):
        # 2.获取我的交易数据
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.FollowStarToken})
        GetMemberInfoRES = FollowStar.GetMemberInfo(userData['hostPyramid'] + userDataFollowStar['GetMemberInfo_url'],
                                                              userData['headers'], interfaceName='GetMyTradeInfo')
        self.assertEqual(GetMemberInfoRES.status_code, userData['status_code_200'])
        self.FMBalance = json.loads(GetMemberInfoRES.text)['data']['Balance']
        self.IncomeAmount = json.loads(GetMemberInfoRES.text)['data']['TotalIncomeAmount']
        self.Lot = json.loads(GetMemberInfoRES.text)['data']['TotalLot']
        self.Commission = json.loads(GetMemberInfoRES.text)['data']['Commission']

        selectMemberInfoSql = 'select FMUserBalance,TotalLot,Commission from usersummary where UserId='+str(self.userId)
        selectMemberInfoRow = MysqlDBOperation.OperationMysqlDB.operationPyramidDB(selectMemberInfoSql)

        # 验证我的余额和交易量，服务费是否正确
        self.assertEqual(self.FMBalance, float(selectMemberInfoRow["FMUserBalance"]),"余额不正确")
        self.assertEqual(self.Lot, float(selectMemberInfoRow["TotalLot"]), "交易量不正确")
        self.assertEqual(self.Commission, float(selectMemberInfoRow["Commission"]), "服务费不正确")

    def tearDown(self):
        # 登出
        FollowStarLogoutRES = FollowStar.FollowStarLogout(userData['hostPyramid'] + userDataFollowStar['FollowStarLogout_url'],
                                                          userData['headers'], interfaceName='FollowStarLogout')
        self.assertEqual(FollowStarLogoutRES.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()
