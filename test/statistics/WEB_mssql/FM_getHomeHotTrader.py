#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getHomeHotTrader
# 用例标题: 获取首页的热门交易员信息
# 预置条件: 
# 测试步骤:
#   1.不登录的情况下获取首页热门交易员信息
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: shencanhui
# 写作日期: 20171211
#=========================================================
import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,Statistic
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()

class HotTrader(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_hotTrader_dayProfit(self):
        '''获取首页的热门交易员日获利信息'''
        hotTrader = Common.getHomeHotTrader(webAPIData['hostName'] + commonData['getHomeHotTrader_url'],printLogs=0)
        self.assertEqual(hotTrader.status_code, webAPIData['status_code_200'])
        print("hotTrader_dayProfit:")
        table = PrettyTable(["预期/实际","NickName","UserID","MT4account","AccountIndex", "跟随获利","被跟随人数","盈亏点数","近一日收益"])
        try:
            for item in json.loads(hotTrader.text)["data"]["Items"]:
                if item["ScreenTime"] == 1:
                    mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                    moneyFollowCloseSum = Statistic.moneyFollowCloseSum(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    befollowedCount = Statistic.befollowedCount(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    pointCloseSum = Statistic.pointCloseSum(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    moneyFollowCloseDay = Statistic.moneyFollowCloseDay(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    table.add_row(["预期结果",item["NickName"],item["UserId"],item["MT4Account"],item["AccountCurrentIndex"],moneyFollowCloseSum,befollowedCount,pointCloseSum,moneyFollowCloseDay])
                    table.add_row(["实际结果",item["NickName"],item["UserId"],item["MT4Account"],item["AccountCurrentIndex"],item["FollowProfit"],item["FOLLOWEDLOGIN"],item["Point"],item["NearProfit"]])
                    table.add_row(["","","","","","","","",""])
                    self.assertAlmostEqual(moneyFollowCloseSum,float(item["FollowProfit"]),delta = 100000)
                    self.assertAlmostEqual(befollowedCount,float(item["FOLLOWEDLOGIN"]),delta = 100000)
                    self.assertAlmostEqual(pointCloseSum,float(item["Point"]),delta = 100000)
                    self.assertAlmostEqual(moneyFollowCloseDay,float(item["NearProfit"]),delta = 100000)
        finally:
            table.reversesort = True
            print(table)

    def test_hotTrader_monthProfit(self):
        '''获取首页的热门交易员月获利信息'''
        hotTrader = Common.getHomeHotTrader(webAPIData['hostName'] + commonData['getHomeHotTrader_url'],printLogs=1)
        self.assertEqual(hotTrader.status_code, webAPIData['status_code_200'])
        print("hotTrader_monthProfit:")
        table = PrettyTable(["预期/实际","NickName","UserID","MT4account","AccountIndex", "跟随获利","被跟随人数","盈亏点数","近一日收益"])
        try:
            for item in json.loads(hotTrader.text)["data"]["Items"]:
                if item["ScreenTime"] == 30:
                    mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                    moneyFollowCloseSum = Statistic.moneyFollowCloseSum(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    befollowedCount = Statistic.befollowedCount(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    pointCloseSum = Statistic.pointCloseSum(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    moneyFollowCloseDay = Statistic.moneyFollowCloseDay(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    table.add_row(["预期结果",item["NickName"],item["UserId"],item["MT4Account"],item["AccountCurrentIndex"],moneyFollowCloseSum,befollowedCount,pointCloseSum,moneyFollowCloseDay])
                    table.add_row(["实际结果",item["NickName"],item["UserId"],item["MT4Account"],item["AccountCurrentIndex"],item["FollowProfit"],item["FOLLOWEDLOGIN"],item["Point"],item["NearProfit"]])
                    table.add_row(["","","","","","","","",""])
                    self.assertAlmostEqual(moneyFollowCloseSum,float(item["FollowProfit"]),delta = 100000)
                    self.assertAlmostEqual(befollowedCount,float(item["FOLLOWEDLOGIN"]),delta = 100000)
                    self.assertAlmostEqual(pointCloseSum,float(item["Point"]),delta = 100000)
                    self.assertAlmostEqual(moneyFollowCloseDay,float(item["NearProfit"]),delta = 100000)
        finally:
            table.reversesort = True
            print(table)

    def test_hotTrader_sumProfit(self):
        '''获取首页的热门交易员总获利信息'''
        hotTrader = Common.getHomeHotTrader(webAPIData['hostName'] + commonData['getHomeHotTrader_url'],printLogs=1)
        self.assertEqual(hotTrader.status_code, webAPIData['status_code_200'])
        print("hotTrader_sumProfit:")
        table = PrettyTable(["预期/实际","NickName","UserID","MT4account","AccountIndex", "跟随获利","被跟随人数","盈亏点数","近一日收益"])
        try:
            for item in json.loads(hotTrader.text)["data"]["Items"]:
                if item["ScreenTime"] == 0:
                    mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                    moneyFollowCloseSum = Statistic.moneyFollowCloseSum(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    befollowedCount = Statistic.befollowedCount(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    pointCloseSum = Statistic.pointCloseSum(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    moneyFollowCloseDay = Statistic.moneyFollowCloseDay(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    table.add_row(["预期结果",item["NickName"],item["UserId"],item["MT4Account"],item["AccountCurrentIndex"],moneyFollowCloseSum,befollowedCount,pointCloseSum,moneyFollowCloseDay])
                    table.add_row(["实际结果",item["NickName"],item["UserId"],item["MT4Account"],item["AccountCurrentIndex"],item["FollowProfit"],item["FOLLOWEDLOGIN"],item["Point"],item["NearProfit"]])
                    table.add_row(["","","","","","","","",""])
                    self.assertAlmostEqual(moneyFollowCloseSum,float(item["FollowProfit"]),delta = 10000000)
                    self.assertAlmostEqual(befollowedCount,float(item["FOLLOWEDLOGIN"]),delta = 100000)
                    self.assertAlmostEqual(pointCloseSum,float(item["Point"]),delta = 100000)
                    self.assertAlmostEqual(moneyFollowCloseDay,float(item["NearProfit"]),delta = 100000)
        finally:
            table.reversesort = True
            print(table)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

