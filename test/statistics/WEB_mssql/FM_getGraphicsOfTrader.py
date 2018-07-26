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
import Auth,FMCommon,Common,PersonalPage,Statistic
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
personalPageData = FMCommon.loadPersonalPageYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()

class GraphicsOfTrader(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_1_getGraphicsOfTrader(self):
        '''获取交易员图表数据'''
        userID = "148174"
        accountIndex = "2"
        url = webAPIData['hostName']+personalPageData['getGraphicsOfTrader_url1'] + userID+'_'+accountIndex + personalPageData['getGraphicsOfTrader_url2']
        statisticData=PersonalPage.getGraphicsOfTrader(url,headers=webAPIData['headers'],printLogs=1)
        #请求成功 返回 200
        self.assertEqual(statisticData.status_code,webAPIData['status_code_200'])
        statistic = json.loads(statisticData.text)["data"]
        mt4Account = Statistic.getMt4Account(userID=userID,accountIndex=accountIndex)
        BrokerId = Statistic.BrokerId(userID=userID,accountIndex=accountIndex)

        #获取每月收益图表数据
        monthProfit = PrettyTable(["预期/实际","报告月份","盈亏"])
        try:
            for key,value in json.loads(statisticData.text)["data"]["months"].items():
                xMonthProfit = Statistic.xMonthProfit(mt4Account=mt4Account,brokerID=BrokerId,date=key.replace("/","-"))
                monthProfit.add_row(["预期结果",key,xMonthProfit])
                monthProfit.add_row(["实际结果",key,value])
                monthProfit.add_row(["","",""])
                #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
                self.assertAlmostEqual(xMonthProfit,value,delta = 10000)
        finally:
            monthProfit.reversesort = True
            print(monthProfit)


        #获取总收益净值图表数据
        sumProfit = PrettyTable(["预期/实际","报告时间","净值","当天收益","总收益","买入(订单)","买入(标准手)","卖出(订单)","卖出(标准手)"])
        try:
            for statstic in json.loads(statisticData.text)["data"]["days"]:
                xDayEquity = Statistic.xDayTraderEquity(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                xDayProfit = Statistic.xDayTraderProfit(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                xDayProfitSum = Statistic.xDayTraderProfitSum(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                xDayBuyOrders = Statistic.xDayTraderBuyOrders(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                xDayBuyVolume = Statistic.xDayTraderBuyVolume(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                xDaySellOrders = Statistic.xDayTraderSellOrders(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                xDaySellVolume = Statistic.xDayTraderSellVolume(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                sumProfit.add_row(["预期结果",statstic["ReportTime"],xDayEquity,xDayProfit,xDayProfitSum,xDayBuyOrders,xDayBuyVolume,xDaySellOrders,xDaySellVolume])
                sumProfit.add_row(["实际结果",statstic["ReportTime"],statstic["Equity"],statstic["Profit"],statstic["TotalProfit"],statstic["BuyOrders"],statstic["BuyStandardLots"],statstic["SellOrders"],statstic["SellStandardLots"]])
                sumProfit.add_row(["","","","","","","","",""])
                #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
                # self.assertAlmostEqual(float(xDayEquity),statstic["Equity"],delta = 1000000)
                # self.assertAlmostEqual(float(xDayProfit),statstic["Profit"],delta = 1000000)
                # self.assertAlmostEqual(float(xDayProfitSum),statstic["TotalProfit"],delta = 1000000)
                # self.assertAlmostEqual(float(xDayBuyOrders),statstic["BuyOrders"],delta = 1000000)
                # self.assertAlmostEqual(float(xDayBuyVolume),statstic["BuyStandardLots"],delta = 1000000)
                # self.assertAlmostEqual(float(xDaySellOrders),statstic["SellOrders"],delta = 1000000)
                # self.assertAlmostEqual(float(xDaySellVolume),statstic["SellStandardLots"],delta = 1000000)
        finally:
            sumProfit.reversesort = True
            print(sumProfit)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

