#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_MyTeam
# 用例标题: 我的团队数据验证
# 预置条件:
# 测试步骤:
#   1.登录FollowStar   2. 按照关键字、全部星级、全部交易时间搜索    3. 验证首页团队成员数量与仓位总结一致
#   4. 验证首页团队余额与仓位总结一致   5. 验证首页团队交易量与仓位总结一致  6. 首页升级信息  7.首页个人信息
#   8. 根据关键字搜索昵称, 只显示五条
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: wangmingli
# 写作日期:
# 修改人：liujifeng
# 修改日期：
#=========================================================
import sys,unittest,json,requests,gc,redis,re,time

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import FMCommon,FollowStar

userData = FMCommon.loadWebAPIYML()
userDataFollowStar = FMCommon.loadFollowStarYML()

class MyTeam(unittest.TestCase):
    def setUp(self):
        # 1.登录FollowStar
        datas = {"account": '18088888802', "password": '123456'}
        followstarloginRES = FollowStar.loginFStar(userData['hostPyramid']+userDataFollowStar['followStarLogin_url'],
                                                   userData['headers'],datas,interfaceName='followStarLogin')
        self.assertEqual(followstarloginRES.status_code, userData['status_code_200'])
        self.userId = json.loads(followstarloginRES.text)['data']['userId']
        self.FollowStarToken = json.loads(followstarloginRES.text)['data']['token']
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.FollowStarToken

    def test_MyTeam(self):
        ''' 3.按照关键字、全部星级、全部交易时间搜索 '''
        # levelId:	星级类型 0:全部， 1: 1/2星，3：3星，4:4星，5：5星
        levelId_all = '0'
        # timeSelectType 交易时间分类 0：全部 1：今天 2：昨天 3：本周 4：上周 5：本月 6：上个月 如果TimeSelectType==7 则表示自定义时间
        timeSelectType_all = '0'
        GetTeamInfoPageRES = FollowStar.GetTeamInfoPage(
            userData['hostPyramid']+userDataFollowStar['GetTeamInfoPage_url']+'&userId='+str(self.userId)
            +'&levelId='+levelId_all+'&startRegisterDate='+'&endRegisterDate='
            +'&timeSelectType='+timeSelectType_all+'&startTradeDate=&endTradeDate=',
            userData['headers'], interfaceName='GetTeamInfoPage')
        print(GetTeamInfoPageRES.text)
        self.assertEqual(GetTeamInfoPageRES.status_code, userData['status_code_200'])
        # 验证团队详情数据正确性

        # *********此下未调试************
        # # 4.团队详情，统计行
        # GetTeamInfoStatisticsRES = userDataFollowStar.GetTeamInfoStatistics(userData['hostPyramid'] + userDataFollowStar['GetTeamInfoStatistics_url'],
        #                                                       userData['headers'], interfaceName='GetTeamInfoStatistics')
        # print(GetTeamInfoStatisticsRES.text)
        # self.assertEqual(GetTeamInfoStatisticsRES.status_code, userData['status_code_200'])

        # 首页-获取我的团队数据
        GetMemberInfoRES = FollowStar.GetMemberInfo(userData['hostPyramid'] + userDataFollowStar['GetMemberInfo_url'],
                                                              userData['headers'], interfaceName='GetMyTradeInfo')
        self.assertEqual(GetMemberInfoRES.status_code, userData['status_code_200'])
        self.TeamPersonCount = json.loads(GetMemberInfoRES.text)['data']['TeamPersonCount']
        self.TeamTotalBalance = json.loads(GetMemberInfoRES.text)['data']['TeamTotalBalance']
        self.TeamTotalLot = json.loads(GetMemberInfoRES.text)['data']['TeamTotalLot']

        # 仓位总结团队统计数据
        GetTeamInfoStatisticsRES = FollowStar.GetTeamInfoStatistics(userData['hostPyramid'] + userDataFollowStar['GetTeamInfoStatistics_url']+'?userId='+str(self.userId)
            +'&levelId='+levelId_all+'&startRegisterDate='+'&endRegisterDate='+'&timeSelectType='+timeSelectType_all+'&startTradeDate=&endTradeDate=',
            userData['headers'], interfaceName='GetTeamInfoStatistics')
        print(GetTeamInfoStatisticsRES.text)
        self.assertEqual(GetTeamInfoStatisticsRES.status_code, userData['status_code_200'])
        # 团队成员数量
        self.TotalUserCount = json.loads(GetTeamInfoStatisticsRES.text)['data']['TotalUserCount']
        # 团队余额
        self.FmBalance = json.loads(GetTeamInfoStatisticsRES.text)['data']['FmBalance']
        # 团队交易量
        self.Lot = json.loads(GetTeamInfoStatisticsRES.text)['data']['Lot']
        # # 验证团队详情，统计行数据正确性
        # 验证首页团队成员数量与仓位总结一致
        self.assertEqual(self.TeamPersonCount, self.TotalUserCount, "成员数量不一致")
        # 验证首页团队余额与仓位总结一致
        self.assertEqual(self.TeamTotalBalance, self.FmBalance, "余额不一致")
        # 验证首页团队交易量与仓位总结一致
        self.assertEqual(self.TeamTotalLot, self.Lot, "交易量不一致")


        # # 5.我的团队，团队成员
        # GetTeamPersonInfoPageRES = userDataFollowStar.GetTeamPersonInfoPage(userData['hostPyramid'] + userDataFollowStar['GetTeamPersonInfoPage_url'],
        #                                                                     userData['headers'], interfaceName='GetTeamPersonInfoPage')
        # print(GetTeamPersonInfoPageRES.text)
        # self.assertEqual(GetTeamPersonInfoPageRES.status_code, userData['status_code_200'])
        # # 验证团队成员数据正确性
        #
        # # 6.我的团队，团队成员底部统计
        # GetTeamPersonStatisticsRES = userDataFollowStar.GetTeamPersonStatistics(userData['hostPyramid'] + userDataFollowStar['GetTeamPersonStatistics_url'],
        #                                                                     userData['headers'], interfaceName='GetTeamPersonStatistics')
        # print(GetTeamPersonStatisticsRES.text)
        # self.assertEqual(GetTeamPersonStatisticsRES.status_code, userData['status_code_200'])
        # # 验证我的团队成员底部统计数据正确性
        # # 7.我的团队，团队交易
        # GetTeamTradePageRES = userDataFollowStar.GetTeamTradePage(userData['hostPyramid'] + userDataFollowStar['GetTeamTradePage_url'],
        #                                                                         userData['headers'], interfaceName='GetTeamTradePage')
        # print(GetTeamTradePageRES.text)
        # self.assertEqual(GetTeamTradePageRES.status_code, userData['status_code_200'])
        #
        # # 验证我的团队，团队交易数据正确性
        # # 8.我的团队，团队交易底部统计
        # GetTeamTradeStatisticsRES = userDataFollowStar.GetTeamTradeStatistics(userData['hostPyramid'] + userDataFollowStar['GetTeamTradeStatistics_url'],
        #                                                           userData['headers'], interfaceName='GetTeamTradeStatistics')
        # print(GetTeamTradeStatisticsRES.text)
        # self.assertEqual(GetTeamTradeStatisticsRES.status_code, userData['status_code_200'])
        #
        # # 9.首页升级信息
        # GetUpgradeInfoRES = userDataFollowStar.GetUpgradeInfo(userData['hostPyramid'] + userDataFollowStar['GetUpgradeInfo_url'],
        #                                                                       userData['headers'], interfaceName='GetUpgradeInfo')
        # print(GetUpgradeInfoRES.text)
        # self.assertEqual(GetUpgradeInfoRES.status_code, userData['status_code_200'])

        # # 9.首页升级信息
        TakeUserUpgradeTipRES = FollowStar.TakeUserUpgradeTip(userData['hostPyramid'] + userDataFollowStar['TakeUserUpgradeTip_url'],
                                                                              userData['headers'], interfaceName='TakeUserUpgradeTip')
        print(TakeUserUpgradeTipRES.text)
        self.assertEqual(TakeUserUpgradeTipRES.status_code, userData['status_code_200'])

        # # 10.首页个人信息
        # GetUserInfoRES = userDataFollowStar.GetUserInfo(userData['hostPyramid'] + userDataFollowStar['GetUserInfo_url'],
        #                                                       userData['headers'], interfaceName='GetUserInfo')
        # print(GetUserInfoRES.text)
        # self.assertEqual(GetUserInfoRES.status_code, userData['status_code_200'])
        GetMemberInfoRES = FollowStar.GetMemberInfo(userData['hostPyramid'] + userDataFollowStar['GetMemberInfo_url'],
                                                              userData['headers'], interfaceName='GetMyTradeInfo')
        self.assertEqual(GetMemberInfoRES.status_code, userData['status_code_200'])
        #
        # # 11.根据关键字搜索昵称, 只显示五条
        # SearchNickNameWithKeyRES = userDataFollowStar.SearchNickNameWithKey(userData['hostPyramid'] + userDataFollowStar['SearchNickNameWithKey_url'],
        #                                                 userData['headers'], interfaceName='SearchNickNameWithKey')
        # print(SearchNickNameWithKeyRES.text)
        # self.assertEqual(SearchNickNameWithKeyRES.status_code, userData['status_code_200'])

        # 11.根据关键字搜索昵称, 只显示五条
        key = "002"
        SearchNickNameWithKeyRES = FollowStar.SearchNickNameWithKey(userData['hostPyramid'] + userDataFollowStar['SearchNickNameWithKey_url']+'?key='+key,
                                                        userData['headers'], interfaceName='SearchNickNameWithKey')
        print(SearchNickNameWithKeyRES.text)
        self.assertEqual(SearchNickNameWithKeyRES.status_code, userData['status_code_200'])

    def tearDown(self):
        # 登出
        FollowStarLogoutRES = FollowStar.FollowStarLogout(
            userData['hostPyramid'] + userDataFollowStar['FollowStarLogout_url'],
            userData['headers'], interfaceName='FollowStarLogout')
        self.assertEqual(FollowStarLogoutRES.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()
