#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getCustomers
# 用例标题: 获取跟随大师的跟随者信息对比MongoDB统计数据
# 预置条件: 
# 测试步骤:
#   1.获取跟随大师的跟随者信息对比MongoDB统计数据
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180413
#=========================================================
import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,Trade,Statistic
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable
from pymongo import MongoClient
from pyhive import presto 
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
tradeData = FMCommon.loadTradeYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()
accountData = FMCommon.loadAccountYML()
followData = FMCommon.loadFollowYML()


class Customers(unittest.TestCase):
    def setUp(self):
        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        self.mongoDB = FMCommon.mongoDB_operater_data(host=mongoUrl, port = statisticData["mongo_port"])
    def test_1_getCustomers(self):

        '''获取近一周有交易的跟随大师信息'''
        params = {"time":7,"pageField":"FollowProfit"}
        customers = Trade.getCustomers(webAPIData['hostName'] + followData['getRankFollowers_url'],params=params,printLogs=0)
        print(customers)
        self.assertEqual(customers.status_code, webAPIData['status_code_200'])
        # print("Customers_oneWeek:")
        table= PrettyTable(["预期/实际","NickName","UserID","mt4Account","AccountIndex","近一周跟随获利","近一周盈亏点数","收益率","平均获利点数","交易笔数","交易周期"])
        try:
            for item in json.loads(customers.text)["data"]["items"]:
                print(item["UserID"],item["AccountIndex"])
                mt4Account = Statistic.getMt4Account(userID=str(item["UserID"]),accountIndex=str(item["AccountIndex"]))
                print("mt4Account",mt4Account)

                for mongoList in self.mongoDB.datastatistic.mg_result_all.find({"login":mt4Account}):
                    key = []
                    for j in self.mongoDB.datastatistic.mg_result_sorted_all.find({"login":mt4Account,"statName":"money_cf_week"}):
                        print("7777777777777")
                        key.append(j["statValue"])
                    
                    table.add_row(["预期结果",item["NickName"],item["UserID"],mt4Account,item["AccountIndex"],j["statValue"],mongoList["point_close_week"],mongoList["rate_ss_profit_balance_close"],mongoList["point_close_avg"],mongoList["deal_close_week"],mongoList["period_trade"]])
                    table.add_row(["实际结果",item["NickName"],item["UserID"],mt4Account,item["AccountIndex"],item["FollowMoney"],item["Pips"],item["Roi"],item["AveragePips"],item["Orders"],item["Weeks"]])
                    table.add_row(["","","","","","","","","","",""])
                    # #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
                    self.assertAlmostEqual(j["statValue"],float(item["FollowMoney"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["point_close_week"],float(item["Pips"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["rate_ss_profit_balance_close"],float(item["Roi"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["point_close_avg"],float(item["AveragePips"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["deal_close_week"],float(item["Orders"]),delta = 0)
                    self.assertAlmostEqual(mongoList["period_trade"],float(item["Weeks"]),delta = 1)        
        finally:
            table.reversesort = True
            print(table)

    def test_2_getCustomers(self):

        '''获取近一月有交易的跟随大师信息'''
        params = {"time":30,"pageField":"FollowProfit"}
        customers = Trade.getCustomers(webAPIData['hostName'] + followData['getRankFollowers_url'],params=params,printLogs=1)
        self.assertEqual(customers.status_code, webAPIData['status_code_200'])
        # print("Customers_oneWeek:")
        table = PrettyTable(["预期/实际","NickName","UserID","mt4Account","AccountIndex","近一月跟随获利","近一月盈亏点数","收益率","平均获利点数","交易笔数","交易周期"])
        try:
            for item in json.loads(customers.text)["data"]["items"]:
                mt4Account = Statistic.getMt4Account(userID=str(item["UserID"]),accountIndex=str(item["AccountIndex"]))
                for i in self.mongoDB.datastatistic.mg_result_all.find({"login":mt4Account}):
                    mongoList = i
                    
                    key = []
                    for j in self.mongoDB.datastatistic.mg_result_sorted_all.find({"login":mt4Account}):
                        key.append(j["statValue"])
                    # print(key[0])
                    table.add_row(["预期结果",item["NickName"],item["UserID"],mt4Account,item["AccountIndex"],key[2],mongoList["point_close_month"],mongoList["rate_ss_profit_balance_close"],mongoList["point_close_avg"],mongoList["deal_close_month"],mongoList["period_trade"]])
                    table.add_row(["实际结果",item["NickName"],item["UserID"],mt4Account,item["AccountIndex"],item["FollowMoney"],item["Pips"],item["Roi"],item["AveragePips"],item["Orders"],item["Weeks"]])
                    table.add_row(["","","","","","","","","","",""])
                    # #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
                    self.assertAlmostEqual(key[2],float(item["FollowMoney"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["point_close_month"],float(item["Pips"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["rate_ss_profit_balance_close"],float(item["Roi"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["point_close_avg"],float(item["AveragePips"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["deal_close_month"],float(item["Orders"]),delta = 0)
                    self.assertAlmostEqual(mongoList["period_trade"],float(item["Weeks"]),delta = 1)
        finally:
            table.reversesort = True
            print(table)

    def test_3_getCustomers(self):

        '''获取近一日有交易的跟随大师信息'''
        params = {"time":1,"pageField":"FollowProfit"}
        customers = Trade.getCustomers(webAPIData['hostName'] + followData['getRankFollowers_url'],params=params,printLogs=1)
        self.assertEqual(customers.status_code, webAPIData['status_code_200'])
        # print("Customers_oneWeek:")
        table = PrettyTable(["预期/实际","NickName","UserID","mt4Account","AccountIndex","近一日跟随获利","近一日盈亏点数","收益率","平均获利点数","交易笔数","交易周期"])
        try:
            for item in json.loads(customers.text)["data"]["items"]:
                mt4Account = Statistic.getMt4Account(userID=str(item["UserID"]),accountIndex=str(item["AccountIndex"]))
                for i in self.mongoDB.datastatistic.mg_result_all.find({"login":mt4Account}):
                    mongoList = i
                    
                    key = []
                    for j in self.mongoDB.datastatistic.mg_result_sorted_all.find({"login":mt4Account}):
                        key.append(j["statValue"])
                    # print(key[0])
                    table.add_row(["预期结果",item["NickName"],item["UserID"],mt4Account,item["AccountIndex"],key[0],mongoList["point_close_day"],mongoList["rate_ss_profit_balance_close"],mongoList["point_close_avg"],mongoList["deal_close_day"],mongoList["period_trade"]])
                    table.add_row(["实际结果",item["NickName"],item["UserID"],mt4Account,item["AccountIndex"],item["FollowMoney"],item["Pips"],item["Roi"],item["AveragePips"],item["Orders"],item["Weeks"]])
                    table.add_row(["","","","","","","","","","",""])
                    # #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
                    self.assertAlmostEqual(key[0],float(item["FollowMoney"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["point_close_day"],float(item["Pips"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["rate_ss_profit_balance_close"],float(item["Roi"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["point_close_avg"],float(item["AveragePips"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["deal_close_day"],float(item["Orders"]),delta = 0)
                    self.assertAlmostEqual(mongoList["period_trade"],float(item["Weeks"]),delta = 1)
        finally:
            table.reversesort = True
            print()
            print(table)


    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

