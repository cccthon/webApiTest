#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getMonthAnalysisReport

# 用例标题: 获取月分析报告数据月统计数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
#   1.获取月分析报告月统计数据对比MongoDB数据
#   1.1 月收益金额
#   1.2 月盈亏点数
#   1.3 月标准手
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180518
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
userData = FMCommon.loadWebAPIYML()

class MonthAnalysisReport(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #入参
        self.userID = '132316'
        print(self.userID)
        self.AccountIndex = 4
        #连接beta环境的MongoDB数据
        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        mongoDB = FMCommon.mongoDB_operater_data(host=mongoUrl, port = statisticData["mongo_port"])
        #获取MT4账号
        self.mt4Account = Statistic.getMt4Account(userID=str(self.userID),accountIndex=str(self.AccountIndex))
        #获取BrokerId
        self.brokerId = Statistic.BrokerId(userID=str(self.userID),accountIndex=str(self.AccountIndex))
        print(self.brokerId)
        '''获取个人展示页的月分析报告数据'''
        # accountRoi = Datastatistic.getAccountRoi(webAPIData['hostName'] + followData['getStatisticsOfAccount_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + followData["getStatisticsOfAccount_url1"],printLogs=0)
        # self.monthAnalysisReport = Datastatistic.getMonthAnalysisReport("http://dev.fmfe.com/api/v2/trade/77141_1/month/analysis/report")
        self.monthAnalysisReport = Datastatistic.getMonthAnalysisReport(webAPIData['hostName'] + datastatisticData['getMonthAnalysisReport_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + datastatisticData["getMonthAnalysisReport_url2"],printLogs=0)
        
        self.monthList = []
        self.moneyList = []
        self.pipsList = []
        self.standardLotslList = []
        for self.item in json.loads(self.monthAnalysisReport.text)["data"]["MonthDataList"]:
            #遍历返回所有的月份数据
            self.monthList.append(self.item["Month"])
            #遍历返回所有的累计收益数据
            self.moneyList.append(self.item["Money"])
            #遍历返回所有的盈亏点数数据
            self.pipsList.append(self.item["Pips"])
            #遍历返回所有的标准手数据
            self.standardLotslList.append(self.item["StandardLots"])
            timeStamp = int(self.item["Month"])
            timeArray = time.localtime(timeStamp)
            otherStyleMonth = time.strftime("%Y-%m", timeArray)
            print(otherStyleMonth)
            self.money_closeList = []
            self.point_closeList = []
            self.standardlots_closeList = []
            for i in mongoDB.datastatistic.mg_result_month.find({"login":str(self.mt4Account),"close_month":otherStyleMonth}):
                # print(i)
                self.mongoList = {}
                for key in statisticData["mongoKeyListAll"]:
                    try:
                        value = i[key]
                    except KeyError:
                        value = statisticData["keyErr"]
                    self.mongoList[key]=value
                    #获取MongoDB的不同月份的累计收益
            # print(self.mongoList["money_close"])
            # print(self.mongoList["factor_profit_equity"])
            # print(self.mongoList["standardlots_close"])

                self.money_closeList.append(self.mongoList["money_close"])
                #获取MongoDB的不同月份的盈亏点数
                self.point_closeList.append(self.mongoList["factor_profit_equity"])
                #获取MongoDB的不同月份的标准手
                self.standardlots_closeList.append(self.mongoList["standardlots_close"])

            table = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","月份","收益金额","收益点数","交易量(标准手)"])

            try: 
                table.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleMonth,self.mongoList["money_close"],self.mongoList["point_close"],self.mongoList["standardlots_close"]])
                table.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleMonth,self.item["Money"],self.item["Pips"],self.item["StandardLots"]])
                table.add_row(["","","","","","","",""])
                
            finally:
                table.reversesort = True
                print(table)

    def setUp(self):
        pass

    def test_1_AvgProfitMoney(self): 
        #收益金额
        self.assertAlmostEqual(self.mongoList["money_close"],float(self.item["Money"]),delta = 0.01)

    def test_2_AvgProfitMoney(self): 
        #收益点数
        self.assertAlmostEqual(self.mongoList["point_close"],float(self.item["Pips"]),delta = 0.01)

    def test_3_MaxLossPips(self):     
        #交易量(标准手)
        self.assertAlmostEqual(self.mongoList["standardlots_close"],float(self.item["StandardLots"]),delta = 0.01)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

 
if __name__ == '__main__':
    unittest.main()

   
