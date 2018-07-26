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

class GraphicsOfCustomer(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_1_GraphicsOfCustomer(self):
        '''获取跟随者图表数据'''
        userID = "148181"
        accountIndex = "2"
        url = webAPIData['hostName']+personalPageData['getGraphicsOfCustomer_url1'] + userID+'_'+accountIndex + personalPageData['getGraphicsOfCustomer_url2']
        statsticData=PersonalPage.getGraphicsOfCustomer(url,headers=webAPIData['headers'],printLogs=1)
        #请求成功 返回 200
        self.assertEqual(statsticData.status_code,webAPIData['status_code_200'])
        mt4Account = Statistic.getMt4Account(userID=userID,accountIndex=accountIndex)
        BrokerId = Statistic.BrokerId(userID=userID,accountIndex=accountIndex)


        #获取总收益净值图表数据
        sumProfit = PrettyTable(["预期/实际","报告时间","净值","当天收益","总收益","买入(订单)","买入(标准手)","卖出(订单)","卖出(标准手)"])
        try:
            for statstic in json.loads(statsticData.text)["data"]["days"]:
                # print(statstic["Equity"])
                # if statstic["Equity"] == None:
                #     print(statstic["ReportTime"],statstic["Equity"])
                xDayEquity = Statistic.xDayCustomerEquity(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                xDayProfit = Statistic.xDayCustomerProfit(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                xDayProfitSum = Statistic.xDayCustomerProfitSum(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                xDayBuyOrders = Statistic.xDayCustomerBuyOrders(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                xDayBuyVolume = Statistic.xDayCustomerBuyVolume(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                xDaySellOrders = Statistic.xDayCustomerSellOrders(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
                xDaySellVolume = Statistic.xDayCustomerSellVolume(mt4Account=mt4Account,brokerID=BrokerId,date=statstic["ReportTime"])
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

