#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getMonthAnalysisReport

# 用例标题: 获取月分析报告月品种数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
# 1.获取月分析报告月品种数据对比MongoDB数据
# 1.1 不同品种的标准手
# 1.2 不同品种的交易笔数
# 1.3 不同品种的平均持仓时间(分钟)
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

class HotTrader(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #入参
        self.userID = '84524'
        self.AccountIndex = 3
        #连接beta环境的MongoDB
        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        mongoDB = FMCommon.mongoDB_operater_data(host=mongoUrl, port = statisticData["mongo_port"])
        #获取MT4账号
        self.mt4Account = Statistic.getMt4Account(userID=str(self.userID),accountIndex=str(self.AccountIndex))
        print(self.mt4Account)
        '''获取个人展示页的月分析报告数据'''
        # accountRoi = Datastatistic.getAccountRoi(webAPIData['hostName'] + followData['getStatisticsOfAccount_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + followData["getStatisticsOfAccount_url1"],printLogs=0)?startTime=1514736000
        # monthAnalysisReport = Datastatistic.getMonthAnalysisReport("http://dev.fmfe.com/api/v2/trade/77141_1/month/analysis/report")
        # self.monthAnalysisReport = Datastatistic.getMonthAnalysisReport(webAPIData['hostName'] + datastatisticData['getMonthAnalysisReport_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + datastatisticData["getMonthAnalysisReport_url2"],params="startTime=1514736000",printLogs=0)
        self.monthAnalysisReport = Datastatistic.getMonthAnalysisReport("https://alibetawww.followme.com/api/v2/trade/84524_3/symbol/month/analysis/report?startTime=1514736000",printLogs=0)

        # self.assertEqual(monthAnalysisReport.status_code, webAPIData['status_code_200'])
        self.monthList = []
        self.standardSymbolList = []
        self.standardLotsList = []
        self.factorProfitEquityList = []
        self.timePossessionAverageList = []

        for self.item in json.loads(self.monthAnalysisReport.text)["data"]["SymbolMonthDataList"]:
            #遍历返回数据的所有月份
            self.monthList.append(self.item["Month"])
            #遍历返回数据的所有标准品种名
            self.standardSymbolList.append(self.item["StandardSymbol"])
            #遍历返回数据的所有标准手
            self.standardLotsList.append(self.item["StandardLots"])
            #遍历返回数据的所有交易笔数
            self.factorProfitEquityList.append(self.item["Orders"])
            #遍历返回数据的所有平均持仓时间(分钟)
            self.timePossessionAverageList.append(self.item["TimePossessionAverage"])
            #转换时间戳，把时间戳转换为时间
            timeStamp = int(self.item["Month"])
            timeArray = time.localtime(timeStamp)
            otherStyleMonth = time.strftime("%Y-%m", timeArray)
            print(otherStyleMonth)
            self.standardlots_closeMongoList = []
            self.factor_profit_equityMongoList = []
            self.time_possession_avgMongoList = []
            # for i in mongoDB.fm.mg_result_symall.find({"_id":str(self.mt4Account) + "_" + str(self.brokerid) + str(otherStyleMonth) + str(item["StandardSymbol"])}):
            for i in mongoDB.datastatistic.mg_result_symmonth.find({"login":str(self.mt4Account),"close_month":otherStyleMonth,"standardsymbol":str(self.item["StandardSymbol"])}):
                self.mongoList = {}
                for key in statisticData["mongoKeyListAll"]:
                    try:
                        value = i[key]
                    except KeyError:
                        value = statisticData["keyErr"]
                    self.mongoList[key]=value

                # 获取MongoDB的不同品种的标准手
                self.standardlots_closeMongoList.append(self.mongoList["standardlots_close"])
                print(self.standardlots_closeMongoList)
                #获取MongoDB的不同品种的交易笔数
                self.factor_profit_equityMongoList.append(self.mongoList["deal_close"])
                #获取MongoDB的不同品种的平均持仓时间(分钟)
                self.time_possession_avgMongoList.append(self.mongoList["time_possession_avg"])

                table = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","月份","标准品种名","标准手","交易笔数","平均持仓时间","做多平均持仓时间","做空平均持仓时间"])

                try: 
                    table.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleMonth,self.item["StandardSymbol"],self.mongoList["standardlots_close"],self.mongoList["deal_close"],self.mongoList["time_possession_avg"],self.mongoList["time_possession_long_avg"],self.mongoList["time_possession_short_avg"]])
                    table.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleMonth,self.item["StandardSymbol"],self.item["StandardLots"],self.item["Orders"],self.item["TimePossessionAverage"],self.item["TimePossessionLongAverage"],self.item["TimePossessionShortAverage"]])
                    table.add_row(["","","","","","","","","","",""])
                    
                finally:
                    table.reversesort = True
                    print(table)

    def setUp(self):
        pass
    def test_1_AvgProfitMoney(self): 
        #标准手
        self.assertAlmostEqual(self.mongoList["standardlots_close"],float(self.item["StandardLots"]),delta = 0.01)

    def test_2_AvgProfitMoney(self): 
        #交易笔数
        self.assertAlmostEqual(self.mongoList["deal_close"],float(self.item["Orders"]),delta = 0.01)
    
    def test_3_MaxLossPips(self):     
        #平均持仓时间
        self.assertAlmostEqual(self.mongoList["time_possession_avg"],float(self.item["TimePossessionAverage"]),delta = 0.01)

    
    

    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

