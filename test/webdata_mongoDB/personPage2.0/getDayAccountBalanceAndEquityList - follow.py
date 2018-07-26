#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getDayAccountBalanceAndEquityList
# 用例标题: 获取跟随者净值余额图表数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
#   1.获取跟随者净值余额图表数据对比MongoDB数据
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180516
#=========================================================
import sys,unittest,json
import time,os
import datetime
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,Statistic,Follow,Datastatistic
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable
from pymongo import MongoClient

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()
followData = FMCommon.loadFollowYML()
datastatisticData = FMCommon.loadDatastatisticYML()

class DayAccountBalanceAndEquityList(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #入参
        self.userID = '18907'
        self.AccountIndex = 2
        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        mongoDB = FMCommon.mongoDB_operater_data(host=mongoUrl, port = statisticData["mongo_port"])
        #获取MT4账号
        self.mt4Account = Statistic.getMt4Account(userID=str(self.userID),accountIndex=str(self.AccountIndex))
        print(self.mt4Account)
        '''获取个人展示页的净值余额图表数据'''
        balanceAndEquity = Datastatistic.getDayAccountBalanceAndEquityList(webAPIData['hostName'] + datastatisticData['getDayAccountBalanceAndEquityList_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + datastatisticData["getDayAccountBalanceAndEquityList_url2"],printLogs=0)        
        # self.assertEqual(balanceAndEquity.status_code, webAPIData['status_code_200'])
        
        self.dateList = []
        self.depositList = []
        self.withdrawList = []
        for self.item in json.loads(balanceAndEquity.text)["data"]["DepositAndWithdrawList"]:
            self.dateList.append(self.item["Date"])
            self.depositList.append(self.item["Deposit"])
            self.withdrawList.append(self.item["Withdraw"])
            timeStamp = int(self.item["Date"])
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
            print(otherStyleTime)

            for i in mongoDB.datastatistic.mg_result_day.find({"login":str(self.mt4Account),"close_date":str(otherStyleTime)}):
                self.mongoList_day = {}
                for key in statisticData["mongoKeyListAll"]:
                    try:
                        value = i[key]
                    except KeyError:
                        value = statisticData["keyErr"]
                    self.mongoList_day[key]=value

            table = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","Date","出金","入金"])

            try:
                table.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleTime,self.mongoList_day["deposit"],self.mongoList_day["withdraw"]])
                table.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleTime,self.item["Deposit"],self.item["Withdraw"]])
                table.add_row(["","","","","","",""])
                
            finally:
                table.reversesort = True
                print(table)

    def test_1_ProfitOrders(self):           
        #出金
        self.assertAlmostEqual(self.mongoList_day["deposit"],float(self.item["Deposit"]),delta = 0.01)

    def test_2_AvgProfitMoney(self): 
        #入金
        self.assertAlmostEqual(self.mongoList_day["withdraw"],float(self.item["Withdraw"]),delta = 0.01)


    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

