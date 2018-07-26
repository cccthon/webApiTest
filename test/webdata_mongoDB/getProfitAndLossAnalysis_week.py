#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getProfitAndLossAnalysis_week

# 用例标题: 获取盈亏分析图表(周)数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
# 1.获取盈亏分析图表(周)数据对比MongoDB数据
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180521
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
        self.userID = '132316'
        self.AccountIndex = 4
        #连接beta环境的MongoDB
        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        mongoDB = FMCommon.mongoDB_operater_data(host=mongoUrl, port = statisticData["mongo_port"])
        #获取MT4账号
        self.mt4Account = Statistic.getMt4Account(userID=str(self.userID),accountIndex=str(self.AccountIndex))
        print(self.mt4Account)
        '''获取个人展示页的月分析报告数据'''
        
        self.profitAndLossAnalysis = Datastatistic.getProfitAndLossAnalysis(webAPIData['hostName'] + datastatisticData['getProfitAndLossAnalysis_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + datastatisticData["getProfitAndLossAnalysis_url2"],params="timeType=TimeTypeWeek",printLogs=0)
        
        # self.assertEqual(monthAnalysisReport.status_code, webAPIData['status_code_200'])
        self.weekList = []
        self.moneyList = []
        self.moneyProfitLongList = []
        self.moneyLossLongList = []
        self.moneyProfitShortList = []
        self.moneyLossShortList = []
        self.pipsList = []
        self.pipsProfitLongList = []
        self.pipsLossLongList = []
        self.pipsProfitShortList = []
        self.pipsLossShortList = []
        self.standardLotsLongList = []
        self.standardLotsShortList = []
        self.money_close_MongoList = []


        for self.item in json.loads(self.profitAndLossAnalysis.text)["data"]["HourAndWeekList"]:
            #遍历返回数据的所有周
            self.weekList.append(self.item["Week"])
            #遍历返回数据的所有收益
            self.moneyList.append(self.item["Money"])
            #遍历返回数据的所有做多盈利收益
            self.moneyProfitLongList.append(self.item["MoneyProfitLong"])
            #遍历返回数据的所有做多亏损收益
            self.moneyLossLongList.append(self.item["MoneyLossLong"])
            #遍历返回数据的所有做空盈利收益
            self.moneyProfitShortList.append(self.item["MoneyProfitShort"])
            #遍历返回数据的所有做空亏损收益
            self.moneyLossShortList.append(self.item["MoneyLossShort"])
            #遍历返回数据的所有点数
            self.pipsList.append(self.item["Pips"])
            #遍历返回数据的所有做多盈利点数
            self.pipsProfitLongList.append(self.item["PipsProfitLong"])
            #遍历返回数据的所有做多亏损点数
            self.pipsLossLongList.append(self.item["PipsLossLong"])
            #遍历返回数据的所有做空盈利点数
            self.pipsProfitShortList.append(self.item["PipsProfitShort"])
            #遍历返回数据的所有做空亏损点数
            self.pipsLossShortList.append(self.item["PipsLossShort"])
            #遍历返回数据的所有做多手数
            self.standardLotsLongList.append(self.item["StandardLotsLong"])
            #遍历返回数据的所有做空手数
            self.standardLotsShortList.append(self.item["StandardLotsShort"])
            # #转换时间戳，把时间戳转换为时间
            # timeStamp = int(self.item["Month"])
            # timeArray = time.localtime(timeStamp)
            # otherStyleMonth = time.strftime("%Y-%m", timeArray)
            # print(otherStyleMonth)
            self.money_close_MongoList = []
            self.money_profit_long_close_MongoList = []
            self.money_loss_long_close_MongoList = []
            self.money_profit_short_close_MongoList = []
            self.money_loss_short_close_MongoList = []
            self.money_loss_long_close_MongoList = []
            self.point_close_MongoList = []
            self.point_profit_long_close_MongoList = []
            self.point_loss_long_close_MongoList = []
            self.point_profit_short_close_MongoList = []
            self.point_loss_short_close_MongoList = []
            self.standardlots_long_close_MongoList = []
            self.standardlots_short_close_MongoList = []
            # for i in mongoDB.fm.mg_result_Week.find({"_id":str(self.mt4Account) + "_" + str(self.brokerid) + str(otherStyleMonth) + str(self.item["Week"])}):
            for i in mongoDB.datastatistic.mg_result_week.find({"login":str(self.mt4Account),"close_week":self.item["Week"]}):
                self.mongoList = {}
                for key in statisticData["mongoKeyListAll"]:
                    try:
                        value = i[key]
                    except KeyError:
                        value = statisticData["keyErr"]
                    self.mongoList[key]=value

                #获取MongoDB的平仓收益
                self.money_close_MongoList.append(self.mongoList["money_close"])
            # print("888888888888")
            # print(self.mongoList["money_close"])
            #获取MongoDB的平仓做多盈利收益
                self.money_profit_long_close_MongoList.append(self.mongoList["money_profit_long_close"])
                #获取MongoDB的平仓做多亏损收益
                self.money_loss_long_close_MongoList.append(self.mongoList["money_loss_long_close"])
                #获取MongoDB的平仓做空盈利收益
                self.money_profit_short_close_MongoList.append(self.mongoList["money_profit_short_close"])
                #获取MongoDB的平仓做空亏损收益
                self.money_loss_short_close_MongoList.append(self.mongoList["money_loss_short_close"])
                #获取MongoDB的平仓点数
                self.point_close_MongoList.append(self.mongoList["point_close"])
                #获取MongoDB的平仓做多盈利点数
                self.point_profit_long_close_MongoList.append(self.mongoList["point_profit_long_close"])
                #获取MongoDB的平仓做多亏损点数
                self.point_loss_long_close_MongoList.append(self.mongoList["point_loss_long_close"])
                #获取MongoDB的平仓做空盈利点数
                self.point_profit_short_close_MongoList.append(self.mongoList["point_profit_short_close"])
                #获取MongoDB的平仓做空亏损点数
                self.point_loss_short_close_MongoList.append(self.mongoList["point_loss_short_close"])
                #获取MongoDB的平仓所有做多手数
                self.standardlots_long_close_MongoList.append(self.mongoList["standardlots_long_close"])
                #获取MongoDB的平仓所有做空手数
                self.standardlots_short_close_MongoList.append(self.mongoList["standardlots_short_close"])



            table_1 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","周","平仓收益","平仓做多盈利收益","平仓做多亏损收益","平仓做空盈利收益","平仓做空亏损收益","做多手数"])
            table_2 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","周","平仓点数","平仓做多盈利点数","平仓做多亏损点数","平仓做空盈利点数","平仓做空亏损点数","做空手数"])

            try: 
                table_1.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.item["Week"],self.mongoList["money_close"],self.mongoList["money_profit_long_close"],self.mongoList["money_loss_long_close"],self.mongoList["money_profit_short_close"],self.mongoList["money_loss_short_close"],self.mongoList["standardlots_long_close"]])
                table_1.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["Week"],self.item["Money"],self.item["MoneyProfitLong"],self.item["MoneyLossLong"],self.item["MoneyProfitShort"],self.item["MoneyLossShort"],self.item["StandardLotsLong"]])
                table_1.add_row(["","","","","","","","","","",""])
                table_2.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.item["Week"],self.mongoList["point_close"],self.mongoList["point_profit_long_close"],self.mongoList["point_loss_long_close"],self.mongoList["point_profit_short_close"],self.mongoList["point_loss_short_close"],self.mongoList["standardlots_short_close"]])
                table_2.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["Week"],self.item["Pips"],self.item["PipsProfitLong"],self.item["PipsLossLong"],self.item["PipsProfitShort"],self.item["PipsLossShort"],self.item["StandardLotsShort"]])
                table_2.add_row(["","","","","","","","","","",""])
                    
            finally:
                table_1.reversesort = True
                table_2.reversesort = True
                print(table_1)
                print(table_2)

    def setUp(self):
        pass
    
    def test_1_Money(self): 
        #平仓收益
        self.assertAlmostEqual(self.mongoList["money_close"],float(self.item["Money"]),delta = 0.01)

    def test_2_AvgProfitMoney(self): 
        #平仓做多盈利收益
        self.assertAlmostEqual(self.mongoList["money_profit_long_close"],float(self.item["MoneyProfitLong"]),delta = 0.01)
    
    def test_3_MaxLossPips(self):     
        #平仓做多亏损收益
        self.assertAlmostEqual(self.mongoList["money_loss_long_close"],float(self.item["MoneyLossLong"]),delta = 0.01)

    def test_4_Pips(self):
        #平仓做空盈利收益
        self.assertAlmostEqual(self.mongoList["money_profit_short_close"],float(self.item["MoneyProfitShort"]),delta = 0.01)

    def test_5_AvgMoney(self):
        #平仓做空亏损收益
        self.assertAlmostEqual(self.mongoList["money_loss_short_close"],float(self.item["MoneyLossShort"]),delta = 0.01)

    def test_6_AvgProfitMoney(self): 
        #平仓点数
        self.assertAlmostEqual(self.mongoList["point_close"],float(self.item["Pips"]),delta = 0.01)

    def test_7_AvgProfitMoney(self): 
        #平仓做多盈利点数
        self.assertAlmostEqual(self.mongoList["point_profit_long_close"],float(self.item["PipsProfitLong"]),delta = 0.01)
    
    def test_8_MaxLossPips(self):     
        #平仓做多亏损点数
        self.assertAlmostEqual(self.mongoList["point_loss_long_close"],float(self.item["PipsLossLong"]),delta = 0.01)

    def test_9_Pips(self):
        #平仓做空盈利点数
        self.assertAlmostEqual(self.mongoList["point_profit_short_close"],float(self.item["PipsProfitShort"]),delta = 0.01)

    def test_10_AvgMoney(self):
        #平仓做空亏损点数
        self.assertAlmostEqual(self.mongoList["point_loss_short_close"],float(self.item["PipsLossShort"]),delta = 0.01)

    def test_11_Pips(self):
        #做多手数
        self.assertAlmostEqual(self.mongoList["standardlots_long_close"],float(self.item["StandardLotsLong"]),delta = 0.01)

    def test_12_AvgMoney(self):
        #做空手数
        self.assertAlmostEqual(self.mongoList["standardlots_short_close"],float(self.item["StandardLotsShort"]),delta = 0.01)
    

    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

