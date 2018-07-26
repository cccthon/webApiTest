#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PrestoCompareMongo_trader_week
# 用例标题: 交易周统计
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
        #生产 piaoyou
        # login = '2100004852'
        login = '2100000005'
        brokerID = 1
        # userType = 2 ## UserType: 交易员 1 ， 跟随者 2
        table = 'mg_result_all'
        mongoFind = {"login": login}
        self.lastN = 'day'  # day week month
        startTime = '2018-06-06 06:00:00.0'
        endTime = '2018-06-07 06:00:00.0'

        ##获取mongo DB数据库中的相关指标值
        mongoUrl = "mongodb://%s:%s@%s" % (statisticConf.mongo_userName, statisticConf.mongo_passwd, statisticConf.mongo_host)
        self.mongoList = Statistic.mongoData(host = mongoUrl, port = statisticConf.mongo_port,db=statisticConf.mongo_DB,table=table,find = mongoFind)
        #从presto读取原始数据，计算后得出的指标值保存到字典
        self.prestoList = Statistic.prestoData(login = login, brokerID = brokerID,startTime=startTime,endTime=endTime)

        print("+" * 100)
        print("Test info: mongoUrl -",mongoUrl,statisticConf.mongo_port,table)
        print("Test info: prestoUrl -",statisticConf.sqlalchemy_presto)
        print("Test info: login -",login," brokerID -", brokerID)
        print("+" * 100)

    def test_1_money_close(self):
        #收益金额
        if self.lastN == 'day':
            self.assertAlmostEqual(sum(self.prestoList.money_close), self.mongoList.money_close_day,delta=0.1)
        elif self.lastN == 'week':
            self.assertAlmostEqual(sum(self.prestoList.money_close), self.mongoList.money_close_week,delta=0.1)
        elif self.lastN == 'month':
            self.assertAlmostEqual(sum(self.prestoList.money_close), self.mongoList.money_close_month,delta=0.1)

    def test_2_point_close(self):
        #点数
        if self.lastN == 'day':
            self.assertAlmostEqual(sum(self.prestoList.point_close), self.mongoList.point_close_day,delta=0.1)
        elif self.lastN == 'week':
            self.assertAlmostEqual(sum(self.prestoList.point_close), self.mongoList.point_close_week,delta=0.1)
        elif self.lastN == 'month':
            self.assertAlmostEqual(sum(self.prestoList.point_close), self.mongoList.point_close_month,delta=0.1)

    def test_3_deal_close(self):
        #订单数
        if self.lastN == 'day':
            self.assertEqual(len(self.prestoList.deal_close), self.mongoList.deal_close_day)
        elif self.lastN == 'week':
            self.assertEqual(len(self.prestoList.deal_close), self.mongoList.deal_close_week)
        elif self.lastN == 'month':
            self.assertEqual(len(self.prestoList.deal_close), self.mongoList.deal_close_month)

    ###################################################
    #跟随者相关###########
    def test_4_money_cs(self):
        #自主收益金额
        if self.lastN == 'day':
            self.assertAlmostEqual(sum(self.prestoList.money_cs), self.mongoList.money_cs_day,delta=0.1)
        elif self.lastN == 'week':
            self.assertAlmostEqual(sum(self.prestoList.money_cs), self.mongoList.money_cs_week,delta=0.1)
        elif self.lastN == 'month':
            self.assertAlmostEqual(sum(self.prestoList.money_cs), self.mongoList.money_cs_month,delta=0.1)

    def test_5_point_cs(self):
        #自主点数
        if self.lastN == 'day':
            self.assertAlmostEqual(sum(self.prestoList.point_cs), self.mongoList.point_cs_day,delta=0.1)
        elif self.lastN == 'week':
            self.assertAlmostEqual(sum(self.prestoList.point_cs), self.mongoList.point_cs_week,delta=0.1)
        elif self.lastN == 'month':
            self.assertAlmostEqual(sum(self.prestoList.point_cs), self.mongoList.point_cs_month,delta=0.1)

    def test_6_deal_cs(self):
        #自主点数
        if self.lastN == 'day':
            self.assertAlmostEqual(len(self.prestoList.deal_cs), self.mongoList.deal_cs_day,delta=0.1)
        elif self.lastN == 'week':
            self.assertAlmostEqual(len(self.prestoList.deal_cs), self.mongoList.deal_cs_week,delta=0.1)
        elif self.lastN == 'month':
            self.assertAlmostEqual(len(self.prestoList.deal_cs), self.mongoList.deal_cs_month,delta=0.1)


    def test_7_money_cf(self):
        #跟随收益金额
        if self.lastN == 'day':
            self.assertAlmostEqual(sum(self.prestoList.money_cf), self.mongoList.money_cf_day,delta=0.1)
        elif self.lastN == 'week':
            self.assertAlmostEqual(sum(self.prestoList.money_cf), self.mongoList.money_cf_week,delta=0.1)
        elif self.lastN == 'month':
            self.assertAlmostEqual(sum(self.prestoList.money_cf), self.mongoList.money_cf_month,delta=0.1)

    def test_8_point_cf(self):
        #跟随点数
        if self.lastN == 'day':
            self.assertAlmostEqual(sum(self.prestoList.point_cf), self.mongoList.point_cf_day,delta=0.1)
        elif self.lastN == 'week':
            self.assertAlmostEqual(sum(self.prestoList.point_cf), self.mongoList.point_cf_week,delta=0.1)
        elif self.lastN == 'month':
            self.assertAlmostEqual(sum(self.prestoList.point_cf), self.mongoList.point_cf_month,delta=0.1)

    def test_9_deal_cf(self):
        #跟随订单数
        if self.lastN == 'day':
            self.assertAlmostEqual(len(self.prestoList.deal_cf), self.mongoList.deal_cf_day,delta=0.1)
        elif self.lastN == 'week':
            self.assertAlmostEqual(len(self.prestoList.deal_cf), self.mongoList.deal_cf_week,delta=0.1)
        elif self.lastN == 'month':
            self.assertAlmostEqual(len(self.prestoList.deal_cf), self.mongoList.deal_cf_month,delta=0.1)


    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

