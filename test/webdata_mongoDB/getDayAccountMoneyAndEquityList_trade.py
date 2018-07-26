#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getDayAccountMoneyAndEquityList

# 用例标题: 获取收益图表数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
#   1.获取收益图表数据对比MongoDB数据
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

class DayAccountMoneyAndEquityList(unittest.TestCase):
    def setUp(self):
        #入参
        self.userID = '132316'
        self.AccountIndex = 5

        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        mongoDB = FMCommon.mongoDB_operater_data(host=mongoUrl, port = statisticData["mongo_port"])
        #获取MT4账号
        self.mt4Account = Statistic.getMt4Account(userID=str(self.userID),accountIndex=str(self.AccountIndex))
        print(self.mt4Account)
        '''获取个人展示页的收益图表数据'''
        # accountRoi = Datastatistic.getAccountRoi(webAPIData['hostName'] + followData['getStatisticsOfAccount_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + followData["getStatisticsOfAccount_url1"],printLogs=0)
        # MoneyAndEquity = Datastatistic.getDayAccountMoneyAndEquityList("http://dev.fmfe.com/api//v2/trade/77141_1/equity/income")
        MoneyAndEquity = Datastatistic.getDayAccountMoneyAndEquityList(webAPIData['hostName'] + datastatisticData['getDayAccountMoneyAndEquityList_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + datastatisticData["getDayAccountMoneyAndEquityList_url2"] + "?category=day",printLogs=0)
        self.assertEqual(MoneyAndEquity.status_code, webAPIData['status_code_200'])
        
        self.dateList = []
        self.daymoneyList = []
        for self.item in json.loads(MoneyAndEquity.text)["data"]["MoneyList"]:
            self.dateList.append(self.item["Date"])
            self.daymoneyList.append(self.item["Money"])
            timeStamp = int(self.item["Date"])
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
            for i in mongoDB.datastatistic_1_16.mg_result_day.find({"login":str(self.mt4Account),"close_date":str(otherStyleTime)}):
                
                self.mongoList_day = {}
                for key in statisticData["mongoKeyListAll"]:
                    try:
                        value = i[key]
                        
                    except KeyError:
                        value = statisticData["keyErr"]
                    self.mongoList_day[key]=value
                        
            table = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","日期","每日收益","已平仓收益"])

            try:
                table.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleTime,self.mongoList_day["money_close"],self.mongoList_day["money_close_asum"]])
                table.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleTime,self.item["Money"],self.item["TotalMoney"]])
                table.add_row(["","","","","","",""])
                
            finally:
                table.reversesort = True
                print(table)



    def test_1_Daymoney(self):           
        #每日收益
        self.assertAlmostEqual(self.mongoList_day["money_close"],float(self.item["Money"]),delta = 0.01)

    def test_2_Monthmoney(self): 
        #已平仓收益
        self.assertAlmostEqual(self.mongoList_day["money_close_asum"],float(self.item["TotalMoney"]),delta = 0.01)
    
    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

