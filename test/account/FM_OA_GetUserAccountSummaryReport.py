#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: OA Account -GetUserAccountSummaryReport

import sys,unittest,json,requests

sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/common")

import FMCommon,Account,Auth

userData = FMCommon.loadWebAPIYML()
userDataAccountUrl=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()

class GetUserAccountSummaryReport(unittest.TestCase):
        def setUp(self):
            'start!'
            # '''登录OA'''
            # loginOAUrl=userData['hostNameOA']+userDataAuthUrl['loginOA_url']
            # loginOARes=Auth.loginOA(loginOAUrl,headers=userData['headersOA'],username=userData['usernameOA'],password=userData['passwordOA'])
            #
            # self.assertEqual(loginOARes.status_code,userData['status_code_200'])
            # self.tokenOA=json.loads(loginOARes.text)['Result']['Token']

            # OA登录
            getUserTokenRes = Auth.getUserToken(
                userData['hostNameSwagger'] + userDataAuthUrl['loginOA_url'] + userData['oaClientId']
                + "&userName=" + userData['oaUsername'] + "&password=" + userData['oapassword'],
                userData['headersOA'], interfaceName="getUserToken")

            self.assertEqual(getUserTokenRes.status_code, userData['status_code_200'])
            self.tokenOA = json.loads(getUserTokenRes.text)['accessToken']

            '''登录OA成功'''
            self.headerOA={'content-type': 'application/json', 'Accept' : 'application/json','Authorization': 'Bearer ' + str(self.tokenOA)}

        '''筛选账户总览中开户类型'''
        def test_getUserAccountSummaryReportOfAccountType_001(self):
            datas={'AccountType': userData['getUserAccountSummaryReportAccountType_1'],'pageIndex': userData['getUserAccountSummaryReportPageIndex'],'pageSize': userData['getUserAccountSummaryReportPageSize'],'orderBy': userData['getUserAccountSummaryReport_Orderby']}
            url=userData['hostNameOA']+userDataAccountUrl['getUserAccountSummaryReport_url']

            userAccSummaryRepRes=Account.getUserAccountSummaryReport(url,self.headerOA,datas,printLogs=0)
            if userAccSummaryRepRes:
                self.assertEqual(userAccSummaryRepRes.status_code,userData['status_code_200'],'获取账户总览失败！')
                userAccSummaryRepList = json.loads( userAccSummaryRepRes.text)['Items']
                if len(userAccSummaryRepList):
                    for i in range(len(userAccSummaryRepList)):
                         self.assertEqual(userAccSummaryRepList[i]['AccountType'], userData['getUserAccountSummaryReportAccountType_1'],
                                     '筛选账户总览中开户类型为API的数据错误！')

        '''筛选账户总览中手机号的数据'''
        def test_getUserAccountSummaryReportOfAccountMobile_002(self):
            datas={'AccountMobile': userData['account'],'pageIndex': userData['getUserAccountSummaryReportPageIndex'],'pageSize': userData['getUserAccountSummaryReportPageSize'],'orderBy': userData['getUserAccountSummaryReport_Orderby']}
            url=userData['hostNameOA']+userDataAccountUrl['getUserAccountSummaryReport_url']

            userAccSummaryRepRes=Account.getUserAccountSummaryReport(url,self.headerOA,datas,printLogs=0)
            if userAccSummaryRepRes:
                self.assertEqual(userAccSummaryRepRes.status_code,userData['status_code_200'],'获取账户总览失败！')

                userAccSummaryRepList = json.loads(userAccSummaryRepRes.text)['Items']
                if len(userAccSummaryRepList):
                    for i in range(len(userAccSummaryRepList)):
                         self.assertEqual(userAccSummaryRepList[i]['AccountMobile'], '180****8805',
                                     '筛选账户总览中手机号的数据错误！')

        '''筛选OA账户总览中FM账户号的数据'''
        def test_getUserAccountSummaryReportOfFMaccount_003(self):
            datas={'FMaccount': userData['FMaccount'],'pageIndex': userData['getUserAccountSummaryReportPageIndex'],'pageSize': userData['getUserAccountSummaryReportPageSize'],'orderBy': userData['getUserAccountSummaryReport_Orderby']}
            url=userData['hostNameOA']+userDataAccountUrl['getUserAccountSummaryReport_url']

            userAccSummaryRepRes=Account.getUserAccountSummaryReport(url,self.headerOA,datas,printLogs=0)
            if userAccSummaryRepRes:
                self.assertEqual(userAccSummaryRepRes.status_code,userData['status_code_200'],'获取账户总览失败！')

                userAccSummaryRepList = json.loads( userAccSummaryRepRes.text)['Items']
                if len(userAccSummaryRepList):
                    for i in range(len(userAccSummaryRepList)):
                         self.assertEqual(userAccSummaryRepList[i]['FMaccount'], userData['FMaccount'],
                                     '筛选账户总览中FM账户号的数据错误！')
        def tearDown(self):
            'end!'
            # gc.collect()
            # loginOutOAUrl=userData['hostNameOA']+userDataAuthUrl['loginOutOA_url']
            # loginOutOARes=Auth.loginOut(loginOutOAUrl,headers=self.headerOA)
            # '''退出OA成功'''
            # self.assertEqual(loginOutOARes.status_code,userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()