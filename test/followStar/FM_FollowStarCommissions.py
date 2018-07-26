# -*-coding:utf-8-*-
#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_FollowStarCommissions
# 用例标题: 获取星级会员服务费核算列表（需要登录）
# 预置条件:
# 测试步骤:
# 1. 验证3星会员服务费返佣正确,服务费明细正确
# 2. 验证服务费总额、余额、已提取、审核中的金额正确
# 3. 验证提取服务费功能
# 4. FollowStar服务费提取记录明细
# 5. OA审核服务费，审核中-审核通过-已打款-打款失败
# 6. OA审核服务费，审核中-审核失败
# 预期结果:
#   1.检查响应码为：200
# 脚本作者:liujifeng
# 写作日期:20180718
# 修改人：
# 修改日期：
#=========================================================

import sys,unittest,json,requests,gc,redis,re,time

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../test/followStar")

import MysqlDBOperation
import FMCommon,Account,Auth,Trade,FollowStar,Commissions
# from lib.tradeOnline import TradeOnline
# from RegisterByMobile import RegisterByMobile
# from BindPico import BindPico
# from TradeForStar import TradeForStar
# from CloseAccounts import CloseAccounts


userData = FMCommon.loadWebAPIYML()
userDataAccountUrl=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()
userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()
userDataFollowStar = FMCommon.loadFollowStarYML()
commissionsData = FMCommon.loadCommissionsYML()

webAPIData = FMCommon.loadWebAPIYML()

