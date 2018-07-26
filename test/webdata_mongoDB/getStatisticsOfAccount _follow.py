#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getStatisticsOfAccount
# 用例标题: 获取跟随者个人展示页交易概览数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
#   1.获取跟随者个人展示页交易概览数据对比MongoDB数据
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180515
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
        self.userID = '117432'
        self.AccountIndex = 6
        #获取MT4账号
        self.mt4Account = Statistic.getMt4Account(userID=str(self.userID),accountIndex=str(self.AccountIndex))
        print(self.mt4Account)
        '''获取跟随者的个人展示页的交易概览数据'''
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

        
        table_1 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","收益率","自主收益率","跟随收益率"])
        table_2 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","交易手数","自主交易手数","跟随交易手数"])
        table_3 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","平均获利","自主平均获利","跟随平均获利"])
        table_4 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","收益点数","自主收益点数","跟随收益点数"])
        table_5 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","交易笔数","自主交易笔数","跟随交易笔数"])
        table_6 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","平均亏损","自主平均亏损","跟随平均亏损"])
        table_7 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","收益金额","自主收益金额","跟随收益金额"])
        table_8 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","盈利订单笔数","亏损交易笔数","自主盈利笔数","自主亏损笔数"])
        table_9 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","跟随盈利笔数","跟随亏损笔数","交易周期"])
        try:
            
            table_1.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["rate_ss_profit_balance_close"],self.mongoList["rate_ss_profit_balance_close_self"],self.mongoList["rate_ss_profit_balance_close_follow"]])
            table_1.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["Roi"],self.item["SelfRoi"],self.item["FollowRoi"]])
            table_1.add_row(["","","","","","",""])
            table_2.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["standardlots_close"],self.mongoList["standardlots_cs"],self.mongoList["standardlots_cf"]])
            table_2.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["StandardLots"],self.item["SelfStandardLots"],self.item["FollowStandardLots"]])
            table_2.add_row(["","","","","","",""])
            table_3.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["money_profit_close_avg"],self.mongoList["money_profit_cs_avg"],self.mongoList["money_profit_cf_avg"]])
            table_3.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["AvgProfitMoney"],self.item["SelfAvgProfitMoney"],self.item["FollowAvgProfitMoney"]])
            table_3.add_row(["","","","","","",""])
            table_4.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["point_close"],self.mongoList["point_cs"],self.mongoList["point_cf"]])
            table_4.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["Pips"],self.item["SelfPips"],self.item["FollowPips"]])
            table_4.add_row(["","","","","","",""])
            table_5.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["deal_close"],self.mongoList["deal_cs"],self.mongoList["deal_cf"]])
            table_5.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["Orders"],self.item["SelfOrders"],self.item["FollowOrders"]])
            table_5.add_row(["","","","","","",""])
            table_6.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["money_loss_close_avg"],self.mongoList["money_loss_cs_avg"],self.mongoList["money_loss_cf_avg"]])
            table_6.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["AvgLossMoney"],self.item["SelfAvgLossMoney"],self.item["FollowAvgLossMoney"]])
            table_6.add_row(["","","","","","",""])
            table_7.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["money_close"],self.mongoList["money_cs"],self.mongoList["money_cf"]])
            table_7.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["Money"],self.item["SelfMoney"],self.item["FollowMoney"]])
            table_7.add_row(["","","","","","",""])
            table_8.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["deal_profit_close"],self.mongoList["deal_loss_close"],self.mongoList["deal_profit_cs"],self.mongoList["deal_loss_cs"]])
            table_8.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["ProfitOrders"],self.item["LossOrders"],self.item["SelfProfitOrders"],self.item["SelfLossOrders"],])
            table_8.add_row(["","","","","","","",""])
            table_9.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["deal_profit_cf"],self.mongoList["deal_loss_cf"],self.mongoList["period_trade"]])
            table_9.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["FollowProfitOrders"],self.item["FollowLossOrders"],self.item["Weeks"]])
            table_9.add_row(["","","","","","",""])
            
        finally:
            table_1.reversesort = True
            table_2.reversesort = True
            table_3.reversesort = True
            table_4.reversesort = True
            table_5.reversesort = True
            table_6.reversesort = True
            table_7.reversesort = True
            table_8.reversesort = True
            table_9.reversesort = True


            print(table_1)
            print(table_2)
            print(table_3)
            print(table_4)
            print(table_5)
            print(table_6)
            print(table_7)
            print(table_8)
            print(table_9)                        

    def test_1_ProfitOrders(self):           
        #盈亏点数
        self.assertAlmostEqual(self.mongoList["rate_ss_profit_balance_close"],float(self.item["Roi"]),delta = 0.01)

    def test_2_AvgProfitMoney(self): 
        #交易笔数
        self.assertAlmostEqual(sself.mongoList["rate_ss_profit_balance_close_self"],float(self.item["SelfRoi"]),delta = 0.01)
    
    def test_3_MaxLossPips(self):     
        #自主开仓笔数
        self.assertAlmostEqual(self.mongoList["rate_ss_profit_balance_close_follow"],float(self.item["FollowRoi"]),delta = 0.01)

    def test_4_Pips(self):
        #交易手数
        self.assertAlmostEqual(self.mongoList["standardlots_close"],float(self.item["StandardLots"]),delta = 0.01)

    def test_5_AvgMoney(self):
        #平均获利点数
        self.assertAlmostEqual(self.mongoList["standardlots_cs"],float(self.item["SelfStandardLots"]),delta = 0.01)
    
    def test_6_SharpRate(self):    
        #胜出交易笔数
        self.assertAlmostEqual(self.mongoList["standardlots_cf"],float(self.item["FollowStandardLots"]),delta = 0.01)
        
    def test_7_StandardLots(self):  
        #跟随开仓笔数
        self.assertAlmostEqual(self.mongoList["money_profit_close_avg"],float(self.item["AvgProfitMoney"]),delta = 0.01)
        
    def test_8_BuyProfitOrders(self):
        #交易周期
        self.assertAlmostEqual(self.mongoList["money_profit_cs_avg"],float(self.item["SelfAvgProfitMoney"]),delta = 0.01)
    def test_9_Roi(self):
        #收益率
        self.assertAlmostEqual(self.mongoList["money_profit_cf_avg"],float(self.item["FollowAvgProfitMoney"]),delta = 0.01)

    def test_10_FollowRoi(self):
        #跟随收益率
        self.assertAlmostEqual(self.mongoList["point_close"],float(self.item["Pips"]),delta = 0.01)

    def test_11_FollowPips(self):
        #跟随获利点数
        self.assertAlmostEqual(self.mongoList["point_cs"],float(self.item["SelfPips"]),delta = 0.01)

    def test_12_FollowPips(self):
        #跟随获利点数
        self.assertAlmostEqual(self.mongoList["point_cf"],float(self.item["FollowPips"]),delta = 0.01)

    def test_13_FollowPips(self):
        #跟随获利点数
        self.assertAlmostEqual(self.mongoList["deal_close"],float(self.item["Orders"]),delta = 0.01)

    def test_1_ProfitOrders(self):           
        #盈亏点数
        self.assertAlmostEqual(self.mongoList["deal_cs"],float(self.item["SelfOrders"]),delta = 0.01)

    def test_2_AvgProfitMoney(self): 
        #交易笔数
        self.assertAlmostEqual(self.mongoList["deal_cf"],float(self.item["FollowOrders"]),delta = 0.01)
    
    def test_3_MaxLossPips(self):     
        #自主开仓笔数
        self.assertAlmostEqual(self.mongoList["money_loss_close_avg"],float(self.item["AvgLossMoney"]),delta = 0.01)

    def test_4_Pips(self):
        #交易手数
        self.assertAlmostEqual(self.mongoList["money_loss_cs_avg"],float(self.item["SelfAvgLossMoney"]),delta = 0.01)

    def test_5_AvgMoney(self):
        #平均获利点数
        self.assertAlmostEqual(self.mongoList["money_loss_cf_avg"],float(self.item["FollowAvgLossMoney"]),delta = 0.01)
   
    def test_6_SharpRate(self):    
        #胜出交易笔数
        self.assertAlmostEqual(self.mongoList["money_close"],float(self.item["Money"]),delta = 0.01)
        
    def test_7_StandardLots(self):  
        #跟随开仓笔数
        self.assertAlmostEqual(self.mongoList["money_cs"],float(self.item["SelfMoney"]),delta = 0.01)
        
    def test_8_BuyProfitOrders(self):
        #交易周期
        self.assertAlmostEqual(self.mongoList["money_cf"],float(self.item["FollowMoney"]),delta = 0.01)

    def test_9_Roi(self):
        #收益率
        self.assertAlmostEqual(self.mongoList["deal_profit_close"],float(self.item["ProfitOrders"]),delta = 0.01)

    def test_10_FollowRoi(self):
        #跟随收益率
        self.assertAlmostEqual(self.mongoList["deal_loss_close"],float(self.item["LossOrders"]),delta = 0.01)

    def test_11_FollowPips(self):
        #跟随获利点数
        self.assertAlmostEqual(self.mongoList["deal_profit_cs"],float(self.item["SelfProfitOrders"]),delta = 0.01)

    def test_12_FollowPips(self):
        #跟随获利点数
        self.assertAlmostEqual(self.mongoList["deal_loss_cs"],float(self.item["SelfLossOrders"]),delta = 0.01)

    def test_10_FollowRoi(self):
        #跟随收益率
        self.assertAlmostEqual(self.mongoList["deal_profit_cf"],float(self.item["FollowProfitOrders"]),delta = 0.01)

    def test_11_FollowPips(self):
        #跟随获利点数
        self.assertAlmostEqual(self.mongoList["deal_loss_cf"],float(self.item["FollowLossOrders"]),delta = 0.01)

    def test_12_FollowPips(self):
        #跟随获利点数
        self.assertAlmostEqual(self.mongoList["period_trade"],float(self.item["Weeks"]),delta = 0.9)
            
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

