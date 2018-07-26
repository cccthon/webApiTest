 #========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getStatisticsOfAccount
# 用例标题: 获取交易员个人展示页交易概览数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
#   1.获取个人展示页交易概览数据对比MongoDB数据
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180514
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

class StatisticsOfAccount(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #入参
        self.userID = '132316'
        self.AccountIndex = 4
        #获取MT4账号
        self.mt4Account = Statistic.getMt4Account(userID=str(self.userID),accountIndex=str(self.AccountIndex))
        print(self.mt4Account)
        '''获取个人展示页的交易概览数据'''
        statisticsOfAccount = Follow.getStatisticsOfAccount(webAPIData['hostName'] + followData['getStatisticsOfAccount_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + followData["getStatisticsOfAccount_url1"],printLogs=1)
        # self.assertEqual(statisticsOfAccount.status_code, webAPIData['status_code_200'])
        self.item = json.loads(statisticsOfAccount.text)["data"]
        

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

        
        table_1 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","收益金额","资金最大回撤","入金","出金","交易周期","盈利订单笔数","亏损交易笔数"])
        table_2 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","盈亏点数","交易笔数","交易手数","每笔平均手数","最大持仓手数"])
        table_3 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","平均获利","平均亏损","最大盈利金额","最大亏损金额","最大盈利点数","最大亏损点数"])
        table_4 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","标准差","夏普比率","日均交易手数"])
        
        try:
            
            table_1.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["money_close"],self.mongoList["rate_retracement_max"],self.mongoList["deposit"],self.mongoList["withdraw"],self.mongoList["period_trade"],self.mongoList["deal_profit_close"],self.mongoList["deal_loss_close"]])
            table_1.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["Money"],self.item["MaxRetracementRate"],self.item["DepositSum"],self.item["WithdrawSum"],self.item["Weeks"],self.item["ProfitOrders"],self.item["LossOrders"]])
            table_1.add_row(["","","","","","","","","","",""])
            table_2.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["point_close"],self.mongoList["deal_close"],self.mongoList["standardlots_close"],self.mongoList["standardlots_close_avg"],self.mongoList["standardlots_max"]])
            table_2.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["Pips"],self.item["Orders"],self.item["StandardLots"],self.item["AvgStandardLots"],self.item["MaxStandardLots"]])
            table_2.add_row(["","","","","","","","",""])
            table_3.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["money_profit_close_avg"],self.mongoList["money_loss_close_avg"],self.mongoList["money_profit_close_max"],self.mongoList["money_loss_close_min"],self.mongoList["point_profit_close_max"],self.mongoList["point_loss_close_min"]])
            table_3.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["AvgProfitMoney"],self.item["AvgLossMoney"],self.item["MaxProfitMoney"],self.item["MaxLossMoney"],self.item["MaxProfitPips"],self.item["MaxLossPips"]])
            table_3.add_row(["","","","","","","","","",""])
            table_4.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["standard_deviation"],self.mongoList["sharpe_ratio"],self.mongoList["standardlots_close"]/self.mongoList["period_trade"]/5])
            table_4.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["StandardDeviation"],self.item["SharpRate"],self.item["AvgDayStandardLots"]])
            table_4.add_row(["","","","","","",""])
        
        finally:
            table_1.reversesort = True
            table_2.reversesort = True
            table_3.reversesort = True
            table_4.reversesort = True

            print(table_1)
            print(table_2)
            print(table_3)
            print(table_4)

    def setUp(self):
        pass

    def test_1_ProfitOrders(self):         
        #收益金额
        self.assertAlmostEqual(self.mongoList["money_close"],float(self.item["Money"]),delta = 0.01)

    def test_2_AvgProfitMoney(self): 
        #资金最大回撤
        self.assertAlmostEqual(self.mongoList["rate_retracement_max"],self.item["MaxRetracementRate"],delta = 0.01)
    
    def test_3_MaxLossPips(self):     
        #入金
        self.assertAlmostEqual(self.mongoList["deposit"],float(self.item["DepositSum"]),delta = 0.01)

    def test_4_Pips(self):
        #出金
        self.assertAlmostEqual(self.mongoList["withdraw"],float(self.item["WithdrawSum"]),delta = 0.01)

    def test_4_Pips(self):
        #交易周期
        self.assertAlmostEqual(self.mongoList["period_trade"],float(self.item["Weeks"]),delta = 0.9)

    def test_5_AvgMoney(self):
        #盈利订单笔数
        self.assertAlmostEqual(self.mongoList["deal_profit_close"],float(self.item["ProfitOrders"]),delta = 0.01)
    
    def test_6_SharpRate(self):    
        #亏损交易笔数
        self.assertAlmostEqual(self.mongoList["deal_loss_close"],float(self.item["LossOrders"]),delta = 0.01)

    def test_7_StandardLots(self):  
        #盈亏点数
        self.assertAlmostEqual(self.mongoList["point_close"],float(self.item["Pips"]),delta = 0.01)
        
    def test_8_BuyProfitOrders(self):
        #交易笔数
        self.assertAlmostEqual(self.mongoList["deal_close"],float(self.item["Orders"]),delta = 0.01)
        
    def test_9_AvgLossMoney(self):
        #交易手数
        self.assertAlmostEqual(self.mongoList["standardlots_close"],float(self.item["StandardLots"]),delta = 0.01)
        
    def test_10_AvgProfitPips(self):
        #每笔平均手数
        self.assertAlmostEqual(self.mongoList["standardlots_close_avg"],float(self.item["AvgStandardLots"]),delta = 0.01)
    
    def test_11_TimePossessionAverage(self):    
        #最大持仓手数
        self.assertAlmostEqual(self.mongoList["standardlots_max"],float(self.item["MaxStandardLots"]),delta = 0.01)
                    
    def test_12_StandardDeviation(self):
        #平均获利
        self.assertAlmostEqual(self.mongoList["money_profit_close_avg"],float(self.item["AvgProfitMoney"]),delta = 0.01)
        
    def test_13_MaxRetracementRate(self):
        #平均亏损
        self.assertAlmostEqual(self.mongoList["money_loss_close_avg"],float(self.item["AvgLossMoney"]),delta = 0.01)
        
    def test_14_LossOrders(self):
        #最大盈利金额
        self.assertAlmostEqual(self.mongoList["money_profit_close_max"],float(self.item["MaxProfitMoney"]),delta = 0.01)
        
    def test_15_SellProfitOrders(self):
        #最大亏损金额
        self.assertAlmostEqual(self.mongoList["money_loss_close_min"],float(self.item["MaxLossMoney"]),delta = 0.01)
        
    def test_16_MaxProfitPips(self):
        #最大盈利点数
        self.assertAlmostEqual(self.mongoList["point_profit_close_max"],float(self.item["MaxProfitPips"]),delta = 0.01)
        
    def test_17_AvgLossPips(self):
        #最大亏损点数
        self.assertAlmostEqual(self.mongoList["point_loss_close_min"],float(self.item["MaxLossPips"]),delta = 0.01)

    def test_18_FollowProfitPips(self):
        #标准差
        self.assertAlmostEqual(self.mongoList["standard_deviation"],float(self.item["StandardDeviation"]),delta = 0.01)
        
    def test_19_Activity(self):
        #夏普比率
        self.assertAlmostEqual(self.mongoList["sharpe_ratio"],float(self.item["SharpRate"]),delta = 0.01)

    def test_20_FactorProfitEquity(self):
        #日均交易手数
        self.assertAlmostEqual(self.mongoList["standardlots_close"]/self.mongoList["period_trade"]/5,float(self.item["AvgDayStandardLots"]),delta = 0.01)

    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

