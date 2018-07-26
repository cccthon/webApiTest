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
sys.path.append("../../lib/statistic")
import FMCommon,Common,PersonalPage,Statistic,Auth
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
personalPageData = FMCommon.loadPersonalPageYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()

class AccountsOfUser(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_1_getAccountsOfUser(self):
        '''获取用户的交易账号列表'''
        # userID = "148171" #交易员
        userID = "148181" #跟随者
        url = webAPIData['hostName']+personalPageData['getAccountsOfUser_url1'] + userID + personalPageData['getAccountsOfUser_url2']
        accountList=PersonalPage.getAccountsOfUser(url,headers=webAPIData['headers'],printLogs=1)
        #请求成功 返回 200
        self.assertEqual(accountList.status_code,webAPIData['status_code_200'])
        table = PrettyTable(["预期/实际","Id","AccountIndex","BrokerId","mt4Account","AccountType","净值利润因子/跟随获利点数","收益率","跟随周期"])
        try:
            for item in json.loads(accountList.text)["data"]["accounts"]:
                mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountIndex"]))
                userType  = Statistic.userType(mt4Account=mt4Account)
                factorProfitEquity = Statistic.factorProfitEquity(mt4Account=mt4Account,brokerID=item["BrokerId"])
                pointOfCfClose = Statistic.pointOfCfClose(mt4Account=mt4Account,brokerID=item["BrokerId"])
                rateProfit = Statistic.rateProfit(mt4Account=mt4Account,brokerID=item["BrokerId"])
                tradePeriod = Statistic.tradePeriod(mt4Account=mt4Account,brokerID=item["BrokerId"])
                if userType == 1:
                    table.add_row(["预期结果",item["Id"],item["AccountIndex"],item["BrokerId"],mt4Account,item["AccountType"],factorProfitEquity,rateProfit,tradePeriod])
                    table.add_row(["实际结果",item["Id"],item["AccountIndex"],item["BrokerId"],mt4Account,item["AccountType"],item["ProfitFactorOrPoint"],item["ROI"]*100,item["Weeks"]])
                    table.add_row(["","","","","","","","",""])
                    #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
                    self.assertAlmostEqual(factorProfitEquity,float(item["ProfitFactorOrPoint"]),delta = 2)
                    self.assertAlmostEqual(rateProfit,float(item["ROI"]*100),delta = 1000000)
                    self.assertAlmostEqual(tradePeriod,float(item["Weeks"]),delta = 1000000)
                elif userType == 2:
                    table.add_row(["预期结果",item["Id"],item["AccountIndex"],item["BrokerId"],mt4Account,item["AccountType"],pointOfCfClose,rateProfit,tradePeriod])
                    table.add_row(["实际结果",item["Id"],item["AccountIndex"],item["BrokerId"],mt4Account,item["AccountType"],item["ProfitFactorOrPoint"],item["ROI"]*100,item["Weeks"]])
                    table.add_row(["","","","","","","","",""])
                    #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
                    self.assertAlmostEqual(pointOfCfClose,float(item["ProfitFactorOrPoint"]),delta = 200)
                    self.assertAlmostEqual(rateProfit,float(item["ROI"]*100),delta = 10000)
                    self.assertAlmostEqual(tradePeriod,item["Weeks"],delta = 10000)
        finally:
            table.reversesort = True
            print(table)
   
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

