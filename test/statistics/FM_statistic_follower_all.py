#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PrestoCompareMongo_foll_all
# 用例标题: 跟随者所有数据统计
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
        '''登录followme系统'''
        #生产 十年一剑1688
        login = '210063091'#'32829'#'81144'#'409987775' #'32829' #'210060270'
        brokerID = 5#6 #4
        #最近存在交易数据帐号
        # login = '2100000014'
        # brokerID = 1

        table = 'mg_result_all'
        mongoFind = {"login": login}

        ##获取mongo DB数据库中的相关指标值
        mongoUrl = "mongodb://%s:%s@%s" % (statisticConf.mongo_userName, statisticConf.mongo_passwd, statisticConf.mongo_host)
        self.mongoList = Statistic.mongoData(host = mongoUrl, port = statisticConf.mongo_port,db=statisticConf.mongo_DB,table=table,find = mongoFind)
        #从presto读取原始数据，计算后得出的指标值保存到字典
        self.prestoList = Statistic.prestoData(login = login, brokerID = brokerID)

        print("+" * 100)
        print("Test info: mongoUrl -",mongoUrl,statisticConf.mongo_port,table)
        print("Test info: prestoUrl -",statisticConf.sqlalchemy_presto)
        print("Test info: login -",login," brokerID -", brokerID)
        print("+" * 100)

    def test_1_deal_close(self):
        '''交易笔数'''
        # print('交易笔数 和 deal_close 对比 '+'账户 '+str(self.login)+'经纪商 '+str(self.brokerID))
        # print(self.mongoList.deal_close)
        self.assertEqual(len(self.prestoList.deal_close),self.mongoList.deal_close)

    def test_2_point_close(self):
        '''跟随者盈亏点数'''
        # print('跟随者盈亏点数 对比 point_close'+'账户 '+str(self.login)+'经纪商 '+str(self.brokerID))
        # print(self.mongoList.point_close)
        self.assertAlmostEqual(sum(self.prestoList.point_close),self.mongoList.point_close,delta=0.001)

    def test_3_point_close_avg(self):
        '''平均获利点数'''
        # print('平均获利点数 对比 point_profit_close_avg'+'盈利点数：'+str(self.point_profit_close)+'盈利单数： ' + str(self.deal_profit_close))
        # print(self.mongoList.point_profit_close_avg)
        self.assertAlmostEqual(sum(self.prestoList.point_profit_close)/len(self.prestoList.deal_profit_close),self.mongoList.point_profit_close_avg,delta=0.01)

    def test_4_deal_profit_close(self):
        '''胜出交易笔数'''
        # print('胜出交易笔数 对比 deal_profit_close'+'账户 '+str(self.login)+'经纪商 '+str(self.brokerID))
        # print(self.mongoList.deal_profit_close)
        self.assertEqual(len(self.prestoList.deal_profit_close),self.mongoList.deal_profit_close)

    def test_5_deal_os(self):
        '''自主开仓笔数'''
        # print('自主开仓笔数 对比 deal_os '+'账户 '+str(self.login)+'经纪商 '+str(self.brokerID))
        # print(self.mongoList.deal_os)
        self.assertEqual(len(self.prestoList.deal_os),self.mongoList.deal_os)

    def test_6_deal_of(self):
        '''跟随开仓笔数'''
        # print('跟随开仓笔数 对比 deal_of'+'账户 '+str(self.login)+'经纪商 '+str(self.brokerID))
        # print(self.mongoList.deal_of)
        self.assertEqual(len(self.prestoList.deal_of),self.mongoList.deal_of)

    def test_7_standardlots_close(self):
        '''交易手数: MT4Trades的standardlots '''
        # print('交易手数 '+'账户 '+str(self.login)+'经纪商 '+str(self.brokerID))
        # print(self.mongoList.standardlots_close)
        self.assertAlmostEqual(sum(self.prestoList.standardlots_close),self.mongoList.standardlots_close,delta = 0.01)

    def test_8_period_trade(self):
        '''交易周期：第一笔开仓单的时间到当前时间的周数'''
        # print('交易周期 对比 period_trade'+'账户 '+str(self.login)+'经纪商 '+str(self.brokerID))
        # print(self.mongoList.period_trade)
        self.assertAlmostEqual((datetime.datetime.now() - parse(min(self.prestoList.period_trade))).days / 7.0 , self.mongoList.period_trade, delta=0.8)

    def test_9_rate_ss_profit_balance_close(self):
        '''收益率'''
        # print('收益率 对比 rate_ss_profit_balance_close'+'账户 '+str(self.login)+'经纪商 '+str(self.brokerID))
        # print(self.mongoList.rate_ss_profit_balance_close)
        self.assertAlmostEqual(sum(self.prestoList.money_close)/sum(self.prestoList.deposit),self.mongoList.rate_ss_profit_balance_close,delta=0.01)

    def test_10_rate_ss_profit_balance_close(self):
        # print('跟随收益率 对比 rate_ss_profit_balance_close_follow '+'账户 '+str(self.login)+'经纪商 '+str(self.brokerID))
        # print(self.money_follow_close_all,self.deposit_sum,self.mongoList.rate_ss_profit_balance_close_follow)
        self.assertAlmostEqual(sum(self.prestoList.money_cf)/sum(self.prestoList.deposit),self.mongoList.rate_ss_profit_balance_close_follow,delta=0.01)

    def test_11_point_cf(self):
        # print('跟随获利点数 对比 point_cf '+'账户 '+str(self.login)+'经纪商 '+str(self.brokerID))
        # print(self.mongoList.point_cf)
        self.assertAlmostEqual(sum(self.prestoList.point_cf),self.mongoList.point_cf,delta=0.01)


    def test_12_deal_close(self):
        # print('订单数 对比 deal_close '+'账户 '+str(self.login)+'经纪商 '+str(self.brokerID))
        # print(self.mongoList.deal_close)
        self.assertEqual(len(self.prestoList.deal_close),self.mongoList.deal_close)

    def test_13_money_cf(self):
        # print('跟随获利 与 money_cf '+'账户 '+str(self.login)+'经纪商 '+str(self.brokerID))
        # print(self.mongoList.money_cf)
        self.assertAlmostEqual(sum(self.prestoList.money_cf),self.mongoList.money_cf,delta=0.01)

    def test_14_standardlots_max(self):
        """最大手数"""
        self.assertAlmostEqual(max(self.prestoList.standardlots_close),self.mongoList.standardlots_max,delta=0.01)

    def test_15_rate_ss_profit_balance_close_self(self):
        """自主收益率"""
        self.assertAlmostEqual(sum(self.prestoList.money_cs)/sum(self.prestoList.deposit),self.mongoList.rate_ss_profit_balance_close_self,delta=0.01)

    def test_16_point_cs(self):
        """自主收益点数"""
        self.assertAlmostEqual(sum(self.prestoList.point_cs),self.mongoList.point_cs,delta=0.01)

    def test_17_money_cs(self):
        """自主收益金额"""
        self.assertAlmostEqual(sum(self.prestoList.money_cs),self.mongoList.money_cs,delta=0.01)

    def test_18_standardlots_cs(self):
        """自主手数"""
        self.assertAlmostEqual(sum(self.prestoList.standardlots_cs),self.mongoList.standardlots_cs,delta=0.01)

    def test_19_standardlots_cf(self):
        """跟随手数"""
        self.assertAlmostEqual(sum(self.prestoList.standardlots_cf),self.mongoList.standardlots_cf,delta=0.01)

    def test_20_deal_cs(self):
        """自主笔数"""
        self.assertAlmostEqual(len(self.prestoList.deal_cs),self.mongoList.deal_cs,delta=0.01)

    def test_21_deal_cf(self):
        """跟随笔数"""
        self.assertAlmostEqual(len(self.prestoList.deal_cf),self.mongoList.deal_cf,delta=0.01)

    def test_22_deal_profit_cs(self):
        """自主盈利笔数"""
        self.assertAlmostEqual(len(self.prestoList.deal_profit_cs),self.mongoList.deal_profit_cs,delta=0.01)

    def test_23_deal_loss_cs(self):
        """自主亏损笔数"""
        self.assertAlmostEqual(len(self.prestoList.deal_loss_cs),self.mongoList.deal_loss_cs,delta=0.01)

    def test_24_deal_profit_cf(self):
        """跟随盈利笔数"""
        self.assertAlmostEqual(len(self.prestoList.deal_profit_cf),self.mongoList.deal_profit_cf,delta=0.01)

    def test_25_deal_loss_cf(self):
        """跟随亏损笔数"""
        self.assertAlmostEqual(len(self.prestoList.deal_loss_cf),self.mongoList.deal_loss_cf,delta=0.01)

    def test_26_money_profit_cs_avg(self):
        """自主平均盈利收益金额"""
        self.assertAlmostEqual(sum(self.prestoList.money_profit_cs) / len(self.prestoList.deal_profit_cs),self.mongoList.money_profit_cs_avg,delta=0.01)

    def test_27_money_profit_cf_avg(self):
        """跟随平均盈利收益金额"""
        self.assertAlmostEqual(sum(self.prestoList.money_profit_cf) / len(self.prestoList.deal_profit_cf),self.mongoList.money_profit_cf_avg,delta=0.01)

    def test_28_money_loss_cs_avg(self):
        """自主平均亏损平均收益金额"""
        self.assertAlmostEqual(sum(self.prestoList.money_loss_cs) / len(self.prestoList.deal_loss_cs),self.mongoList.money_loss_cs_avg,delta=0.01)

    def test_29_money_profit_cf_avg(self):
        """跟随平均亏损平均收益金额"""
        self.assertAlmostEqual(sum(self.prestoList.money_loss_cf) / len(self.prestoList.deal_loss_cf),self.mongoList.money_loss_cf_avg,delta=0.01)


    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

