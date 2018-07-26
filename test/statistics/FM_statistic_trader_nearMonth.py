#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PrestoCompareMongo_trader_nearMonth
# 用例标题: 近一月统计
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
        # #生产 十年一剑1688
        # self.login = '210062656'
        # self.brokerID = 5
        #生产 piaoyou
        login = '210062988'
        brokerID = 5
        close_month = "2017-11"
        table = 'mg_result_month'
        #mongo过滤条件
        mongoFind = {"login":login,"close_month":close_month}
        #presto 需要过滤数据的时间
        startTime = '2017-11-01 06:00:00.0'
        endTime = '2017-11-30 06:00:00.0'

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
        '''近一月收益金额'''
        self.assertAlmostEqual(sum(self.prestoList.money_close), self.mongoList.money_close,delta=0.1)

    def test_2_money_close(self):
        '''近一月盈亏点数'''
        self.assertAlmostEqual(sum(self.prestoList.point_close), self.mongoList.point_close,delta=0.05)


    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

