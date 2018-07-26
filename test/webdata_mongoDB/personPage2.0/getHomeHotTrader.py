88#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getHomeHotTrader
# 用例标题: 获取首页的热门交易员信息
# 预置条件: 
# 测试步骤:
#   1.不登录的情况下获取首页热门交易员信息
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180423
#=========================================================
import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,Statistic
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable
from pymongo import MongoClient

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()

class HotTrader(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        self.mongoDB = FMCommon.mongoDB_operater_data(host=mongoUrl, port = statisticData["mongo_port"])


    def test_1_hotTrader_dayProfit(self):
        '''获取首页的热门交易员日获利信息'''
        hotTrader = Common.getHomeHotTrader(webAPIData['hostName'] + "api/v2/trade/home/hot-traders",printLogs=0)
        self.assertEqual(hotTrader.status_code, webAPIData['status_code_200'])
        print("hotTrader_dayProfit:")
        table = PrettyTable(["预期/实际","NickName","UserID","MT4account","AccountIndex", "跟随获利","被跟随人数","盈亏点数","近一日收益"])
        try:
            for item in json.loads(hotTrader.text)["data"]["daily"]:
                # print(item)
                mt4Account = Statistic.getMt4Account(userID=str(item["UserID"]),accountIndex=str(item["AccountIndex"]))
                # print(mt4Account)
                for i in self.mongoDB.datastatistic.mg_result_all.find({"login":mt4Account}):
                    mongoList = {}
                    for key in statisticData["mongoKeyListAll"]:
                        try:
                            value = i[key]
                        except KeyError:
                            value = statisticData["keyErr"]
                        mongoList[key]=value
                    table.add_row(["预期结果",item["NickName"],item["UserID"],mt4Account,item["AccountIndex"],mongoList["money_followed_close_day"],mongoList["report_followerscount_demo_following"] + mongoList["report_followerscount_actual_following"],mongoList["point_close_day"],mongoList["money_close_day"]])
                    table.add_row(["实际结果",item["NickName"],item["UserID"],mt4Account,item["AccountIndex"],item["FollowMoney"],item["FollowAccount"],item["Pips"],item["NearDayMoney"]])
                    table.add_row(["","","","","","","","",""])
                    self.assertAlmostEqual(mongoList["money_followed_close_day"],float(item["FollowMoney"]),delta = 0.01)
                    self.assertAlmostEqual(mongoList["report_followerscount_demo_following"] + mongoList["report_followerscount_actual_following"],item["FollowAccount"],delta = 0.01)
                    self.assertAlmostEqual(mongoList["point_close_day"],float(item["Pips"]),delta = 0.01) 
                    self.assertAlmostEqual(mongoList["money_close_day"],float(item["NearDayMoney"]),delta = 0.01)
        finally:
            table.reversesort = True
            print(table)

    def test_2_hotTrader_monthProfit(self):
        '''获取首页的热门交易员月获利信息'''
        hotTrader = Common.getHomeHotTrader(webAPIData['hostName'] + "api/v2/trade/home/hot-traders",printLogs=1)
        self.assertEqual(hotTrader.status_code, webAPIData['status_code_200'])
        print("hotTrader_monthProfit:")
        table = PrettyTable(["预期/实际","NickName","UserID","MT4account","AccountIndex", "跟随获利","被跟随人数","盈亏点数","近一日收益"])
        try:
            for item in json.loads(hotTrader.text)["data"]["monthly"]:
                # print(item)
                mt4Account = Statistic.getMt4Account(userID=str(item["UserID"]),accountIndex=str(item["AccountIndex"]))
                # print(mt4Account)
                for i in self.mongoDB.datastatistic.mg_result_all.find({"login":mt4Account}):
                    mongoList = {}
                    for key in statisticData["mongoKeyListAll"]:
                        try:
                            value = i[key]
                        except KeyError:
                            value = statisticData["keyErr"]
                        mongoList[key]=value 
                table.add_row(["预期结果",item["NickName"],item["UserID"],mt4Account,item["AccountIndex"],mongoList["money_followed_close_month"],mongoList["report_followerscount_demo_following"] + mongoList["report_followerscount_actual_following"],mongoList["point_close_month"],mongoList["money_close_day"]])
                table.add_row(["实际结果",item["NickName"],item["UserID"],mt4Account,item["AccountIndex"],item["FollowMoney"],item["FollowAccount"],item["Pips"],item["NearDayMoney"]])
                table.add_row(["","","","","","","","",""])
                self.assertAlmostEqual(mongoList["money_followed_close_month"],float(item["FollowMoney"]),delta = 0.01)
                self.assertAlmostEqual(mongoList["report_followerscount_demo_following"] + mongoList["report_followerscount_actual_following"],item["FollowAccount"],delta = 0.01)
                self.assertAlmostEqual(mongoList["point_close_month"],float(item["Pips"]),delta = 0.01) 
                self.assertAlmostEqual(mongoList["money_close_day"],float(item["NearDayMoney"]),delta = 0.01)
        finally:
            table.reversesort = True
            print(table)

    def test_3_hotTrader_allProfit(self):
        '''获取首页的热门交易员总获利信息'''
        hotTrader = Common.getHomeHotTrader(webAPIData['hostName'] + "api/v2/trade/home/hot-traders",printLogs=1)
        self.assertEqual(hotTrader.status_code, webAPIData['status_code_200'])
        print("hotTrader_allProfit:")
        table = PrettyTable(["预期/实际","NickName","UserID","MT4account","AccountIndex", "跟随获利","被跟随人数","盈亏点数","近一日收益"])
        try:
            for item in json.loads(hotTrader.text)["data"]["all"]:
                # print(item)
                mt4Account = Statistic.getMt4Account(userID=str(item["UserID"]),accountIndex=str(item["AccountIndex"]))
                # print(mt4Account)
                for i in self.mongoDB.datastatistic.mg_result_all.find({"login":mt4Account}):
                    self.mongoList = {}
                    for key in statisticData["mongoKeyListAll"]:
                        try:
                            value = i[key]
                        except KeyError:
                            value = statisticData["keyErr"]
                        self.mongoList[key]=value 
                table.add_row(["预期结果",item["NickName"],item["UserID"],mt4Account,item["AccountIndex"],self.mongoList["money_followed_close_all"],self.mongoList["report_followerscount_demo_following"] + self.mongoList["report_followerscount_actual_following"],self.mongoList["point_close_all"],self.mongoList["money_close_day"]])
                table.add_row(["实际结果",item["NickName"],item["UserID"],mt4Account,item["AccountIndex"],item["FollowMoney"],item["FollowAccount"],item["Pips"],item["NearDayMoney"]])
                table.add_row(["","","","","","","","",""])
                # self.assertEqual(mt4Account,self.mongoList["login"])
                self.assertAlmostEqual(self.mongoList["money_followed_close_all"],float(item["FollowMoney"]),delta = 0.01)
                self.assertAlmostEqual(self.mongoList["report_followerscount_demo_following"] + self.mongoList["report_followerscount_actual_following"],item["FollowAccount"],delta = 0.01)
                self.assertAlmostEqual(self.mongoList["point_close_all"],float(item["Pips"]),delta = 0.01) 
                self.assertAlmostEqual(self.mongoList["money_close_day"],float(item["NearDayMoney"]),delta = 0.01)
        finally:
            table.reversesort = True
            print(table)

    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

