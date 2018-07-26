#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PrestoCompareMongo_tradeScore
# 用例标题: 交易员得分计算
# 预置条件: 
# 测试步骤:
# 预期结果:
# 脚本作者: shencanhui
# 写作日期: 20171211
#=========================================================
import sys,unittest,json,numpy,datetime,time
from dateutil.parser import parse #pip3 install python-dateutil
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,Account,Statistic
from Statistic import t_mt4trades,t_followorders,TD_followorders,t_mt4tradesinfo
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable
from pymongo import MongoClient
from pyhive import presto 
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# import pandas as pd

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
accountData = FMCommon.loadAccountYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()


class UserInfo(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        '''登录followme系统'''
        #生产 piaoyou kvb
        self.login = '210062656'
        self.brokerID = 5
        curr_tiem = datetime.datetime.now() + datetime.timedelta(days=-1)
        self.yesterDay = curr_tiem.strftime('%Y-%m-%d 00:00:00.000')

        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        mongoDB = FMCommon.mongoDB_operater(host=mongoUrl, port = statisticData["mongo_port"])
        for i in mongoDB.fm.mg_result_all.find({"login":self.login}):
            self.mongoList = {}
            for key in statisticData["mongoKeyListAll"]:
                try:
                    value = i[key]
                except KeyError:
                    value = statisticData["keyErr"]
                self.mongoList[key]=value

        #计算保证金
        margin = presto.connect(host=statisticData["prosto_host"],port=statisticData["prosto_port"]).cursor()
        margin.execute("SELECT margin FROM test_t_mt4users where login='%s' and brokerid=%d" % (self.login,self.brokerID))
        #计算实盘跟随人数
        follower_count = presto.connect(host=statisticData["prosto_host"],port=statisticData["prosto_port"]).cursor()
        follower_count.execute("SELECT count(distinct(followaccount)) from test_T_FollowReport  where masteraccount='%s' and masterbrokerid=%d and endDate='1970-01-01 00:00:00.0'" % (self.login,self.brokerID))

        self.T_MT4TradesTable = Statistic.getPrestoData(login=self.login,brokerID=self.brokerID,echo=False)
        print("------------------------------------")
        # for i in self.T_MT4TradesTable:
        #     print(i)

        #每张订单收益
        self.deal_profit = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_profit')
        #盈利总额
        self.profit_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='profit_sum')
        #平仓订单收益
        self.profit_close_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='profit_close_sum')
        #近7天平仓订单收益
        self.profit_close_sum_week = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='profit_close_sum_Nday',closeTime=Statistic.n_dayAgo(-7))
        #1周以前的净值，期初净值
        self.deposit_sum_week = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deposit_sum_Nday',closeTime=Statistic.n_dayAgo(-7))
        #近30天平仓订单收益
        self.profit_close_sum_month = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='profit_close_sum_Nday',closeTime=Statistic.n_dayAgo(-30))
        #1月以前的净值，期初净值
        self.deposit_sum_month = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deposit_sum_Nday',closeTime=Statistic.n_dayAgo(-30))
        #亏损总额
        self.loss_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='loss_sum')
        #平仓亏损订单数
        self.deal_loss_close = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_loss_close')
        #平仓盈利订单数
        self.deal_profit_close = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_profit_close')
        #平仓做多盈利笔数
        self.deal_profit_long_close = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_profit_long_close')
        #持仓盈利订单
        self.deal_profit_open = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_profit_open')
        #平仓点数
        self.point_close = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='point_close')
        #平仓盈利点数
        self.point_profit_close = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='point_profit_close')
        #盈利订单总点数，包括持仓
        self.point_profit_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='point_profit_sum')
        #亏损订单总点数，包括持仓
        self.point_loss_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='point_loss_sum')
        #标准差
        self.standard_deviation = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='standard_deviation')
        #持仓时间
        self.time_possession = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='time_possession')
        #交易周期
        self.period_trade = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='period_trade')
        #平仓标准手
        self.standardlots_close = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='standardlots_close')
        #累计入金
        self.deposit_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deposit_sum')
        #净值
        self.equity_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='equity_sum')
        #余额
        self.balance_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='balance_sum')
        #已用保证金
        self.margin = margin.fetchone()[0]
        #实盘跟随人数
        self.follower_count = follower_count.fetchone()[0]
        #该交易员自主平仓订单笔数
        self.deal_os = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_os')
        #跟随平仓订单笔数
        self.deal_cs = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_cs')
        #盈利订单数量，包括持仓
        self.deal_profit_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_profit_sum')
        #亏损订单数量，包括持仓
        self.deal_loss_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_loss_sum')

        # print(self.deposit_sum)
        

    def test_01_FactorProfitEquity(self):
        '''净值利润因子：(平仓盈利金额+持仓盈利金额)/(平仓亏损金额+持仓亏损金额)'''
        print("ddd")
        # """
        item = self.profit_sum/self.loss_sum
        # print(self.profit_sum,self.loss_sum)
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
        print("预期净值利润因子：", item,"   Score: ", ProfitEquityscore)
        print("实际净值利润因子：", self.mongoList["factor_profit_equity"])

    def test_02_RateProfitBalance(self):
        '''历史余额收益率：已平仓订单收益／累计入金'''
        item = self.profit_close_sum / self.deposit_sum
        # print(self.profit_close_sum, self.deposit_sum)
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
        print("预期历史余额收益率：", item,"   Score: ", RateProfitBalance)
        print("实际历史余额收益率：", item)

    def test_03_RateProfitWeek(self):
        '''近7天收益率'''
        item = self.profit_close_sum_week / self.deposit_sum_week
        # print(self.profit_close_sum_week, self.deposit_sum_week)
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
        print("预期近7天收益率：", item,"   Score: ", RateProfitWeek)
        print("实际近7天收益率：", item)

    def test_04_RateProfitMonth(self):
        '''近30天收益率'''
        item = self.profit_close_sum_month / self.deposit_sum_month
        # print(self.profit_close_sum_month, self.deposit_sum_month)
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
        print("预期近30天收益率：", item,"   Score: ", RateProfitMonth)
        print("实际近30天收益率：", item)

    def test_05_RatioProfit(self):
        '''收益对比'''
        item = (self.profit_sum + self.loss_sum) / self.profit_close_sum
        # print(self.profit_sum + self.loss_sum, self.profit_close_sum)
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
        print("预期收益对比：", item,"   Score: ", RatioProfit)
        print("实际收益对比：", item)

    def test_06_Equity(self):
        '''净值'''
        item = self.equity_sum
        # print(self.equity_sum)
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
        print("预期净值：", item,"   Score: ", Equity)
        print("实际净值：", item)

    def test_07_RatePositionMaxHistory(self):
        '''最大资金持仓占比'''
        item = self.margin / self.balance_sum
        # print(self.margin, self.balance_sum)
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
        print("预期最大资金持仓占比：", item,"   Score: ", RatePositionMaxHistory)
        print("实际最大资金持仓占比：", self.mongoList['rate_possession_max_history'])

    def test_08_RatioEdgePoints(self):
        '''极限点数对比'''
        item = max(self.point_close) / min(self.point_close)
        print(max(self.point_close), min(self.point_close))
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
        print("预期极限点数对比：", item,"   Score: ", RatioEdgePoints)
        print("实际极限点数对比：", self.mongoList['ratio_edge_points'])

    def test_09_PeriodTrade(self):
        '''交易周数'''
        item = (datetime.datetime.now() - parse(min(self.period_trade))).days / 7.0
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
        print("预期交易周数：", item,"   Score: ", PeriodTrade)
        print("实际交易周数：", self.mongoList['period_trade'])

    def test_10_Activity(self):
        '''活跃度'''
        item = (parse(Statistic.n_dayAgo(0)) - parse(max(self.period_trade))).days
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
        print("预期活跃度：", item,"   Score: ", Activity)
        print("实际活跃度：", self.mongoList['activity'])

    def test_11_NumberOfFollow(self):
        '''实盘跟随人数'''
        item = self.follower_count
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
        print("预期实盘跟随人数：", item,"   Score: ", NumberOfFollow)
        print("实际实盘跟随人数：", self.mongoList['report_followerscount_actual_following'])

    def test_12_PointsLossMaxClose(self):
        '''平仓最大亏损点数'''
        item = min(self.point_close)
        # print(item)
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
        print("预期平仓最大亏损点数：", item,"   Score: ", PointsLossMaxClose)
        print("实际平仓最大亏损点数：", self.mongoList['point_loss_close_max'])

    def test_13_RatioAveragePoints(self):
        '''平均点数对比（所有盈利订单点数/所有盈利订单数）／（所有亏损订单点数/所有亏损订单数）'''
        item = (self.point_profit_sum / self.deal_profit_sum) / (self.point_loss_sum / self.deal_loss_sum)
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
        print("预期平均点数对比：", item,"   Score: ", RatioAveragePoints)
        print("实际平均点数对比：", self.mongoList['ratio_average_points'])

    def test_14_reTraceMent(self):
        '''再途回撤率（ 已平仓订单总收益+未平仓订单收益-历史已平仓订单最大收益）／（历史已平仓订单最大收益+总入金）'''
        historyMaxProfit = 0
        sum = 0
        for i in range(len(self.deal_profit)):
            sum += self.deal_profit[i]
            if historyMaxProfit < sum:
                historyMaxProfit = sum
        item = (self.profit_sum + self.loss_sum - historyMaxProfit) / (historyMaxProfit + self.deposit_sum)
        # print(self.profit_sum,self.loss_sum,historyMaxProfit,historyMaxProfit,self.deposit_sum)
        # print(item)
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
        print("预期再途回撤率：", item,"   Score: ", ReTraceMent)
        print("实际再途回撤率：", self.mongoList['rate_retracement_max'])

    def test_15_CountWeekProfit(self):
        '''连续收益周数'''
        item = 0
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
        print("预期连续收益周数：", item,"   Score: ", CountWeekProfit)
        print("实际连续收益周数：", self.mongoList['continuous_weeks_profit'])

        print("")
        print("-------------------------------------")
        print("AccountInfo: " + self.login,"---- brokerID: "+ str(self.brokerID))
        print("Total Score:", ProfitEquityscore + RateProfitBalance + RateProfitWeek + RateProfitMonth + RatioProfit + Equity + 
            RatePositionMaxHistory + RatioEdgePoints + PeriodTrade + Activity + NumberOfFollow + PointsLossMaxClose + RatioAveragePoints + ReTraceMent + CountWeekProfit)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

