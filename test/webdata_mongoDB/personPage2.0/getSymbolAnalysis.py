 #========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getSymbolAnalysis

# 用例标题: 获取品种分析图表数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
# 1.获取品种分析图表数据对比MongoDB数据
# 1.1 不同品种的收益
# 1.2 不同品种的盈利收益
# 1.3 不同品种的亏损收益
# 1.4 不同品种的亏损收益
# 1.5 不同品种的标准手数
# 1.6 不同品种的订单数
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
        '''获取个人展示页的获取品种分析图表数据'''
        symbolAnalysis = Datastatistic.getSymbolAnalysis(webAPIData['hostName'] + datastatisticData['getSymbolAnalysis_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + datastatisticData["getSymbolAnalysis_url2"],printLogs=0)

        # self.assertEqual(monthAnalysisReport.status_code, webAPIData['status_code_200'])
        self.standardSymbolList = []
        self.moneyList = []
        self.moneyProfitList = []
        self.moneyLossList = []
        self.standardLotsList = []
        self. ordersList = []

        for self.item in json.loads(symbolAnalysis.text)["data"]["SymbolList"]:
            #遍历返回数据的所有标准品种名
            self.standardSymbolList.append(self.item["StandardSymbol"])
            print(self.item["StandardSymbol"])
            #遍历返回数据的所有收益
            self.moneyList.append(self.item["Money"])
            #遍历返回数据的所有盈利收益
            self.moneyProfitList.append(self.item["MoneyProfit"])
            #遍历返回数据的所有亏损收益
            self.standardLotsList.append(self.item["MoneyLoss"])
            #遍历返回数据的所有标准手数
            self.ordersList.append(self.item["StandardLots"])
            #遍历返回数据的所有订单数
            self.ordersList.append(self.item["Orders"])


            self.money_close_MongoList = []
            self.money_profit__close_MongoList = []
            self.money_loss_close_MongoList = []
            self.standardlots_close_MongoList = []
            self.deal_close_MongoList = []
            for i in mongoDB.datastatistic.mg_result_symall.find({"login":str(self.mt4Account),"standardsymbol":str(self.item["StandardSymbol"])}): 
                self.mongoList = {}
                for key in statisticData["mongoKeyListAll"]:
                    try:
                        value = i[key]
                    except KeyError:
                        value = statisticData["keyErr"]
                    self.mongoList[key]=value
                #获取MongoDB的不同品种的收益
                self.money_close_MongoList.append(self.mongoList["money_close"])
                #获取MongoDB的不同品种的盈利收益
                self.money_profit__close_MongoList.append(self.mongoList["money_profit_close"])
                #获取MongoDB的不同品种的亏损收益
                self.money_loss_close_MongoList.append(self.mongoList["money_loss_close"])
                #获取MongoDB的不同品种的标准手数
                self.standardlots_close_MongoList.append(self.mongoList["standardlots_close"])
                #获取MongoDB的不同品种的订单数
                self.deal_close_MongoList.append(self.mongoList["deal_close"])
                table = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","标准品种名","收益","盈利收益","亏损收益","标准手数","订单数"])

                try: 
                    table.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.item["StandardSymbol"],self.mongoList["money_close"],self.mongoList["money_profit_close"],self.mongoList["money_loss_close"],self.mongoList["standardlots_close"],self.mongoList["deal_close"]])
                    table.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["StandardSymbol"],self.item["Money"],self.item["MoneyProfit"],self.item["MoneyLoss"],self.item["StandardLots"],self.item["Orders"]])
                    table.add_row(["","","","","","","","","",""])
                    
                finally:
                    table.reversesort = True
                    print(table)

    def setUp(self):
        pass

    
    def test_1_Money(self):          
        # 收益
        self.assertAlmostEqual(self.mongoList["money_close"],float(self.item["Money"]),delta = 0.01)

    def test_2_MoneyProfit(self): 
        #盈利收益
        self.assertAlmostEqual(self.mongoList["money_profit_close"],float(self.item["MoneyProfit"]),delta = 0.01)
    
    def test_3_MoneyLoss(self):     
        #亏损收益
        self.assertAlmostEqual(self.mongoList["money_loss_close"],float(self.item["MoneyLoss"]),delta = 0.01)

    def test_4_StandardLots(self):
        #标准手数
        self.assertAlmostEqual(self.mongoList["standardlots_close"],float(self.item["StandardLots"]),delta = 0.01)

    def test_5_Orders(self):
        #订单数
        self.assertAlmostEqual(self.mongoList["deal_close"],float(self.item["Orders"]),delta = 0.01)
    

    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

