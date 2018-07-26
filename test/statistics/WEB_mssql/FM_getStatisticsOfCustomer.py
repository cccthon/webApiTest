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

class StatisticsOfCustomer(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_1_getStatisticsOfCustomer(self):
        '''获取跟随者用户的交易统计数据'''
        userID = "148181"
        accountIndex = "2"
        url = webAPIData['hostName']+personalPageData['getStatisticsOfcustomer_url1'] + userID+'_'+accountIndex + personalPageData['getStatisticsOfcustomer_url2']
        statisticData=PersonalPage.getStatisticsOfCustomer(url,headers=webAPIData['headers'],printLogs=1)
        #请求成功 返回 200
        self.assertEqual(statisticData.status_code,webAPIData['status_code_200'])
        statistic = json.loads(statisticData.text)["data"]
        mt4Account = Statistic.getMt4Account(userID=userID,accountIndex=accountIndex)
        BrokerId = Statistic.BrokerId(userID=userID,accountIndex=accountIndex)

        rateProfit = Statistic.rateProfit(mt4Account=mt4Account,brokerID=BrokerId)
        followRateProfit = Statistic.followRateProfit(mt4Account=mt4Account,brokerID=BrokerId)
        pointOfCfClose = Statistic.pointOfCfClose(mt4Account=mt4Account,brokerID=BrokerId)
        #获取:收益率,跟随收益率,跟随获利点数
        topTable = PrettyTable(["预期/实际","收益率","跟随收益率","跟随获利点数"])
        topTable.add_row(["预期结果",rateProfit,followRateProfit,pointOfCfClose])
        topTable.add_row(["实际结果",statistic["ROI"],statistic["FollowROI"],statistic["FollowPoints"]])
        try:
            #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
            self.assertAlmostEqual(rateProfit,float(statistic["ROI"]),delta = 20)
            self.assertAlmostEqual(followRateProfit,float(statistic["FollowROI"]),delta = 100)
            self.assertAlmostEqual(pointOfCfClose,float(statistic["FollowPoints"]),delta = 1000000)
        finally:
            topTable.reversesort = True
            print(topTable)


        pointCloseSum = Statistic.pointCloseSum(mt4Account=mt4Account,brokerID=BrokerId)
        orderClose = Statistic.orderClose(mt4Account=mt4Account,brokerID=BrokerId)
        orderOs = Statistic.orderOs(mt4Account=mt4Account,brokerID=BrokerId)
        standardlotsClose = Statistic.standardlotsClose(mt4Account=mt4Account,brokerID=BrokerId)
        pointProfitCloseMean = Statistic.pointProfitCloseMean(mt4Account=mt4Account,brokerID=BrokerId)
        orderProfitClose = Statistic.orderProfitClose(mt4Account=mt4Account,brokerID=BrokerId)
        orderCs = Statistic.orderCs(mt4Account=mt4Account,brokerID=BrokerId)
        tradePeriod = Statistic.tradePeriod(mt4Account=mt4Account,brokerID=BrokerId)
        #获取:交易概览统计数据
        overView = PrettyTable(["预期/实际","盈亏点数","交易笔数","自主开仓笔数","交易手数","平均获利点数","胜出交易笔数","跟随开仓笔数","交易周期"])
        overView.add_row(["预期结果",pointCloseSum,orderClose,orderOs,standardlotsClose,pointProfitCloseMean,orderProfitClose,orderCs,tradePeriod])
        overView.add_row(["实际结果",statistic["Point"],statistic["Orders"],statistic["SelfOrders"],statistic["StandardLots"],statistic["AVGPoint"],statistic["WinOrders"],statistic["FollowOrders"],statistic["Weeks"]])
        try:
            #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
            self.assertAlmostEqual(pointCloseSum,float(statistic["Point"]),delta = 2000000)
            self.assertAlmostEqual(orderClose,float(statistic["Orders"]),delta = 100)
            self.assertAlmostEqual(orderOs,float(statistic["SelfOrders"]),delta = 1000000)
            self.assertAlmostEqual(standardlotsClose,float(statistic["StandardLots"]),delta = 1000000)
            self.assertAlmostEqual(pointProfitCloseMean,float(statistic["AVGPoint"]),delta = 1000000)
            self.assertAlmostEqual(orderProfitClose,float(statistic["WinOrders"]),delta = 1000000)
            self.assertAlmostEqual(orderProfitClose,float(statistic["FollowOrders"]),delta = 1000000)
            self.assertAlmostEqual(tradePeriod,statistic["Weeks"],delta = 1000000)
        finally:
            overView.reversesort = True
            print(overView)


    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

