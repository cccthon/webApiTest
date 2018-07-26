#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getStatisticsOfAccount
# 用例标题: 获取交易员个人展示页交易概览接口多空分析数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
#   1. 获取交易员个人展示页交易概览接口多空分析数据对比MongoDB数据
#   1.1 做多标准手
#   1.2 做空标准手
#   1.3 做多收益金额
#   1.4 做空收益金额
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180522
#=========================================================
import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,Statistic,Follow
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable
from pymongo import MongoClient

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()
followData = FMCommon.loadFollowYML()

class HotTrader(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #入参
        self.userID = 84524     #'132316'
        self.AccountIndex = 3 #5
        #获取MT4账号
        self.mt4Account = Statistic.getMt4Account(userID=str(self.userID),accountIndex=str(self.AccountIndex))
        print(self.mt4Account)
        '''获取个人展示页的交易概览接口多空分析数据'''
        statisticsOfAccount = Follow.getStatisticsOfAccount(webAPIData['hostName'] + followData['getStatisticsOfAccount_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + followData["getStatisticsOfAccount_url1"],printLogs=1)
        # self.assertEqual(statisticsOfAccount.status_code, webAPIData['status_code_200'])
        self.item = json.loads(statisticsOfAccount.text)["data"]
        
        #连接mongoDB
        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        mongoDB = FMCommon.mongoDB_operater_data(host=mongoUrl, port = statisticData["mongo_port"])
        for i in mongoDB.datastatistic.mg_result_all.find({"login":str(self.mt4Account)}):
            self.mongoList = {}
            for key in statisticData["mongoKeyListAll"]:
                try:
                    value = i[key]
                except KeyError:
                    value = statisticData["keyErr"]
                self.mongoList[key]=value
        
        table_1 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","做多标准手","做空标准手","做多收益金额","做空收益金额","平仓做多笔数","平仓做空笔数"])
        table_2 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","平仓做多亏损笔数","平仓做多盈利笔数","平仓做空亏损笔数"," 平仓做空盈利笔数"])

        try:
            
            table_1.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["standardlots_long_close"],self.mongoList["standardlots_short_close"],self.mongoList["money_long_close"],self.mongoList["money_short_close"],self.mongoList["deal_long_close"],self.mongoList["deal_short_close"]])
            table_1.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["LongStandardLots"],self.item["ShortStandardLots"],self.item["LongMoney"],self.item["ShortMoney"],self.item["BuyOrders"],self.item["SellOrders"]])
            table_1.add_row(["","","","","","","","","",""])
            table_2.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["deal_loss_long_close"],self.mongoList["deal_profit_long_close"],self.mongoList["deal_loss_short_close"],self.mongoList["deal_profit_short_close"]])
            table_2.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["BuyLossOrders"],self.item["BuyProfitOrders"],self.item["SellLossOrders"],self.item["SellProfitOrders"]])
            table_2.add_row(["","","","","","","",""])
            
        finally:
            table_1.reversesort = True
            table_2.reversesort = True
            print(table_1)  
            print(table_2)          


    def test_1_LongStandardLots(self):           
        #做多标准手
        self.assertAlmostEqual(self.mongoList["standardlots_long_close"],float(self.item["LongStandardLots"]),delta = 0.01)

    def test_2_ShortStandardLots(self): 
        #做空标准手
        self.assertAlmostEqual(self.mongoList["standardlots_short_close"],float(self.item["ShortStandardLots"]),delta = 0.01)
    
    def test_3_LongMoney(self):     
        #最做多收益金额
        self.assertAlmostEqual(self.mongoList["money_long_close"],float(self.item["LongMoney"]),delta = 0.01)

    def test_4_ShortMoney(self):
        #做空收益金额
        self.assertAlmostEqual(self.mongoList["money_short_close"],float(self.item["ShortMoney"]),delta = 0.01)
    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

