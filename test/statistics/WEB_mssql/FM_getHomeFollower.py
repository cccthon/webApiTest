#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getHomeFollower
# 用例标题: 获取首页的跟随者收益信息
# 预置条件: 
# 测试步骤:
#   1.不登录的情况下获取首页的跟随者收益信息
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

class HomeFollowerProfit(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_followerProfit_dayProfit(self):
        '''获取首页的跟随者日收益信息'''
        follower = Common.getHomeFollower(webAPIData['hostName'] + commonData['getHomeFollower_url'],printLogs=1)
        self.assertEqual(follower.status_code, webAPIData['status_code_200'])
        print("followerProfit_dayProfit:")
        table = PrettyTable(["预期/实际","NickName","UserID","MT4account","AccountIndex","他跟随","近一日收益"])
        try:
            for item in json.loads(follower.text)["data"]["Items"]:
                if item["ScreenTime"] == 1:
                    mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                    followedCount = Statistic.followedCount(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    moneyFollowCloseDay = Statistic.moneyFollowCloseDay(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    table.add_row(["预期结果",item["NickName"],item["UserId"],item["MT4Account"],item["AccountCurrentIndex"],followedCount,moneyFollowCloseDay])
                    table.add_row(["实际结果",item["NickName"],item["UserId"],item["MT4Account"],item["AccountCurrentIndex"],item["FOLLOWEDLOGIN"],item["Profit"]])
                    table.add_row(["","","","","","",""])
                    #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
                    self.assertAlmostEqual(followedCount,item["FOLLOWEDLOGIN"],delta = 10000)
                    self.assertAlmostEqual(moneyFollowCloseDay,item["Profit"],delta = 10000)
        finally:
            table.reversesort = True
            print(table)

    def test_followerProfit_monthProfit(self):
        '''获取首页的跟随者月收益信息'''
        follower = Common.getHomeFollower(webAPIData['hostName'] + commonData['getHomeFollower_url'],printLogs=1)
        self.assertEqual(follower.status_code, webAPIData['status_code_200'])
        print("followerProfit_monthProfit:")
        table = PrettyTable(["预期/实际","NickName","UserID","MT4account","AccountIndex","他跟随","近一月收益"])
        try:
            for item in json.loads(follower.text)["data"]["Items"]:
                if item["ScreenTime"] == 30:
                    mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                    followedCount = Statistic.followedCount(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    moneyFollowCloseMonth = Statistic.moneyFollowCloseMonth(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    table.add_row(["预期结果",item["NickName"],item["UserId"],item["MT4Account"],item["AccountCurrentIndex"],followedCount,moneyFollowCloseMonth])
                    table.add_row(["实际结果",item["NickName"],item["UserId"],item["MT4Account"],item["AccountCurrentIndex"],item["FOLLOWEDLOGIN"],item["Profit"]])
                    table.add_row(["","","","","","",""])
                    #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
                    self.assertAlmostEqual(followedCount,item["FOLLOWEDLOGIN"],delta = 100000)
                    self.assertAlmostEqual(moneyFollowCloseMonth,item["Profit"],delta = 100000)
        finally:
            table.reversesort = True
            print(table)

    def test_followerProfit_sumProfit(self):
        '''获取首页的跟随者总收益信息'''
        follower = Common.getHomeFollower(webAPIData['hostName'] + commonData['getHomeFollower_url'],printLogs=1)
        self.assertEqual(follower.status_code, webAPIData['status_code_200'])
        print("followerProfit_sumProfit:")
        table = PrettyTable(["预期/实际","NickName","UserID","MT4account","AccountIndex","他跟随","总收益"])
        try:
            for item in json.loads(follower.text)["data"]["Items"]:
                if item["ScreenTime"] == 0:
                    mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                    followedCount = Statistic.followedCount(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    moneyFollowCloseSum = Statistic.moneyFollowCloseSum(mt4Account=mt4Account,brokerID=item["BrokerId"])
                    table.add_row(["预期结果",item["NickName"],item["UserId"],item["MT4Account"],item["AccountCurrentIndex"],followedCount,moneyFollowCloseSum])
                    table.add_row(["实际结果",item["NickName"],item["UserId"],item["MT4Account"],item["AccountCurrentIndex"],item["FOLLOWEDLOGIN"],item["Profit"]])
                    table.add_row(["","","","","","",""])
                    #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
                    self.assertAlmostEqual(followedCount,item["FOLLOWEDLOGIN"],delta = 100000)
                    self.assertAlmostEqual(moneyFollowCloseSum,item["Profit"],delta = 100000)
        finally:
            table.reversesort = True
            print(table)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

