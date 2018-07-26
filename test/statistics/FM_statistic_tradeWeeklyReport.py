#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PrestoCompareMongo_tradeWeeklyReport
# 用例标题: 交易周报
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
statisticData = FMCommon.loadStatisticYML()


class UserInfo(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        '''登录followme系统'''

        #生产 piaoyou
        self.login = '210062988'
        self.brokerID = 5
        #A在路上
        # self.login = '78351'
        # self.brokerID = 4
        #跟随者
        # self.login='210060270'
        # self.brokerID=5
        #模拟帐号
        # self.login = '2000125085'
        # self.brokerID = 3

        curr_tiem = datetime.datetime.now() + datetime.timedelta(days=-1)
        self.yesterDay = curr_tiem.strftime('%Y-%m-%d 00:00:00.000')

        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        mongoDB = FMCommon.mongoDB_operater(host=mongoUrl, port = statisticData["mongo_port"])
        # mongoDB = FMCommon.mongoDB_operater(host='mongodb://10.0.0.51:27017', port=27017)
        for i in mongoDB.fm.mg_result_weekofyear.find({"login":self.login,"close_weekofyear": "2018-16"}):
            self.mongoList = {}
            for key in statisticData["mongoKeyListAll"]:
                try:
                    value = i[key]
                except KeyError:
                    value = statisticData["keyErr"]
                self.mongoList[key]=value

        #粉丝人数
        fans = presto.connect(host=statisticData["prosto_host"],port=statisticData["prosto_port"]).cursor()
        fans.execute("SELECT count(1) FROM S_Follower where objectid=(select userid from t_useraccount where mt4account='%s')" % (self.login))

        self.T_MT4TradesTable = Statistic.getPrestoData(login=self.login,brokerID=self.brokerID,echo=False,startTime='2018-04-16 06:00:00.0',endTime='2018-04-23 06:00:00.0')

        #粉丝人数
        self.fans_count = fans.fetchone()[0]
        #每张订单收益
        self.deal_profit = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_profit')
        #平仓总收益
        self.money_close = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='money_close')
        #盈利总额
        self.profit_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='profit_sum')
        #平仓收益总额，平仓订单收益
        self.profit_close_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='profit_close_sum')
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
        #每一笔订单的收益列表
        self.deal_profit_close_list = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_profit_close_list')
        #持仓时间
        self.time_possession = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='time_possession')
        #交易周期
        self.period_trade = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='period_trade')
        #交易周期
        self.deal_openTime_list = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='period_trade',closeTime='1969-01-01 00:00:00.0')
        #平仓标准手
        self.standardlots_close = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='standardlots_close')
        #累计如金
        self.deposit_sum = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deposit_sum')
        #该交易员自主平仓订单笔数
        self.deal_os = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_os')
        #跟随平仓订单笔数
        self.deal_cs = Statistic.statisticQuota(table=self.T_MT4TradesTable,quota='deal_cs')

        # print(self.deposit_sum)

    def test_1_factor_profit_equity_all(self):
        '''净值利润因子：(平仓盈利金额+持仓盈利金额)/(平仓亏损金额+持仓亏损金额)'''
        #取小数点后17位
        self.assertAlmostEqual(abs(self.profit_sum / self.loss_sum),self.mongoList['factor_profit_equity'],delta=0.01)

    def test_2_profit(self):
        '''收益'''
        self.assertAlmostEqual(self.profit_sum + self.loss_sum,self.mongoList['money_close'],delta=0.01)

    def test_3_money_rate(self):
        '''收益率.上一自然周的收益 / 期初余额 + 入金'''
        #期初余额，从mssql数据库读取：SELECT balance from T_TraderDaily_New where traderid='210062988' and brokerid=5 and date='20180415'
        self.assertAlmostEqual((self.profit_sum + self.loss_sum) / (6179.48 + self.deposit_sum) ,self.mongoList['rate_profit_balance_close_bfhists'],delta=0.01)

    def test_4_profit_rate(self):
        '''胜率(week)。赢的订单数/总单数'''
        self.assertAlmostEqual(self.deal_profit_close / (self.deal_profit_close + self.deal_loss_close),self.mongoList['rate_profit'],delta=0.01)

    def test_5_fans_count(self):
        '''粉丝人数'''
        self.assertAlmostEqual(self.fans_count ,self.mongoList['fans_count'],delta=0.01)

    def test_6_deal_close(self):
        '''平仓总订单数,交易笔数'''
        self.assertEqual(self.deal_profit_close + self.deal_loss_close, self.mongoList['deal_close'])

   
    def test_15_rate_retracement_max(self):
        #直接读库，不计算
        '''最大回撤率：(平仓总收益金额+持仓总收益金额-历史累计订单金额最大值)/(历史累计订单金额最大值+累计入金)'''
        hisMaxProfit = 0
        prifitSum = 0
        for i in range(0,len(self.deal_profit)):
            prifitSum += self.deal_profit[i]
            if hisMaxProfit < prifitSum:
                hisMaxProfit = prifitSum
        # print("retracement_max >>>: ","profit_sum: ",self.profit_sum,", loss_sum: ",self.loss_sum,", hisMaxProfit: ",hisMaxProfit,", deposit_sum: ",self.deposit_sum)
        self.assertEqual((self.profit_sum+self.loss_sum-hisMaxProfit)/(hisMaxProfit+self.deposit_sum), self.mongoList['rate_retracement_max'])

    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

