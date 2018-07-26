#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PrestoCompareMongo_trader_all
# 用例标题: all表统计
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

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
accountData = FMCommon.loadAccountYML()
commonData = FMCommon.loadCommonYML()
statisticConf = FMCommon.loadStatisticYML()

class UserInfo(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #生产 piaoyou  210062988
        # login = '210062988'
        # brokerID = 5
        # login = '210063091'#'32829'#'81144'#'409987775' #'32829' #'210060270'
        # brokerID = 5
        #A在路上
        # login = '3100078351'
        # brokerID = 4
        #跟随者
        # login='210060270'
        # brokerID=5
        #模拟帐号
        # login = '2000125085'
        # brokerID = 3
        #最近存在交易数据帐号
        login = '830005'
        brokerID = 5

        table = 'mg_result_all'
        mongoFind = {"login": login}

        ##获取mongo DB数据库中的相关指标值
        mongoUrl = "mongodb://%s:%s@%s" % (statisticConf.mongo_userName, statisticConf.mongo_passwd, statisticConf.mongo_host)
        self.mongoList = Statistic.mongoData(host = mongoUrl, port = statisticConf.mongo_port,db=statisticConf.mongo_DB,table=table,find = mongoFind)
        #从presto读取原始数据，计算后得出的指标值保存到字典
        self.prestoList = Statistic.prestoData(login = login, brokerID = brokerID)

        #获取mongoDB中数据最后统计时间
        self.updatets = time.strftime("%Y-%m-%d %H:%M:%S.0", time.localtime(self.mongoList.updatets / 1000))

        print("+" * 100)
        print("Test info: mongoUrl -",mongoUrl,statisticConf.mongo_port,table)
        print("Test info: prestoUrl -",statisticConf.sqlalchemy_presto)
        print("Test info: login -",login," brokerID -", brokerID)
        print("+" * 100)

        t_MT4TradesTable = Statistic.getPrestoData(login=login,brokerID=brokerID,endTime=self.updatets)
        tradeTime = []
        for i in t_MT4TradesTable:
            tradeTime.append(i.open_time)
        self.firstTrade = parse(min(tradeTime)).strftime("%Y-%m-%d")

    def setUp(self):
        pass

    def test_01_deal_amount_per_day(self):
        '''日均交易笔数: 总交易笔数 / 首笔开仓到现在的总交易天数（不是有交易的天数，是总的自然天数扣除节假日）'''
        deal_close = len(self.prestoList.deal_close)
        trade_Day = FMCommon.trade_numOfDay(self.firstTrade,parse(self.updatets).strftime("%Y-%m-%d"),webAPIData['dataHost'],webAPIData['dataPost'],webAPIData['database_V3'],webAPIData['dataID'],webAPIData['dataPWD'])
        # print(deal_close)
        # print(self.firstTrade,self.updatets,trade_Day)
        self.assertAlmostEqual(deal_close / trade_Day  ,self.mongoList.deal_amount_per_day,delta=0.01)

    def test_1_factor_profit_equity_all(self):
        '''净值利润因子：(平仓盈利金额+持仓盈利金额)/(平仓亏损金额+持仓亏损金额)'''
        #取小数点后17位
        self.assertAlmostEqual(abs(sum(self.prestoList.money_profit_sum) / sum(self.prestoList.money_loss_sum)),self.mongoList.factor_profit_equity,delta=0.01)

    def test_2_deal_loss_close(self):
        '''平仓亏损订单笔数,亏损交易：平仓亏损笔数之和(亏损:swaps+commission+profit<0)'''
        self.assertEqual(len(self.prestoList.deal_loss_close),self.mongoList.deal_loss_close)
    
    def test_3_deal_profit_close(self):
        '''平仓盈利订单笔数,盈利交易：平仓盈利笔数之和(盈利:swaps+commission+profit>=0)'''
        self.assertEqual(len(self.prestoList.deal_profit_close),self.mongoList.deal_profit_close)

    def test_4_money_profit_os_close_avg(self):
        '''平仓平均盈利金额,，平均盈利：平仓总盈利收益金额/平仓总盈利笔数'''
        self.assertAlmostEqual(sum(self.prestoList.money_profit_close) / len(self.prestoList.deal_profit_close), self.mongoList.money_profit_close_avg,delta=0.1)

    def test_5_point_loss_close_max(self):
        '''平仓最大亏损点数，最大亏损点数'''
        self.assertEqual(min(self.prestoList.point_close), self.mongoList.point_loss_close_min)

    def test_6_point_close(self):
        '''平仓总点数'''
        self.assertAlmostEqual(sum(self.prestoList.point_close), self.mongoList.point_close,delta=0.1)

    def test_7_money_profit_os_close_avg(self):
        '''平仓平均盈亏金额,预期回报：平仓总收益金额/平仓总笔数'''
        self.assertAlmostEqual(sum(self.prestoList.money_close) / (len(self.prestoList.deal_profit_close) + len(self.prestoList.deal_loss_close)), self.mongoList.money_close_avg, delta=0.01)

    def test_8_sharpe_ratio(self):
        '''夏普比率：(平仓平均收益金额)/标准差..'''
        money_close_avg = sum(self.prestoList.money_close)/(len(self.prestoList.deal_close))
        self.assertAlmostEqual((money_close_avg)/numpy.std(self.prestoList.money_close), self.mongoList.sharpe_ratio,delta=0.01)

    def test_9_deal_close(self):
        '''平仓总订单数,交易笔数'''
        self.assertEqual(len(self.prestoList.deal_close), self.mongoList.deal_close)

    def test_10_deal_profit_long_close(self):
        '''平仓做多盈利笔数,做多盈利交易：平仓订单类型(cmd=0)的盈利笔数'''
        self.assertEqual(len(self.prestoList.deal_profit_long_close), self.mongoList.deal_profit_long_close)

    def test_11_money_loss_close_mean(self):
        '''平仓平均亏损金额，平均亏损：平仓总亏损收益金额/平仓亏损订单总数'''
        # print(self.loss_sum, self.deal_loss_close)
        self.assertAlmostEqual(sum(self.prestoList.money_loss_sum) / len(self.prestoList.deal_loss_close), self.mongoList.money_loss_close_avg, delta=0.01)

    def test_12_point_profit_close_avg(self):
        '''平仓平均盈利点数：平仓盈利总点数/平仓盈利总笔数'''
        self.assertAlmostEqual(sum(self.prestoList.point_profit_close) / len(self.prestoList.deal_profit_close), self.mongoList.point_profit_close_avg, delta=0.1)

    def test_13_time_possession_all(self):
        '''平均持仓时间(小时)：平仓订单的总持仓时间/平仓订单总笔数'''
        self.assertAlmostEqual((sum(self.prestoList.time_possession)) / (len(self.prestoList.deal_close)) / 3600, self.mongoList.time_possession_avg / 60,delta=0.1)

    def test_14_standard_deviation(self):
        '''标准差:(每一笔订单的收益金额)'''
        self.assertAlmostEqual(numpy.std(self.prestoList.money_close), float(self.mongoList.standard_deviation),delta=0.2)

    # def test_15_rate_retracement_max(self):
    #     #直接读库，不计算
    #     '''最大回撤率：(平仓总收益金额+持仓总收益金额-历史累计订单金额最大值)/(历史累计订单金额最大值+累计入金)'''
    #     hisMaxProfit = 0
    #     prifitSum = 0
    #     for i in range(0,len(self.prestoList.money_close)):
    #         prifitSum += self.prestoList.money_close[i]
    #         if hisMaxProfit < prifitSum:
    #             hisMaxProfit = prifitSum
    #     print((sum(self.prestoList.money_close), hisMaxProfit,hisMaxProfit, sum(self.prestoList.deposit)))
    #     self.assertEqual((sum(self.prestoList.money_close) - hisMaxProfit)/(hisMaxProfit + sum(self.prestoList.deposit)), self.mongoList['rate_retracement_max'])

    def test_16_deal_profit_short_close(self):
        '''平仓做空盈利笔数，做空盈利交易：平仓订单类型(cmd=1)的盈利笔数：盈利总订单 - 盈利做多订单'''
        self.assertEqual(len(self.prestoList.deal_profit_short_close), self.mongoList.deal_profit_short_close)

    def test_17_point_profit_close_max(self):
        '''平仓最大盈利点数，最大盈利点数'''
        self.assertEqual(max(self.prestoList.point_close), self.mongoList.point_profit_close_max_all)

    def test_18_point_loss_close_avg(self):
        '''平仓平均亏损点数：平仓亏损总点数 / 平仓亏损总笔数'''
        self.assertAlmostEqual(sum(self.prestoList.point_loss_close) / len(self.prestoList.deal_loss_close), self.mongoList.point_loss_close_avg, delta=0.1)

    def test_19_standardlots_close(self):
        '''平仓总标准手'''
        self.assertAlmostEqual(sum(self.prestoList.standardlots_close), self.mongoList.standardlots_close, delta=0.1)
        
    def test_20_period_trade(self):
        '''交易周期：第一笔开仓单的时间到当前时间的周数'''
        self.assertAlmostEqual((datetime.datetime.now() - parse(min(self.prestoList.period_trade))).days / 7.0 , self.mongoList.period_trade, delta=0.8)

    def test_21_rate_asumasum_profit_balance_ln_all(self):
        '''历史余额收益率: 平仓总收益金额/累计入金'''
        self.assertAlmostEqual(sum(self.prestoList.money_close) / sum(self.prestoList.deposit) , self.mongoList.rate_ss_profit_balance_close, delta=0.1)

    # # def test_23_point_of_cf_close(self):
    # #     '''平仓跟随获利点数,sql presto 验证。scoreVerify.sql'''
    # #     self.assertEqual(self.profit_sum + self.loss_sum, self.mongoList['point_followed_close'])

    def test_24_point(self):
        '''盈亏点数：交易员的盈亏点数'''
        self.assertAlmostEqual(sum(self.prestoList.point_close), self.mongoList.point_close, delta=0.1)

    def test_25_point_close_avg(self):
        '''平仓平均点数：平仓总点数/平仓总笔数'''
        self.assertAlmostEqual(sum(self.prestoList.point_close) / len(self.prestoList.deal_close), self.mongoList.point_close_avg, delta=0.1)

    # def test_28_Activity(self):
    #     """活跃度(天)：当前时间距离最近一笔交易的时间(该指标页面废弃，不做测试)"""
    #     activity = (parse(Statistic.n_dayAgo(0)) - parse(max(self.prestoList.period_trade))).total_seconds() / 3600 / 24
    #     self.assertAlmostEqual(activity, self.mongoList.activity, delta=0.6)

    def test_22_money_close(self):
        '''平仓总收益'''
        self.assertAlmostEqual(sum(self.prestoList.money_close), self.mongoList.money_close, delta=0.1)

    def test_29_deposit_sum(self):
        '''入金'''
        self.assertAlmostEqual(sum(self.prestoList.deposit), self.mongoList.deposit, delta=0.1)

    def test_30_withdraw_sum(self):
        '''出金'''
        self.assertAlmostEqual(abs(sum(self.prestoList.withdraw)), self.mongoList.withdraw, delta=0.1)

    def test_31_standardlots_close_avg(self):
        '''平均手数'''
        standardlots_close_avg = sum(self.prestoList.standardlots_close) / len(self.prestoList.deal_close)
        self.assertAlmostEqual(standardlots_close_avg, self.mongoList.standardlots_close_avg, delta=0.1)

    def test_32_money_profit_close_max(self):
        '''最大盈利金额'''
        self.assertAlmostEqual(max(self.prestoList.money_profit_close), self.mongoList.money_profit_close_max, delta=0.1)

    def test_33_money_loss_close_min(self):
        '''最大亏损金额'''
        self.assertAlmostEqual(min(self.prestoList.money_loss_close), self.mongoList.money_loss_close_min, delta=0.1)

    def test_34_standardlots_long_close(self):
        '''做多标准手'''
        self.assertAlmostEqual(sum(self.prestoList.standardlots_long_close), self.mongoList.standardlots_long_close, delta=0.1)

    def test_35_standardlots_short_close(self):
        '''做空标准手'''
        self.assertAlmostEqual(sum(self.prestoList.standardlots_short_close), self.mongoList.standardlots_short_close, delta=0.1)

    def test_36_money_long_close(self):
        '''做多收益金额'''
        self.assertAlmostEqual(sum(self.prestoList.money_long_close), self.mongoList.money_long_close, delta=0.1)

    def test_37_money_short_close(self):
        '''做空收益金额'''
        self.assertAlmostEqual(sum(self.prestoList.money_short_close), self.mongoList.money_short_close, delta=0.1)

    def test_38_standardlots_max(self):
        '''最大手数'''
        self.assertAlmostEqual(max(self.prestoList.standardlots_close), self.mongoList.standardlots_max, delta=0.1)


    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

