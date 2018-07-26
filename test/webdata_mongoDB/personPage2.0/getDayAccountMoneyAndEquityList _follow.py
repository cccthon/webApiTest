#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getDayAccountMoneyAndEquityList

# 用例标题: 获取跟随者收益图表数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
#   1.获取跟随者收益图表数据对比MongoDB数据
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180517
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

class DayAccountMoneyAndEquityList(unittest.TestCase):
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
        '''获取跟随者个人展示页的收益图表数据'''
        # accountRoi = Datastatistic.getAccountRoi(webAPIData['hostName'] + followData['getStatisticsOfAccount_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + followData["getStatisticsOfAccount_url1"],printLogs=0)
        # MoneyAndEquity = Datastatistic.getDayAccountMoneyAndEquityList("http://dev.fmfe.com/api//v2/trade/77141_1/equity/income")
        MoneyAndEquity = Datastatistic.getDayAccountMoneyAndEquityList(webAPIData['hostName'] + datastatisticData['getDayAccountMoneyAndEquityList_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + datastatisticData["getDayAccountMoneyAndEquityList_url2"],printLogs=1)
        
        # self.assertEqual(MoneyAndEquity.status_code, webAPIData['status_code_200'])
        
        self.dateList = []
        self.totalMoneyList = []
        self.totalSelfMoneyList= []
        self.totalFollowMoneyList = []
        for self.item in json.loads(MoneyAndEquity.text)["data"]["MoneyList"]:
            self.dateList.append(self.item["Date"])
            self.totalMoneyList.append(self.item["TotalMoney"])
            self.totalSelfMoneyList.append(self.item["TotalSelfMoney"])
            self.totalFollowMoneyList.append(self.item["TotalFollowMoney"])
            timeStamp = int(self.item["Date"])
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
            for i in mongoDB.datastatistic.mg_result_day.find({"login":str(self.mt4Account),"close_date":str(otherStyleTime)}):
                self.mongoList_day = {}
                for key in statisticData["mongoKeyListAll"]:
                    try:
                        value = i[key]
                    except KeyError:
                        value = statisticData["keyErr"]
                    self.mongoList_day[key]=value
            table = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","日期","总收益","自主收益","跟随收益"])

            try:
                table.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleTime,self.mongoList_day["money_close_asum"],self.mongoList_day["money_cs_asum"],self.mongoList_day["money_cf_asum"]])
                table.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleTime,self.item["TotalMoney"],self.item["TotalSelfMoney"],self.item["TotalFollowMoney"]])
                table.add_row(["","","","","","","",""])
                
            finally:
                table.reversesort = True
                print(table)



        self.monthList = []
        self.selfMoneyList = []
        self.followMoneyList = []
        for self.items in json.loads(MoneyAndEquity.text)["data"]["MonthMoneyList"]:
            self.monthList.append(self.items["Month"])
            self.selfMoneyList.append(self.items["SelfMoney"])
            self.followMoneyList.append(self.items["FollowMoney"])
            monthStamp = int(self.items["Month"])
            monthArray = time.localtime(monthStamp)
            otherStyleMonth = time.strftime("%Y-%m", monthArray)
            print(otherStyleMonth)

            for i in mongoDB.datastatistic.mg_result_month.find({"login":str(self.mt4Account),"close_month":str(otherStyleMonth)}):
                self.mongoList_month = {}
                for key in statisticData["mongoKeyListAll"]:
                    try:
                        value = i[key]
                    except KeyError:
                        value = statisticData["keyErr"]
                    self.mongoList_month[key]=value

            table = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","月份","月自主收益","月跟随收益","月自主收益点数","月跟随收益点数","月自主标准手","月跟随标准手"])

            try:
                table.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleMonth,self.mongoList_month["money_cs"],self.mongoList_month["money_cf"],self.mongoList_month["point_cs"],self.mongoList_month["point_cf"],self.mongoList_month["standardlots_cs"],self.mongoList_month["standardlots_cf"]])
                table.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleMonth,self.items["SelfMoney"],self.items["FollowMoney"],self.items["SelfPips"],self.items["FollowPips"],self.items["SelfStandardlots"],self.items["FollowStandardlots"]])
                table.add_row(["","","","","","","","","","",""])
                
            finally:
                table.reversesort = True
                print(table)

    def test_1_TotalMoney(self):           
        #总收益
        self.assertAlmostEqual(self.mongoList_day["money_close_asum"],float(self.item["TotalMoney"]),delta = 0.01)

    def test_2_TotalSelfMoney(self): 
        #自主收益
        self.assertAlmostEqual(self.mongoList_day["money_cs_asum"],float(self.item["TotalSelfMoney"]),delta = 0.01)

    def test_3_TotalFollowMoney(self):           
        #跟随收益
        self.assertAlmostEqual(self.mongoList_day["money_cf_asum"],float(self.item["TotalFollowMoney"]),delta = 0.01)

    def test_4_SelfMoney(self): 
        #月自主收益
        self.assertAlmostEqual(self.mongoList_month["money_cs"],float(self.items["SelfMoney"]),delta = 0.01)

    def test_5_FollowMoney(self):           
        #月跟随收益
        self.assertAlmostEqual(self.mongoList_month["money_cf"],float(self.items["FollowMoney"]),delta = 0.01)

    
    
    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