class Commission(unittest.TestCase):
    def setUp(self):
        # 1.登录FollowStar
        datas = {"account": '18088888802', "password": '123456'}
        followstarloginRES = FollowStar.loginFStar(userData['hostPyramid'] + userDataFollowStar['followStarLogin_url'],
                                                   userData['headers'], datas, interfaceName='followStarLogin')
        self.assertEqual(followstarloginRES.status_code, userData['status_code_200'])
        self.userId = json.loads(followstarloginRES.text)['data']['userId']
        self.FollowStarToken = json.loads(followstarloginRES.text)['data']['token']
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.FollowStarToken

        # OA登录
        getUserTokenRes = Auth.getUserToken(
            userData['hostNameSwagger'] + userDataAuthUrl['loginOA_url'] + userData['oaClientId']
            + "&userName=" + userData['oaUsername'] + "&password=" + userData['oapassword'],
            userData['headersOA'], interfaceName="getUserToken")

        self.assertEqual(getUserTokenRes.status_code, userData['status_code_200'])
        self.tokenOA = json.loads(getUserTokenRes.text)['accessToken']

        '''登录OA成功'''
        self.headerOA = {'content-type': 'application/json', 'Accept': 'application/json',
                         'Authorization': 'Bearer ' + str(self.tokenOA)}

    def test_Commission(self):
        # '''1. 1/2星会员没有服务费，验证3/4/5星会员服务费返佣正确,服务费明细正确'''
        # FollowStar服务费明细，默认返回
        # pageIndex:1
        pageIndex = '1'
        # pageSize
        pageSize = '20'
        GetCommissionLogPageRES = FollowStar.GetTeamInfoPage(
            userData['hostPyramid']+userDataFollowStar['GetCommissionLogPage_url']+'?pageIndex='+pageIndex
            +'&pageSize='+pageSize,userData['headers'], interfaceName='GetCommissionLogPage')
        # print(GetCommissionLogPageRES.text)
        self.assertEqual(GetCommissionLogPageRES.status_code, userData['status_code_200'])
        # 提取明细里第一笔订单服务费
        self.AmountNum = json.loads(GetCommissionLogPageRES.text)['data']['List'][0]['AmountNum']
        # 提取明细里第一笔订单号
        self.OrderNo = json.loads(GetCommissionLogPageRES.text)['data']['List'][0]['OrderNo']
        self.LogId = json.loads(GetCommissionLogPageRES.text)['data']['List'][0]['LogId']
        # print(self.OrderNo)
        # 查询MySQL commissionlog表里该会员的最新一笔返佣
        selectOrderNoSql = 'SELECT Amount,OrderNo FROM commissionlog where ToUserId='+str(self.userId)+' ORDER BY CreateTime DESC LIMIT 1'
        selectOrderNoRow = MysqlDBOperation.OperationMysqlDB.operationPyramidDB(selectOrderNoSql)
        # print(selectOrderNoRow)
        # 验证服务费明细--服务费金额是否一致
        # self.assertEqual(self.AmountNum, selectOrderNoRow["Amount"],"服务费金额不一致")
        # 验证服务费明细--订单号是否一致
        self.assertEqual(self.OrderNo, selectOrderNoRow["OrderNo"],"订单号不一致")

        # '''2. 我的服务费--数据总览，验证服务费总额、余额、已提取、审核中的金额正确'''
        GetMyCommissionSummaryRES = FollowStar.GetMyCommissionSummary(userData['hostPyramid']+userDataFollowStar['GetMyCommissionSummary_url'],
                                                   userData['headers'],interfaceName='GetMyCommissionSummary')
        self.assertEqual(GetMyCommissionSummaryRES.status_code, userData['status_code_200'])
        # 会员服务费
        self.Commissions = json.loads(GetMyCommissionSummaryRES.text)['data']['Commissions']
        # print(self.Commissions)
        # 审核中
        self.Auditings = json.loads(GetMyCommissionSummaryRES.text)['data']['Auditings']
        # print(self.Auditings)
        # 已提取
        self.Withdrews = json.loads(GetMyCommissionSummaryRES.text)['data']['Withdrews']
        # print(self.Withdrews)
        # 余额
        self.Balances = json.loads(GetMyCommissionSummaryRES.text)['data']['Balances']
        # print(self.Balances)
        # 断言余额=会员服务费-已提取-审核中
        Balances1 = float('%.2f' %(self.Commissions-self.Withdrews-self.Auditings))
        # print(Balances1)
        self.assertEqual(self.Balances, Balances1, "余额不一致")


        # ''3. '验证提取服务费功能，审核中-审核通过-已打款-打款失败'''
        # web端提取$100服务费
        # amount：100，服务费最低提取金额为$100
        datas = {"amount": 100}
        ApplyingCommissionWithdrawRES = FollowStar.ApplyingCommissionWithdraw(userData['hostPyramid']+userDataFollowStar['ApplyingCommissionWithdraw_url'],
                                                   userData['headers'], datas, interfaceName='ApplyingCommissionWithdraw')
        self.assertEqual(ApplyingCommissionWithdrawRES.status_code, userData['status_code_200'])

        # amount:30，服务费最低提取金额为$100
        datas = {"amount": 30}
        ApplyingCommissionWithdrawRES = FollowStar.ApplyingCommissionWithdraw(userData['hostPyramid']+userDataFollowStar['ApplyingCommissionWithdraw_url'],
                                                   userData['headers'], datas, interfaceName='ApplyingCommissionWithdraw')
        self.assertEqual(json.loads(ApplyingCommissionWithdrawRES.text)["message"], "commission withdraw fail")

        time.sleep(3)
        # 4. FollowStar服务费提取记录明细
        # pageIndex:1
        pageIndex = '1'
        # pageSize
        pageSize = '20'
        GetCommissionWithdrawRecordRES = FollowStar.GetCommissionWithdrawRecord(
            userData['hostPyramid']+userDataFollowStar['GetCommissionWithdrawRecord_url']+'?pageIndex='+pageIndex
            +'&pageSize='+pageSize,userData['headers'], interfaceName='GetCommissionWithdrawRecord')
        # print(GetCommissionWithdrawRecordRES.text)
        self.assertEqual(GetCommissionWithdrawRecordRES.status_code, userData['status_code_200'])
        # 验证服务费提取记录，最新提取服务费金额
        self.AmountNum = json.loads(GetCommissionWithdrawRecordRES.text)['data']['List'][0]['AmountNum']
        # 验证服务费提取记录，最新提取服务费LogId
        self.LogId = json.loads(GetCommissionWithdrawRecordRES.text)['data']['List'][0]['LogId']
        # # 验证服务费提取记录 第一条审核状态：审核中
        # self.StateStr = json.loads(GetCommissionWithdrawRecordRES.text)['data']['List'][0]['StateStr']
        # 查询MySQL withdrawlog表里最新一笔服务费提取记录
        selectWithdrawSql = 'SELECT DollarAmount,WithdrawNo FROM withdrawlog where UserId='+str(self.userId)+' ORDER BY CreateTime DESC LIMIT 1'
        selectWithdrawRow = MysqlDBOperation.OperationMysqlDB.operationPyramidDB(selectWithdrawSql)

        # print(selectOrderNoRow)
        # 验证服务费提取记录--申请金额是否一致
        self.assertEqual(self.AmountNum, float(selectWithdrawRow["DollarAmount"]), "申请金额不一致")

        # 5. OA审核服务费，审核中-审核通过-已打款-打款失败
        #设置汇率为6.55
        datas = {'ExchangeRate': "6.55"}
        addExchangeRateRES = FollowStar.addExchangeRate(userData['hostNameOA']+commissionsData['addExchangeRate_url'], self.headerOA, datas, printLogs=0)
        self.assertEqual(addExchangeRateRES.status_code, userData['status_code_200'])
        # 获取OA服务费审核的数据列表
        # {"auditState":"","searchType":2,"searchValue":"","pageIndex":1,"pageSize":10,"total":178}
        datas={'pageIndex': '1', 'pageSize': '10', 'auditState': 1}
        GetCommissionListRES = FollowStar.GetCommissionList(userData['hostNameOA'] + userDataFollowStar['GetCommissionList_url'], self.headerOA, datas, printLogs=0)
        self.assertEqual(GetCommissionListRES.status_code, userData['status_code_200'])
        # print(json.loads(GetCommissionListRES.text)['Items'])
        # 获取服务费审核的数据列表审核状态
        self.StateStr = json.loads(GetCommissionListRES.text)['Items'][0]['StateStr']
        self.State = json.loads(GetCommissionListRES.text)['Items'][0]['State']
        # 获取服务费审核的数据列表订单号
        self.WithdrawNo = json.loads(GetCommissionListRES.text)['Items'][0]['WithdrawNo']
        # 验证服务费提取记录，最新提取订单号是否一致
        self.assertEqual(self.WithdrawNo, selectWithdrawRow["WithdrawNo"], "申请订单号不一致")
        # 获取OA今日汇率
        todayExchangeRateRES = FollowStar.getTodayExchangeRate(userData['hostNameOA']+commissionsData['getTodayExchangeRate_url'],self.headerOA,printLogs=0)
        self.assertEqual(todayExchangeRateRES.status_code, webAPIData['status_code_200'])
        # 审核中的订单--审核通过
        # {"auditStateCmd":2,"auditAmount":100,"remark":"","logId":182,"Amount":100,"UserID":169190}
        datas= {"auditStateCmd":2, "auditAmount":self.AmountNum, "remark":"test","logId":self.LogId,"Amount":self.AmountNum, "UserID":self.userId}
        AuditingCommissionRES = FollowStar.AuditingCommission(userData['hostNameOA']+userDataFollowStar['AuditingCommission_url'],
                                                              self.headerOA, datas, interfaceName='AuditingCommission')
        self.assertEqual(AuditingCommissionRES.status_code, webAPIData['status_code_200'])

        # 审核通过的订单--已打款
        datas= {"auditStateCmd":4,"remark":"test","auditAmount":self.AmountNum,"logId":self.LogId,"Amount":self.AmountNum, "UserID":self.userId}
        AuditingCommissionPayMoneyRES = FollowStar.AuditingCommissionPayMoney(userData['hostNameOA']+userDataFollowStar['AuditingCommissionPayMoney_url'],
                                                                              self.headerOA, datas, interfaceName='AuditingCommissionPayMoney')
        self.assertEqual(AuditingCommissionPayMoneyRES.status_code, webAPIData['status_code_200'])
        # 打款之后，对比未提取时，服务费金额（余额、已提取）会变化
        GetMyCommissionSummaryRES = FollowStar.GetMyCommissionSummary(userData['hostPyramid']+userDataFollowStar['GetMyCommissionSummary_url'],
                                                   userData['headers'],interfaceName='GetMyCommissionSummary')
        self.assertEqual(GetMyCommissionSummaryRES.status_code, userData['status_code_200'])
        # 断言会员服务费不变
        Commissions = json.loads(GetMyCommissionSummaryRES.text)['data']['Commissions']
        # print(Commissions)
        self.assertEqual(Commissions, self.Commissions, "会员服务费不一致")
        # 审核中
        Auditings = json.loads(GetMyCommissionSummaryRES.text)['data']['Auditings']
        # print(Auditings)
        self.assertEqual(Auditings, self.Auditings, "审核中不一致")
        # 已提取
        Withdrews = json.loads(GetMyCommissionSummaryRES.text)['data']['Withdrews']
        # print(Withdrews)
        self.assertEqual(Withdrews, self.Withdrews+self.AmountNum, "已提取不一致")
        # 余额
        Balances = json.loads(GetMyCommissionSummaryRES.text)['data']['Balances']
        # print(Balances)
        self.assertEqual(Balances, float('%.2f' %(self.Balances-self.AmountNum)), "会员余额不一致")
        # 断言余额=会员服务费-已提取-审核中
        Balances_1 = float('%.2f' %(Commissions-Withdrews-Auditings))
        # print(Balances_1)
        self.assertEqual(Balances, Balances_1, "已打款余额不一致")

        # 已打款-打款失败
        datas= {"auditStateCmd":5,"remark":"test","auditAmount":self.AmountNum,"logId":self.LogId,"Amount":self.AmountNum, "UserID":self.userId}
        AuditingCommissionPayMoneyRES = FollowStar.AuditingCommissionPayMoney(userData['hostNameOA']+userDataFollowStar['AuditingCommissionPayMoney_url'],
                                                                              self.headerOA, datas, interfaceName='AuditingCommissionPayMoney')
        self.assertEqual(AuditingCommissionPayMoneyRES.status_code, webAPIData['status_code_200'])

        # '''6. OA审核服务费，审核中-审核失败'''
        # web端提取$100服务费
        # amount，服务费最低提取金额为$100
        datas = {"amount": 100}
        ApplyingCommissionWithdrawRES = FollowStar.ApplyingCommissionWithdraw(userData['hostPyramid']+userDataFollowStar['ApplyingCommissionWithdraw_url'],
                                                   userData['headers'], datas, interfaceName='ApplyingCommissionWithdraw')
        self.assertEqual(ApplyingCommissionWithdrawRES.status_code, userData['status_code_200'])
        # FollowStar服务费提取记录明细
        # pageIndex:1
        pageIndex = '1'
        # pageSize
        pageSize = '20'
        GetCommissionWithdrawRecordRES = FollowStar.GetCommissionWithdrawRecord(
            userData['hostPyramid']+userDataFollowStar['GetCommissionWithdrawRecord_url']+'?pageIndex='+pageIndex
            +'&pageSize='+pageSize,userData['headers'], interfaceName='GetCommissionWithdrawRecord')
        # print(GetCommissionWithdrawRecordRES.text)
        self.assertEqual(GetCommissionWithdrawRecordRES.status_code, userData['status_code_200'])
        # 验证服务费提取记录，最新提取服务费金额
        self.AmountNum_1 = json.loads(GetCommissionWithdrawRecordRES.text)['data']['List'][0]['AmountNum']
        # 验证服务费提取记录，最新提取服务费LogId
        self.LogId_1 = json.loads(GetCommissionWithdrawRecordRES.text)['data']['List'][0]['LogId']

        # 审核中的订单--审核失败
        # {"auditStateCmd":1,"remark":"","auditAmount":null,"logId":177,"Amount":100,"UserID":169190}
        datas= {"auditStateCmd":1, "auditAmount":None, "remark":"test","logId":self.LogId_1,"Amount":self.AmountNum_1, "UserID":self.userId}
        AuditingCommissionRES = FollowStar.AuditingCommission(userData['hostNameOA']+userDataFollowStar['AuditingCommission_url'],
                                                              self.headerOA, datas, interfaceName='AuditingCommission')
        self.assertEqual(AuditingCommissionRES.status_code, webAPIData['status_code_200'])
        # FollowStar我的服务费，审核失败对比未提取时，服务费金额--余额不变
        GetMyCommissionSummaryRES = FollowStar.GetMyCommissionSummary(userData['hostPyramid']+userDataFollowStar['GetMyCommissionSummary_url'],
                                                   userData['headers'],interfaceName='GetMyCommissionSummary')
        self.assertEqual(GetMyCommissionSummaryRES.status_code, userData['status_code_200'])
        # 断言会员服务费不变
        Balances_1 = json.loads(GetMyCommissionSummaryRES.text)['data']['Balances']
        self.assertEqual(Balances_1, self.Balances, "OA审核失败余额不一致")

    def tearDown(self):
        # 退出
        FollowStarLogoutRES = FollowStar.FollowStarLogout(
            userData['hostPyramid'] + userDataFollowStar['FollowStarLogout_url'],
            userData['headers'], interfaceName='FollowStarLogout')
        self.assertEqual(FollowStarLogoutRES.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()
