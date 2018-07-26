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
import Auth,FMCommon,Common,FollowManage,Statistic
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
followData = FMCommon.loadFollowYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()

class ChoiceTrades(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_1_getChoiceTrades_oneWeek(self):
        '''获取近一周的精选交易员信息'''
        #净值利润因子

        params = {"category ":"fm","time":7}
        trades = FollowManage.getTraders(webAPIData['hostName'] + followData['getTraders_url'],params=params,printLogs=1)
        self.assertEqual(trades.status_code, webAPIData['status_code_200'])
        print("ChoiceTrades_oneWeek:")
        table = PrettyTable(["预期/实际","NickName","UserID","AccountIndex","净值利润因子","近一周盈亏点数","交易周期","平均持仓时间","粉丝人数","交易笔数"])
        try:
            for item in json.loads(trades.text)["data"]["items"]:
                mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                factorProfitEquity = Statistic.factorProfitEquity(mt4Account=mt4Account,brokerID=item["BrokerId"])
                nearWeekPoint = Statistic.nearWeekPoint(mt4Account=mt4Account,brokerID=item["BrokerId"])
                tradePeriod = Statistic.tradePeriod(mt4Account=mt4Account,brokerID=item["BrokerId"])
                avgTradeTimeMin = Statistic.avgTradeTime(mt4Account=mt4Account,brokerID=item["BrokerId"])
                avgTradeTime = str(int(avgTradeTimeMin//60) ) + '小时' + str(int(avgTradeTimeMin%60)) + '分'
                fansCount = Statistic.fansCount(mt4Account=mt4Account)
                historyOrder = Statistic.historyOrder(mt4Account=mt4Account,brokerID=item["BrokerId"])
                table.add_row(["预期结果",item["NickName"],item["UserId"],item["AccountCurrentIndex"],factorProfitEquity,nearWeekPoint,tradePeriod,avgTradeTime,fansCount,historyOrder])
                table.add_row(["实际结果",item["NickName"],item["UserId"],item["AccountCurrentIndex"],item["ProfitFactor"],item["BizPoint"],item["Weeks"],item["BizAVGTradeTime"],item["FoucsCount"],item["Orders"]])
                table.add_row(["","","","","","","","","",""])
                #由于非实时统计数据，实际结果存在误差。净值利润因子预期和实际正负差值小于等于0.2都算断言通过
                self.assertAlmostEqual(factorProfitEquity,item["ProfitFactor"],delta = 0.9)
                self.assertAlmostEqual(nearWeekPoint,float(item["BizPoint"]),delta = 100000)
                self.assertAlmostEqual(tradePeriod,item["Weeks"],delta = 1)
                # self.assertEqual(avgTradeTime,item["BizAVGTradeTime"])
                self.assertAlmostEqual(fansCount,item["FoucsCount"],delta = 100)
                self.assertAlmostEqual(historyOrder,item["Orders"],delta = 10000)
        finally:
            table.reversesort = True
            print(table)

    def test_2_getChoiceTrades_twoWeek(self):
        '''获取近两周的精选交易员信息'''
        params = {"category ":"fm","time":14}
        trades = FollowManage.getTraders(webAPIData['hostName'] + followData['getTraders_url'],params=params,printLogs=1)
        self.assertEqual(trades.status_code, webAPIData['status_code_200'])
        print("ChoiceTrades_twoWeek:")
        table = PrettyTable(["预期/实际","NickName","UserID","AccountIndex","净值利润因子","近一周盈亏点数","交易周期","平均持仓时间","粉丝人数","交易笔数"])
        try:
            for item in json.loads(trades.text)["data"]["items"]:
                mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                factorProfitEquity = Statistic.factorProfitEquity(mt4Account=mt4Account,brokerID=item["BrokerId"])
                nearWeekPoint = Statistic.nearWeekPoint(mt4Account=mt4Account,brokerID=item["BrokerId"])
                tradePeriod = Statistic.tradePeriod(mt4Account=mt4Account,brokerID=item["BrokerId"])
                avgTradeTimeMin = Statistic.avgTradeTime(mt4Account=mt4Account,brokerID=item["BrokerId"])
                avgTradeTime = str(int(avgTradeTimeMin//60) ) + '小时' + str(int(avgTradeTimeMin%60)) + '分'
                fansCount = Statistic.fansCount(mt4Account=mt4Account)
                historyOrder = Statistic.historyOrder(mt4Account=mt4Account,brokerID=item["BrokerId"])
                table.add_row(["预期结果",item["NickName"],item["UserId"],item["AccountCurrentIndex"],factorProfitEquity,nearWeekPoint,tradePeriod,avgTradeTime,fansCount,historyOrder])
                table.add_row(["实际结果",item["NickName"],item["UserId"],item["AccountCurrentIndex"],item["ProfitFactor"],item["BizPoint"],item["Weeks"],item["BizAVGTradeTime"],item["FoucsCount"],item["Orders"]])
                table.add_row(["","","","","","","","","",""])
                #由于非实时统计数据，实际结果存在误差。净值利润因子预期和实际正负差值小于等于0.2都算断言通过
                self.assertAlmostEqual(factorProfitEquity,item["ProfitFactor"],delta = 0.9)
                self.assertAlmostEqual(nearWeekPoint,float(item["BizPoint"]),delta = 100000)
                self.assertAlmostEqual(tradePeriod,item["Weeks"],delta = 1)
                # self.assertEqual(avgTradeTime,item["BizAVGTradeTime"])
                self.assertAlmostEqual(fansCount,item["FoucsCount"],delta = 100)
                self.assertAlmostEqual(historyOrder,item["Orders"],delta = 10000)
        finally:
            table.reversesort = True
            print(table)

    def test_3_getChoiceTrades_month(self):
        '''获取近一月的精选交易员信息'''
        params = {"category ":"fm","time":30}
        trades = FollowManage.getTraders(webAPIData['hostName'] + followData['getTraders_url'],params=params,printLogs=1)
        self.assertEqual(trades.status_code, webAPIData['status_code_200'])
        print("ChoiceTrades_month:")
        table = PrettyTable(["预期/实际","NickName","UserID","AccountIndex","净值利润因子","近一周盈亏点数","交易周期","平均持仓时间","粉丝人数","交易笔数"])
        try:
            for item in json.loads(trades.text)["data"]["items"]:
                mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                factorProfitEquity = Statistic.factorProfitEquity(mt4Account=mt4Account,brokerID=item["BrokerId"])
                nearWeekPoint = Statistic.nearWeekPoint(mt4Account=mt4Account,brokerID=item["BrokerId"])
                tradePeriod = Statistic.tradePeriod(mt4Account=mt4Account,brokerID=item["BrokerId"])
                avgTradeTimeMin = Statistic.avgTradeTime(mt4Account=mt4Account,brokerID=item["BrokerId"])
                avgTradeTime = str(int(avgTradeTimeMin//60) ) + '小时' + str(int(avgTradeTimeMin%60)) + '分'
                fansCount = Statistic.fansCount(mt4Account=mt4Account)
                historyOrder = Statistic.historyOrder(mt4Account=mt4Account,brokerID=item["BrokerId"])
                table.add_row(["预期结果",item["NickName"],item["UserId"],item["AccountCurrentIndex"],factorProfitEquity,nearWeekPoint,tradePeriod,avgTradeTime,fansCount,historyOrder])
                table.add_row(["实际结果",item["NickName"],item["UserId"],item["AccountCurrentIndex"],item["ProfitFactor"],item["BizPoint"],item["Weeks"],item["BizAVGTradeTime"],item["FoucsCount"],item["Orders"]])
                table.add_row(["","","","","","","","","",""])
                #由于非实时统计数据，实际结果存在误差。净值利润因子预期和实际正负差值小于等于0.2都算断言通过
                self.assertAlmostEqual(factorProfitEquity,item["ProfitFactor"],delta = 0.9)
                self.assertAlmostEqual(nearWeekPoint,float(item["BizPoint"]),delta = 100000)
                self.assertAlmostEqual(tradePeriod,item["Weeks"],delta = 1)
                # self.assertEqual(avgTradeTime,item["BizAVGTradeTime"])
                self.assertAlmostEqual(fansCount,item["FoucsCount"],delta = 100)
                self.assertAlmostEqual(historyOrder,item["Orders"],delta = 10000)
        finally:
            table.reversesort = True
            print(table)


    def test_4_getSamTrades_oneWeek(self):
        '''获取近一周的全网交易员信息'''
        params = {"category ":"sam","time":7}
        trades = FollowManage.getTraders(webAPIData['hostName'] + followData['getTraders_url'],params=params,printLogs=1)
        self.assertEqual(trades.status_code, webAPIData['status_code_200'])
        print("getSamTrades_oneWeek:")
        table = PrettyTable(["预期/实际","NickName","UserID","AccountIndex","净值利润因子","近一周盈亏点数","交易周期","平均持仓时间","粉丝人数","交易笔数"])
        try:
            for item in json.loads(trades.text)["data"]["items"]:
                mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                factorProfitEquity = Statistic.factorProfitEquity(mt4Account=mt4Account,brokerID=item["BrokerId"])
                nearWeekPoint = Statistic.nearWeekPoint(mt4Account=mt4Account,brokerID=item["BrokerId"])
                tradePeriod = Statistic.tradePeriod(mt4Account=mt4Account,brokerID=item["BrokerId"])
                avgTradeTimeMin = Statistic.avgTradeTime(mt4Account=mt4Account,brokerID=item["BrokerId"])
                avgTradeTime = str(int(avgTradeTimeMin//60) ) + '小时' + str(int(avgTradeTimeMin%60)) + '分'
                fansCount = Statistic.fansCount(mt4Account=mt4Account)
                historyOrder = Statistic.historyOrder(mt4Account=mt4Account,brokerID=item["BrokerId"])
                table.add_row(["预期结果",item["NickName"],item["UserId"],item["AccountCurrentIndex"],factorProfitEquity,nearWeekPoint,tradePeriod,avgTradeTime,fansCount,historyOrder])
                table.add_row(["实际结果",item["NickName"],item["UserId"],item["AccountCurrentIndex"],item["ProfitFactor"],item["BizPoint"],item["Weeks"],item["BizAVGTradeTime"],item["FoucsCount"],item["Orders"]])
                table.add_row(["","","","","","","","","",""])
                #由于非实时统计数据，实际结果存在误差。净值利润因子预期和实际正负差值小于等于0.2都算断言通过
                self.assertAlmostEqual(factorProfitEquity,item["ProfitFactor"],delta = 0.9)
                self.assertAlmostEqual(nearWeekPoint,float(item["BizPoint"]),delta = 100000)
                self.assertAlmostEqual(tradePeriod,item["Weeks"],delta = 1)
                # self.assertEqual(avgTradeTime,item["BizAVGTradeTime"])
                self.assertAlmostEqual(fansCount,item["FoucsCount"],delta = 100)
                self.assertAlmostEqual(historyOrder,item["Orders"],delta = 10000)
        finally:
            table.reversesort = True
            print(table)


    def test_5_getSamTrades_twoWeek(self):
        '''获取近两周的全网交易员信息'''
        params = {"category ":"sam","time":14}
        trades = FollowManage.getTraders(webAPIData['hostName'] + followData['getTraders_url'],params=params,printLogs=1)
        self.assertEqual(trades.status_code, webAPIData['status_code_200'])
        print("getSamTrades_twoWeek:")
        table = PrettyTable(["预期/实际","NickName","UserID","AccountIndex","净值利润因子","近一周盈亏点数","交易周期","平均持仓时间","粉丝人数","交易笔数"])
        try:
            for item in json.loads(trades.text)["data"]["items"]:
                mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                factorProfitEquity = Statistic.factorProfitEquity(mt4Account=mt4Account,brokerID=item["BrokerId"])
                nearWeekPoint = Statistic.nearWeekPoint(mt4Account=mt4Account,brokerID=item["BrokerId"])
                tradePeriod = Statistic.tradePeriod(mt4Account=mt4Account,brokerID=item["BrokerId"])
                avgTradeTimeMin = Statistic.avgTradeTime(mt4Account=mt4Account,brokerID=item["BrokerId"])
                avgTradeTime = str(int(avgTradeTimeMin//60) ) + '小时' + str(int(avgTradeTimeMin%60)) + '分'
                fansCount = Statistic.fansCount(mt4Account=mt4Account)
                historyOrder = Statistic.historyOrder(mt4Account=mt4Account,brokerID=item["BrokerId"])
                table.add_row(["预期结果",item["NickName"],item["UserId"],item["AccountCurrentIndex"],factorProfitEquity,nearWeekPoint,tradePeriod,avgTradeTime,fansCount,historyOrder])
                table.add_row(["实际结果",item["NickName"],item["UserId"],item["AccountCurrentIndex"],item["ProfitFactor"],item["BizPoint"],item["Weeks"],item["BizAVGTradeTime"],item["FoucsCount"],item["Orders"]])
                table.add_row(["","","","","","","","","",""])
                #由于非实时统计数据，实际结果存在误差。净值利润因子预期和实际正负差值小于等于0.2都算断言通过
                self.assertAlmostEqual(factorProfitEquity,item["ProfitFactor"],delta = 0.9)
                self.assertAlmostEqual(nearWeekPoint,float(item["BizPoint"]),delta = 100000)
                self.assertAlmostEqual(tradePeriod,item["Weeks"],delta = 1)
                # self.assertEqual(avgTradeTime,item["BizAVGTradeTime"])
                self.assertAlmostEqual(fansCount,item["FoucsCount"],delta = 100)
                self.assertAlmostEqual(historyOrder,item["Orders"],delta = 10000)
        finally:
            table.reversesort = True
            print(table)


    def test_6_getSamTrades_month(self):
        '''获取近一月的全网交易员信息'''
        params = {"category ":"sam","time":30}
        trades = FollowManage.getTraders(webAPIData['hostName'] + followData['getTraders_url'],params=params,printLogs=1)
        self.assertEqual(trades.status_code, webAPIData['status_code_200'])
        print("getSamTrades_month:")
        table = PrettyTable(["预期/实际","NickName","UserID","AccountIndex","净值利润因子","近一周盈亏点数","交易周期","平均持仓时间","粉丝人数","交易笔数"])
        try:
            for item in json.loads(trades.text)["data"]["items"]:
                mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                factorProfitEquity = Statistic.factorProfitEquity(mt4Account=mt4Account,brokerID=item["BrokerId"])
                nearWeekPoint = Statistic.nearWeekPoint(mt4Account=mt4Account,brokerID=item["BrokerId"])
                tradePeriod = Statistic.tradePeriod(mt4Account=mt4Account,brokerID=item["BrokerId"])
                avgTradeTimeMin = Statistic.avgTradeTime(mt4Account=mt4Account,brokerID=item["BrokerId"])
                avgTradeTime = str(int(avgTradeTimeMin//60) ) + '小时' + str(int(avgTradeTimeMin%60)) + '分'
                fansCount = Statistic.fansCount(mt4Account=mt4Account)
                historyOrder = Statistic.historyOrder(mt4Account=mt4Account,brokerID=item["BrokerId"])
                table.add_row(["预期结果",item["NickName"],item["UserId"],item["AccountCurrentIndex"],factorProfitEquity,nearWeekPoint,tradePeriod,avgTradeTime,fansCount,historyOrder])
                table.add_row(["实际结果",item["NickName"],item["UserId"],item["AccountCurrentIndex"],item["ProfitFactor"],item["BizPoint"],item["Weeks"],item["BizAVGTradeTime"],item["FoucsCount"],item["Orders"]])
                table.add_row(["","","","","","","","","",""])
                #由于非实时统计数据，实际结果存在误差。净值利润因子预期和实际正负差值小于等于0.2都算断言通过
                self.assertAlmostEqual(factorProfitEquity,item["ProfitFactor"],delta = 0.9)
                self.assertAlmostEqual(nearWeekPoint,float(item["BizPoint"]),delta = 1000000)
                self.assertAlmostEqual(tradePeriod,item["Weeks"],delta = 1)
                # self.assertEqual(avgTradeTime,item["BizAVGTradeTime"])
                self.assertAlmostEqual(fansCount,item["FoucsCount"],delta = 100)
                self.assertAlmostEqual(historyOrder,item["Orders"],delta = 10000)
        finally:
            table.reversesort = True
            print(table)


    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

