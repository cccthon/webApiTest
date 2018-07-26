#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_TradeScore_001_001
# 用例标题: 交易员评分
# 预置条件: 
# 测试步骤:
#   1.传入mt4帐号、brokerid
#   2.分别计算每个指标的得分值
#   3.统计总得分
# 预期结果:
#   1.得分与tradescore表的得分一致
# 脚本作者: shencanhui
# 写作日期: 20171102
#=========================================================
import sys,unittest,json,requests,pymssql
sys.path.append("../../lib/common")
sys.path.append("../../lib/tradeScore")
sys.path.append("../../lib/WebAPI")
import FMCommon,Auth,Account
from socketIO_client import SocketIO
from base64 import b64encode
import numpy as np

tradeScoreData = FMCommon.loadTradeScoreYML()
webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
accountData = FMCommon.loadAccountYML()

class tradeScore(unittest.TestCase):
    def setUp(self):

        #申明需要测试的经纪商。1为pico
        self.brokerID = 102
        #获取指定经纪商的mt4账号。当前为：pcio
        self.trademt4Account = '4563597'

    def test_01_FactorProfitEquity(self):
        '''净值利润因子'''
        print("")
        expectFactorProfitEquity = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectFactorProfitEquity'])
        for mtuple in expectFactorProfitEquity:
            for item in mtuple:
                print("预期净值利润因子：", item)
        global ProfitEquityscore
        ProfitEquityscore=0
        if   1.01 <= abs(item) < 1.20:
            ProfitEquityscore = 100 * 20 / 100
        elif 1.20 <= abs(item) < 1.40:
            ProfitEquityscore = 100 * 40 / 100
        elif 1.40 <= abs(item) < 1.60:
            ProfitEquityscore = 100 * 60 / 100
        elif 1.60 <= abs(item) < 1.80:
            ProfitEquityscore = 100 * 80 / 100
        elif 1.80 <= abs(item) < 1000:
            ProfitEquityscore = 100 * 100 / 100
        print("Score: ", ProfitEquityscore)

        actualFactorProfitEquity = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualFactorProfitEquity']+self.trademt4Account)
        for mtuple in actualFactorProfitEquity:
            for item in mtuple:
                print("实际净值利润因子：", item)
        # self.assertEqual(expectFactorProfitEquity,actualFactorProfitEquity)

    def test_02_RateProfitBalance(self):
        '''历史余额收益率'''
        print("")
        expectRateProfitBalance = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectRateProfitBalance'])
        for mtuple in expectRateProfitBalance:
            for item in mtuple:
                print("预期历史余额收益率：", item)
        global RateProfitBalance
        RateProfitBalance=0
        if   0.01 <= item * 100 < 10:
            RateProfitBalance = 50 * 20 / 100
        elif 10 <= item * 100 < 20:
            RateProfitBalance = 50 * 40 / 100
        elif 20 <= item * 100 < 30:
            RateProfitBalance = 50 * 60 / 100
        elif 30 <= item * 100 < 40:
            RateProfitBalance = 50 * 80 / 100
        elif 40 <= item * 100 < 1000:
            RateProfitBalance = 50 * 100 / 100
        print("Score: ", RateProfitBalance)

        actualRateProfitBalance = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualRateProfitBalance']+self.trademt4Account)
        for mtuple in actualRateProfitBalance:
            for item in mtuple:
                print("实际历史余额收益率：", item)
        # self.assertEqual(expectRateProfitBalance,actualRateProfitBalance)

    def test_03_RateProfitWeek(self):
        '''近7天收益率'''
        print("")
        expectRateProfitWeek = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectRateProfitWeek'])
        for mtuple in expectRateProfitWeek:
            for item in mtuple:
                print("预期近7天收益率：", item)
        global RateProfitWeek
        RateProfitWeek=0
        if  0.01 <= item * 100 < 0.5:
            RateProfitWeek = 50 * 20 / 100
        elif 0.5 <= item * 100 < 1:
            RateProfitWeek = 50 * 40 / 100
        elif 1 <= item * 100 < 1.5:
            RateProfitWeek = 50 * 60 / 100
        elif 1.5 <= item * 100 < 2:
            RateProfitWeek = 50 * 80 / 100
        elif 2 <= item * 100 < 1000:
            RateProfitWeek = 50 * 100 / 100
        print("Score: ",RateProfitWeek)

        actualRateProfitWeek = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualRateProfitWeek']+self.trademt4Account)
        for mtuple in actualRateProfitWeek:
            for item in mtuple:
                print("实际近7天收益率：", item)
        # self.assertEqual(expectRateProfitWeek,actualRateProfitWeek)

    def test_04_RateProfitMonth(self):
        '''近30天收益率'''
        print("")
        expectRateProfitMonth = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectRateProfitMonth'])
        for mtuple in expectRateProfitMonth:
            for item in mtuple:
                print("预期近30天收益率：", item)
        global RateProfitMonth
        RateProfitMonth=0
        if  0.01 <= item * 100 < 2:
            RateProfitMonth = 50 * 20 / 100
        elif 2 <= item * 100 < 4:
            RateProfitMonth = 50 * 40 / 100
        elif 4 <= item * 100 < 6:
            RateProfitMonth = 50 * 60 / 100
        elif 6 <= item * 100 < 8:
            RateProfitMonth = 50 * 80 / 100
        elif 8 <= item * 100 < 1000:
            RateProfitMonth = 50 * 100 / 100
        print("Score: ",RateProfitMonth)

        actualRateProfitMonth = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualRateProfitMonth']+self.trademt4Account)
        for mtuple in actualRateProfitMonth:
            for item in mtuple:
                print("实际近30天收益率：", item)
        # self.assertEqual(expectRateProfitMonth,actualRateProfitMonth)

    def test_05_RatioProfit(self):
        '''收益对比'''
        print("")
        expectRatioProfit = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectRatioProfit'])
        for mtuple in expectRatioProfit:
            for item in mtuple:
                print("预期收益对比：", item)
        global RatioProfit
        RatioProfit=0
        if  1.01 <= abs(item) < 1.20:
            RatioProfit = 50 * 20 / 100
        elif 1.20 <= abs(item) < 1.40:
            RatioProfit = 50 * 40 / 100
        elif 1.40 <= abs(item) < 1.60:
            RatioProfit = 50 * 60 / 100
        elif 1.60 <= abs(item) < 1.80:
            RatioProfit = 50 * 80 / 100
        elif 1.80 <= abs(item) < 1000:
            RatioProfit = 50 * 100 / 100
        print("Score: ",RatioProfit)

        actualRatioProfit = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualRatioProfit']+self.trademt4Account)
        for mtuple in actualRatioProfit:
            for item in mtuple:
                print("实际收益对比：", item)
        # self.assertEqual(expectRatioProfit,actualRatioProfit)

    def test_06_Equity(self):
        '''净值'''
        print("")
        expectEquity = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectEquity'])
        for mtuple in expectEquity:
            for item in mtuple:
                print("预期净值：", item)
        global Equity
        Equity=0
        if  0 <= item < 2000:
            Equity = 50 * 20 / 100
        elif 2000 <= item < 5000:
            Equity = 50 * 40 / 100
        elif 5000 <= item < 10000:
            Equity = 50 * 60 / 100
        elif 10000 <= item < 20000:
            Equity = 50 * 80 / 100
        elif 20000 <= item < 1000000000:
            Equity = 50 * 100 / 100
        print("Score: ",Equity)

        actualEquity = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualEquity']+self.trademt4Account)
        for mtuple in actualEquity:
            for item in mtuple:
                print("实际净值：", item)
        # self.assertEqual(expectEquity,actualEquity)

    def test_07_RatePositionMaxHistory(self):
        '''最大资金持仓占比'''
        print("")
        expectRatePositionMaxHistory = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectRatePositionMaxHistory'])
        for mtuple in expectRatePositionMaxHistory:
            for item in mtuple:
                print("预期最大资金持仓占比：", item)
        global RatePositionMaxHistory
        RatePositionMaxHistory=0
        if  10 <= item * 100 < 20:
            RatePositionMaxHistory = -(50 * 20 / 100)
        elif 20 <= item * 100 < 30:
            RatePositionMaxHistory = -(50 * 40 / 100)
        elif 30 <= item * 100 < 40:
            RatePositionMaxHistory = -(50 * 60 / 100)
        elif 40 <= item * 100 < 50:
            RatePositionMaxHistory = -(50 * 80 / 100)
        elif 50 <= item * 100 < 100000:
            RatePositionMaxHistory = -(50 * 100 / 100)
        else:
            RatePositionMaxHistory = RatePositionMaxHistory
        print("Score: ", RatePositionMaxHistory)

        actualRatePositionMaxHistory = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualRatePositionMaxHistory']+self.trademt4Account)
        for mtuple in actualRatePositionMaxHistory:
            for item in mtuple:
                print("实际最大资金持仓占比：", item)
        # self.assertEqual(expectRatePositionMaxHistory,actualRatePositionMaxHistory)

    def test_08_RatioEdgePoints(self):
        '''极限点数对比'''
        print("")
        expectRatioEdgePoints = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectRatioEdgePoints'])
        for mtuple in expectRatioEdgePoints:
            for item in mtuple:
                print("预期极限点数对比：", item)
        global RatioEdgePoints
        RatioEdgePoints=0
        if  0 <= abs(item) < 0.2:
            RatioEdgePoints = 50 * 20 / 100
        elif 0.2 <= abs(item) < 0.4:
            RatioEdgePoints = 50 * 40 / 100
        elif 0.4 <= abs(item) < 0.6:
            RatioEdgePoints = 50 * 60 / 100
        elif 0.6 <= abs(item) < 0.8:
            RatioEdgePoints = 50 * 80 / 100
        elif 0.8 <= abs(item) < 10000000:
            RatioEdgePoints = 50 * 100 / 100
        print("Score: ",RatioEdgePoints)

        actualRatioEdgePoints = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualRatioEdgePoints']+self.trademt4Account)
        for mtuple in actualRatioEdgePoints:
            for item in mtuple:
                print("实际极限点数对比：", item)
        # self.assertEqual(expectRatioEdgePoints,actualRatioEdgePoints)

    def test_09_PeriodTrade(self):
        '''交易周数'''
        print("")
        expectPeriodTrade = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectPeriodTrade'])
        for mtuple in expectPeriodTrade:
            for item in mtuple:
                print("预期交易周数：", item)
        global PeriodTrade
        PeriodTrade=0
        if  0 <= item < 4:
            PeriodTrade = 50 * 20 / 100
        elif 4 <= item < 8:
            PeriodTrade = 50 * 40 / 100
        elif 8 <= item < 12:
            PeriodTrade = 50 * 60 / 100
        elif 12 <= item < 16:
            PeriodTrade = 50 * 80 / 100
        elif 16 <= item < 10000000:
            PeriodTrade = 50 * 100 / 100
        print("Score: ", PeriodTrade)

        actualPeriodTrade = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualPeriodTrade']+self.trademt4Account)
        for mtuple in actualPeriodTrade:
            for item in mtuple:
                print("实际交易周数：", item)
        # self.assertEqual(expectPeriodTrade,actualPeriodTrade)

    def test_10_Activity(self):
        '''活跃度'''
        print("")
        expectActivity = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectActivity'])
        for mtuple in expectActivity:
            for item in mtuple:
                print("预期活跃度：", item)
        global Activity
        Activity=0
        if  14 <= abs(item) < 100000:
            Activity = 50 * 20 / 100
        elif 7 <= abs(item) < 14:
            Activity = 50 * 40 / 100
        elif 5 <= abs(item) < 7:
            Activity = 50 * 60 / 100
        elif 2 <= abs(item) < 5:
            Activity = 50 * 80 / 100
        elif 0 <= abs(item) < 2:
            Activity = 50 * 100 / 100
        print("Score: ", Activity)

        actualActivity = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualActivity']+self.trademt4Account)
        for mtuple in actualActivity:
            for item in mtuple:
                print("实际活跃度：", item)
        # self.assertEqual(expectActivity,actualActivity)

    def test_11_NumberOfFollow(self):
        '''实盘跟随人数'''
        print("")
        expectNumberOfFollow = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectNumberOfFollow'])
        for mtuple in expectNumberOfFollow:
            for item in mtuple:
                print("预期实盘跟随人数：", item)
        global NumberOfFollow
        NumberOfFollow=0
        if  1 <= abs(item) < 5:
            NumberOfFollow = 50 * 20 / 100
        elif 5 <= abs(item) < 10:
            NumberOfFollow = 50 * 40 / 100
        elif 10 <= abs(item) < 20:
            NumberOfFollow = 50 * 60 / 100
        elif 20 <= abs(item) < 50:
            NumberOfFollow = 50 * 80 / 100
        elif 50 <= abs(item) < 1000000:
            NumberOfFollow = 50 * 100 / 100
        print("Score: ", NumberOfFollow)

        actualNumberOfFollow = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualNumberOfFollow']+self.trademt4Account)
        for mtuple in actualNumberOfFollow:
            for item in mtuple:
                print("实际实盘跟随人数：", item)
        # self.assertEqual(expectNumberOfFollow,actualNumberOfFollow)

    def test_12_PointsLossMaxClose(self):
        '''平仓最大亏损点数'''
        print("")
        expectPointsLossMaxClose = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectPointsLossMaxClose'])
        for mtuple in expectPointsLossMaxClose:
            for item in mtuple:
                print("预期平仓最大亏损点数：", item)
        global PointsLossMaxClose
        PointsLossMaxClose=0
        if  0 <= abs(item) < 50:
            PointsLossMaxClose = -(50 * 20 / 100)
        elif 50 <= abs(item) < 100:
            PointsLossMaxClose = -(50 * 40 / 100)
        elif 100 <= abs(item) < 150:
            PointsLossMaxClose = -(50 * 60 / 100)
        elif 150 <= abs(item) < 200:
            PointsLossMaxClose = -(50 * 80 / 100)
        elif 200 <= abs(item) < 1000000:
            PointsLossMaxClose = -(50 * 100 / 100)
        print("Score: ", PointsLossMaxClose)

        actualPointsLossMaxClose = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualPointsLossMaxClose']+self.trademt4Account)
        for mtuple in actualPointsLossMaxClose:
            for item in mtuple:
                print("实际平仓最大亏损点数：", item)
        # self.assertEqual(expectPointsLossMaxClose,actualPointsLossMaxClose)

    def test_13_RatioAveragePoints(self):
        '''平均点数对比'''
        print("")
        expectRatioAveragePoints = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectRatioAveragePoints'])
        for mtuple in expectRatioAveragePoints:
            for item in mtuple:
                print("预期平均点数对比：", item)
        global RatioAveragePoints
        RatioAveragePoints=0
        if  0 <= abs(item) < 0.2:
            RatioAveragePoints = 100 * 20 / 100
        elif 0.2 <= abs(item) < 0.4:
            RatioAveragePoints = 100 * 40 / 100
        elif 0.4 <= abs(item) < 0.6:
            RatioAveragePoints = 100 * 60 / 100
        elif 0.6 <= abs(item) < 0.8:
            RatioAveragePoints = 100 * 80 / 100
        elif 0.8 <= abs(item) < 1000000:
            RatioAveragePoints = 100 * 100 / 100
        print("Score: ", RatioAveragePoints)

        actualRatioAveragePoints = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualRatioAveragePoints']+self.trademt4Account)
        for mtuple in actualRatioAveragePoints:
            for item in mtuple:
                print("实际平均点数对比：", item)
        # self.assertEqual(expectRatioAveragePoints,actualRatioAveragePoints)

    def test_14_reTraceMent(self):
        '''再途回撤率'''
        print("")
        expectReTraceMent = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + tradeScoreData['expectReTraceMent'])
        for mtuple in expectReTraceMent:
            for item in mtuple:
                if item > 0:
                    print("预期再途回撤率：", 0/item)
                else:
                    print("预期再途回撤率：", item)
        global ReTraceMent
        ReTraceMent=0
        if  0.001 <= abs(item) < 10:
            ReTraceMent = -(50 * 20 / 100)
        elif 10 <= abs(item) < 20:
            ReTraceMent = -(50 * 40 / 100)
        elif 20 <= abs(item) < 30:
            ReTraceMent = -(50 * 60 / 100)
        elif 30 <= abs(item) < 40:
            ReTraceMent = -(50 * 80 / 100)
        elif 40 <= abs(item) < 1000:
            ReTraceMent = -(50 * 100 / 100)
        print("Score: ", ReTraceMent)

        actualReTraceMent = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualReTraceMent']+self.trademt4Account)
        for mtuple in actualReTraceMent:
            for item in mtuple:
                print("实际再途回撤率：", item)
        # self.assertEqual(expectReTraceMent,actualReTraceMent)

    def test_15_CountWeekProfit(self):
        '''连续收益周数'''
        print("")
        expectCountWeekProfit = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql="DECLARE @account VARCHAR(64)=" + self.trademt4Account+ "\n" + "DECLARE @brokerid int=" + str(self.brokerID) + "\n" + tradeScoreData['expectCountWeekProfit'])
        for mtuple in expectCountWeekProfit:
            for item in mtuple:
                print("预期连续收益周数：", item)
        global CountWeekProfit
        CountWeekProfit=0
        if  2 <= item < 3:
            CountWeekProfit = -(50 * 20 / 100)
        elif 3 <= item < 4:
            CountWeekProfit = -(50 * 40 / 100)
        elif 4 <= item < 5:
            CountWeekProfit = -(50 * 60 / 100)
        elif 5 <= item < 6:
            CountWeekProfit = -(50 * 80 / 100)
        elif 6 <= item < 1000:
            CountWeekProfit = -(50 * 100 / 100)
        print("Score: ", CountWeekProfit)

        actualCountWeekProfit = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],
            sql=tradeScoreData['actualCountWeekProfit']+self.trademt4Account)
        for mtuple in actualCountWeekProfit:
            for item in mtuple:
                print("实际连续收益周数：", item)
        # self.assertEqual(expectCountWeekProfit,actualCountWeekProfit)
        print("")
        print("-------------------------------------")
        print("AccountInfo: " + self.trademt4Account,"---- brokerID: "+ str(self.brokerID))
        print("Total Score:", ProfitEquityscore + RateProfitBalance + RateProfitWeek + RateProfitMonth + RatioProfit + Equity + 
            RatePositionMaxHistory + RatioEdgePoints + PeriodTrade + Activity + NumberOfFollow + PointsLossMaxClose + RatioAveragePoints + ReTraceMent + CountWeekProfit)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #将测试订单平掉。平仓
        pass
        #登出followme系统
        #登出followme系统
        # tradeSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.tradeHeaders, printLogs=1)
        # self.assertEqual(tradeSignout.status_code, webAPIData['status_code_200'])

if __name__ == '__main__':
    unittest.main()