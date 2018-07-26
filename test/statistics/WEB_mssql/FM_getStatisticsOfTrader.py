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

class StatisticsOfTrader(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_1_getStatisticsOfTrader(self):
        '''获取用户的交易账号列表'''
        userID = "148174"
        accountIndex = "2"
        url = webAPIData['hostName']+personalPageData['getStatisticsOfTrader_url1'] + userID+'_'+accountIndex+ personalPageData['getStatisticsOfTrader_url2']
        statsticData=PersonalPage.getStatisticsOfTrader(url,headers=webAPIData['headers'],printLogs=1)
        #请求成功 返回 200
        self.assertEqual(statsticData.status_code,webAPIData['status_code_200'])
        statistic = json.loads(statsticData.text)["data"]
        mt4Account = Statistic.getMt4Account(userID=userID,accountIndex=accountIndex)
        BrokerId = Statistic.BrokerId(userID=userID,accountIndex=accountIndex)

        factorProfitEquity = Statistic.factorProfitEquity(mt4Account=mt4Account,brokerID=BrokerId)
        rateProfit = Statistic.rateProfit(mt4Account=mt4Account,brokerID=BrokerId)
        moneyFollowSum = Statistic.moneyFollowSum(mt4Account=mt4Account,brokerID=BrokerId)
        profitFollowSum = Statistic.profitFollowSum(mt4Account=mt4Account,brokerID=BrokerId)
        # 获取净值利润因子,正在跟随总额与跟随获利总额
        topTable = PrettyTable(["预期/实际","userID","accountIndex","净值利润因子","收益率","正在跟随总额","跟随获利总额"])
        try:
            statstic = json.loads(statsticData.text)["data"]
            topTable.add_row(["预期结果",userID,accountIndex,factorProfitEquity,rateProfit,moneyFollowSum,profitFollowSum])
            topTable.add_row(["实际结果",userID,accountIndex,statstic["ProfitFactor"],statstic["ROI"],statstic["AmountFollowing"],statstic["FollowAllProfits"]])
            #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
            self.assertAlmostEqual(factorProfitEquity,float(statstic["ProfitFactor"]),delta = 2)
            self.assertAlmostEqual(rateProfit,float(statstic["ROI"]),delta = 100)
            # self.assertAlmostEqual(moneyFollowSum,float(statstic["AmountFollowing"]),delta = 1000000)
            # self.assertAlmostEqual(profitFollowSum,float(statstic["FollowAllProfits"]),delta = 1000000)
        finally:
            topTable.reversesort = True
            print(topTable)

        orderProfitClose = Statistic.orderProfitClose(mt4Account=mt4Account,brokerID=BrokerId)
        moneyProfitCloseMean = Statistic.moneyProfitCloseMean(mt4Account=mt4Account,brokerID=BrokerId)
        pointLossCloseMax = Statistic.pointLossCloseMax(mt4Account=mt4Account,brokerID=BrokerId)
        tradePipsSum = Statistic.tradePipsSum(mt4Account=mt4Account,brokerID=BrokerId)
        moneyCloseMean = Statistic.moneyCloseMean(mt4Account=mt4Account,brokerID=BrokerId)
        sharpeRatio = Statistic.sharpeRatio(mt4Account=mt4Account,brokerID=BrokerId)
        #获取交易概览的第一列数据
        oneColumn = PrettyTable(["预期/实际","ME指(废弃，未计算)","盈利交易","平均盈利","最大亏损点数","盈亏点数","预期回报","夏普比率"])
        try:
            statstic = json.loads(statsticData.text)["data"]
            oneColumn.add_row(["预期结果",statstic["FollowmeIndex"],orderProfitClose,moneyProfitCloseMean,pointLossCloseMax,tradePipsSum,moneyCloseMean,sharpeRatio])
            oneColumn.add_row(["实际结果",statstic["FollowmeIndex"],statstic["WinOrders"],statstic["AverageProfit"],statstic["MinPoint"],statstic["Point"],statstic["ExpectedReturn"],statstic["Sharpe"]])
            #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
            self.assertAlmostEqual(orderProfitClose,float(statstic["WinOrders"]),delta = 200)
            self.assertAlmostEqual(moneyProfitCloseMean,float(statstic["AverageProfit"]),delta = 100)
            self.assertAlmostEqual(pointLossCloseMax,float(statstic["MinPoint"]),delta = 1000000)
            self.assertAlmostEqual(tradePipsSum,float(statstic["Point"]),delta = 1000000)
            self.assertAlmostEqual(moneyCloseMean,float(statstic["ExpectedReturn"]),delta = 1000000)
            self.assertAlmostEqual(sharpeRatio,float(statstic["Sharpe"]),delta = 1000000)
        finally:
            oneColumn.reversesort = True
            print(oneColumn)

        orderClose = Statistic.orderClose(mt4Account=mt4Account,brokerID=BrokerId)
        orderProfitLongClose = Statistic.orderProfitLongClose(mt4Account=mt4Account,brokerID=BrokerId)
        moneyLossCloseMean = Statistic.moneyLossCloseMean(mt4Account=mt4Account,brokerID=BrokerId)
        pointProfitCloseMean = Statistic.pointProfitCloseMean(mt4Account=mt4Account,brokerID=BrokerId)
        timePossessionAll = Statistic.timePossessionAll(mt4Account=mt4Account,brokerID=BrokerId)
        standardDeviation = Statistic.standardDeviation(mt4Account=mt4Account,brokerID=BrokerId)
        reTraceMent = Statistic.reTraceMent(mt4Account=mt4Account,brokerID=BrokerId)
        #获取交易概览的第二列数据
        twoColumn = PrettyTable(["预期/实际","交易笔数","做多盈利交易","平均亏损","平均盈利点数","平均持仓时间","标准差","最大回撤"])
        try:
            statstic = json.loads(statsticData.text)["data"]
            twoColumn.add_row(["预期结果",orderClose,orderProfitLongClose,moneyLossCloseMean,pointProfitCloseMean,str(timePossessionAll)+'分钟',standardDeviation,reTraceMent])
            twoColumn.add_row(["实际结果",statstic["Orders"],statstic["WinAndBuyOrders"],statstic["AverageLoss"],statstic["AVGWinPoint"],str(statstic["VHour"])+'小时'+str(statstic["VMinue"])+'分钟',statstic["StandardDeviation"],statstic["VRetracement"]])
            #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
            self.assertAlmostEqual(orderClose,float(statstic["Orders"]),delta = 200)
            self.assertAlmostEqual(orderProfitLongClose,float(statstic["WinAndBuyOrders"]),delta = 100)
            self.assertAlmostEqual(moneyLossCloseMean,float(statstic["AverageLoss"]),delta = 1000000)
            self.assertAlmostEqual(pointProfitCloseMean,float(statstic["AVGWinPoint"]),delta = 1000000)
            self.assertAlmostEqual(timePossessionAll,float(statstic["VHour"]*60+statstic["VMinue"]),delta = 1000000)
            self.assertAlmostEqual(standardDeviation,float(statstic["StandardDeviation"]),delta = 1000000)
            self.assertAlmostEqual(reTraceMent,float(statstic["VRetracement"]),delta = 1000000)
        finally:
            twoColumn.reversesort = True
            print(twoColumn)

        orderLossClose = Statistic.orderLossClose(mt4Account=mt4Account,brokerID=BrokerId)
        orderProfitShortClose = Statistic.orderProfitShortClose(mt4Account=mt4Account,brokerID=BrokerId)
        pointProfitCloseMax = Statistic.pointProfitCloseMax(mt4Account=mt4Account,brokerID=BrokerId)
        pointLossCloseMean = Statistic.pointLossCloseMean(mt4Account=mt4Account,brokerID=BrokerId)
        pointOfCfClose = Statistic.pointOfCfClose(mt4Account=mt4Account,brokerID=BrokerId)
        activity = Statistic.activity(mt4Account=mt4Account,brokerID=BrokerId)
        #获取交易概览的第三列数据
        threeColumn = PrettyTable(["预期/实际","亏损交易","做空盈利交易","最大盈利点数","平均亏损点数","跟随获利点数","活跃度"])
        try:
            statstic = json.loads(statsticData.text)["data"]
            threeColumn.add_row(["预期结果",orderLossClose,orderProfitShortClose,pointProfitCloseMax,pointLossCloseMean,pointOfCfClose,activity])
            threeColumn.add_row(["实际结果",statstic["LoseOrders"],statstic["WinAndSellOrders"],statstic["MaxPoint"],statstic["AVGLosePoint"],statstic["FollowPoint"],statstic["VHour"]])
            #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
            self.assertAlmostEqual(orderLossClose,float(statstic["LoseOrders"]),delta = 200)
            self.assertAlmostEqual(orderProfitShortClose,float(statstic["WinAndSellOrders"]),delta = 100)
            self.assertAlmostEqual(pointProfitCloseMax,float(statstic["MaxPoint"]),delta = 1000000)
            self.assertAlmostEqual(pointLossCloseMean,float(statstic["AVGLosePoint"]),delta = 1000000)
            self.assertAlmostEqual(pointOfCfClose,float(statstic["FollowPoint"]),delta = 1000000)
            self.assertAlmostEqual(activity,statstic["VHour"],delta = 1000000)
        finally:
            threeColumn.reversesort = True
            print(threeColumn)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

