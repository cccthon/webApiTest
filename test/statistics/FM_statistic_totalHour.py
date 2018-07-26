#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_statistic_hourAll
# 用例标题: 交易小时统计。 统计某个小时的所有数据。
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
        # 生产 piaoyou
        login = '210062988'    #hour = 17
        brokerID = 5
        #最近存在交易数据帐号
        # login = '830005'  #交易员
        # brokerID = 5
        # login = '830014'  #跟随者
        # brokerID = 5

        #endtime为 mongo统计数据的截止时间。如果不传，presto会统计到当前的所有数据
        #去monggoDB中updatets字段即可。
        endTime='2018-06-12 21:53:18.0'
        #查询几点的数据
        hour = 17
        table = 'mg_result_hour'
        mongoFind = {"login": login,"close_hour": hour}

        ##获取mongo DB数据库中的相关指标值
        mongoUrl = "mongodb://%s:%s@%s" % (statisticConf.mongo_userName, statisticConf.mongo_passwd, statisticConf.mongo_host)
        self.mongoList = Statistic.mongoData(host = mongoUrl, port = statisticConf.mongo_port,db=statisticConf.mongo_DB,table=table,find = mongoFind)
        #从presto读取原始数据，计算后得出的指标值保存到字典
        self.prestoList = Statistic.prestoData(login = login, brokerID = brokerID,endTime=endTime,hour=hour)

        print("+" * 100)
        print("Test info: mongoUrl -",mongoUrl,statisticConf.mongo_port,table)
        print("Test info: prestoUrl -",statisticConf.sqlalchemy_presto)
        print("Test info: login -",login," brokerID -", brokerID)
        print("+" * 100)


    def test_1_money_close(self):
        """收益金额"""
        self.assertAlmostEqual(sum(self.prestoList.money_close), self.mongoList.money_close,delta=0.1)

    def test_2_money_profit_short_close(self):
        """做空盈利订单收益"""
        self.assertEqual(sum(self.prestoList.money_profit_short_close), self.mongoList.money_profit_short_close)

    def test_3_money_loss_short_close(self):
        """做空亏损订单收益"""
        self.assertEqual(sum(self.prestoList.money_loss_short_close), self.mongoList.money_loss_short_close)

    def test_4_money_profit_long_close(self):
        """做多盈利订单收益"""
        self.assertAlmostEqual(sum(self.prestoList.money_profit_long_close), self.mongoList.money_profit_long_close,delta=0.1)

    def test_5_money_loss_long_close(self):
        """做多亏损订单收益"""
        self.assertAlmostEqual(sum(self.prestoList.money_loss_long_close), self.mongoList.money_loss_long_close,delta=0.1)

    def test_6_point_close(self):
        """平仓点数"""
        self.assertAlmostEqual(sum(self.prestoList.point_close), self.mongoList.point_close,delta=0.1)

    def test_7_point_profit_short_close(self):
        """做空盈利订单点数"""
        self.assertAlmostEqual(sum(self.prestoList.point_profit_short_close), self.mongoList.point_profit_short_close,delta=0.1)

    def test_8_point_loss_short_close(self):
        """做空亏损订单点数"""
        self.assertEqual(sum(self.prestoList.point_loss_short_close), self.mongoList.point_loss_short_close)

    def test_9_point_profit_long_close(self):
        """做多盈利订单点数"""
        self.assertAlmostEqual(sum(self.prestoList.point_profit_long_close), self.mongoList.point_profit_long_close,delta=0.1)

    def test_10_point_loss_long_close(self):
        """做多亏损订单点数"""
        self.assertAlmostEqual(sum(self.prestoList.point_loss_long_close), self.mongoList.point_loss_long_close,delta=0.1)

    def test_11_standardlots_short_close(self):
        """做空标准手"""
        self.assertEqual(sum(self.prestoList.standardlots_short_close), self.mongoList.standardlots_short_close)

    def test_12_standardlots_long_close(self):
        """做多标准手"""
        self.assertAlmostEqual(sum(self.prestoList.standardlots_long_close), self.mongoList.standardlots_long_close,delta=0.1)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

