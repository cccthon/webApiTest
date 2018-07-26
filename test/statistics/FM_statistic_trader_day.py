#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PrestoCompareMongo_foll_day
# 用例标题: 近一天统计
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
        #生产环境测试账号
        # 交易员 piaoyou
        # login = '210062988'
        # brokerID = 5

        
        #mongoDB中的close_date
        # close_date = "2017-11-15"
        # #presto需要过滤包括closeDate的数据加经纪商时间。
        # endTime = "2017-11-16 06:00:00.0"
        # print(close_date + " 06:00:00.0")

        
        # #最近存在交易数据帐号
        # login = '830005'
        # brokerID = 5
        ####跟随者帐号
        login='830012'    
        brokerID=5
        
        #mongoDB中的close_date
        close_date = "2018-06-08"
        #presto需要过滤包括closeDate的数据加经纪商时间。
        endTime = "2018-06-09 06:00:00.0"
        print(close_date + " 06:00:00.0")
        table = 'mg_result_day'
        mongoFind = {"login": login,"close_date": close_date}

        #需要根据mongoDB updatets字段确认统计时间。再往前推
        #获取当前天的前一天0点到24点的时间
        curr_tiem = datetime.datetime.now() + datetime.timedelta(days=-2)
        parseTime = datetime.datetime.now() + datetime.timedelta(days=0)
        self.yesterDay =  curr_tiem.strftime('%Y-%m-%d 00:00:00.0')
        self.beforeDawn = parseTime.strftime('%Y-%m-%d 00:00:00.0')
        

        ##获取mongo DB数据库中的相关指标值
        mongoUrl = "mongodb://%s:%s@%s" % (statisticConf.mongo_userName, statisticConf.mongo_passwd, statisticConf.mongo_host)
        self.mongoList = Statistic.mongoData(host = mongoUrl, port = statisticConf.mongo_port,db=statisticConf.mongo_DB,table=table,find = mongoFind)
        #从presto读取原始数据，计算后得出的指标值保存到字典
        self.prestoList = Statistic.prestoData(login = login, brokerID = brokerID,startTime='1970-01-01 00:00:00.1',endTime=endTime)

        print("+" * 100)
        print("Test info: mongoUrl -",mongoUrl,statisticConf.mongo_port,table)
        print("Test info: prestoUrl -",statisticConf.sqlalchemy_presto)
        print("Test info: login -",login," brokerID -", brokerID)
        print("+" * 100)


    # def test_1_money_close(self):
    #     """每日收益金额"""
    #     # print(self.money_close)
    #     self.assertAlmostEqual(sum(self.prestoList.money_close), self.mongoList.money_close,delta=0.1)

    def test_2_money_cs_asum(self):
        """自主收益"""
        print(len(self.prestoList.money_cs))
        self.assertAlmostEqual(sum(self.prestoList.money_cs), self.mongoList.money_cs_asum,delta=0.1)

    def test_3_money_cf_asum(self):
        """跟随收益"""
        self.assertAlmostEqual(sum(self.prestoList.money_cf), self.mongoList.money_cf_asum,delta=0.1)

    def test_4_deposit(self):
        """入金"""
        self.assertAlmostEqual(sum(self.prestoList.deposit), self.mongoList.deposit_asum,delta=0.1)

    def test_5_withdraw(self):
        """出金"""
        self.assertAlmostEqual(abs(sum(self.prestoList.withdraw)), self.mongoList.withdraw_asum,delta=0.1)

    def test_6_rate_ss_profit_balance_close(self):
        """总平仓收益率"""
        self.assertAlmostEqual(sum(self.prestoList.money_close) / sum(self.prestoList.deposit) , self.mongoList.rate_asumasum_profit_balance_close,delta=0.1)

    def test_7_rate_ss_profit_balance_close_self(self):
        """自主平仓收益率"""
        self.assertAlmostEqual(sum(self.prestoList.money_cs) / sum(self.prestoList.deposit) , self.mongoList.rate_asumasum_profit_balance_close_self,delta=0.1)

    def test_8_rate_ss_profit_balance_close_follow(self):
        """跟随平仓收益率"""
        self.assertAlmostEqual(sum(self.prestoList.money_cf) / sum(self.prestoList.deposit) , self.mongoList.rate_asumasum_profit_balance_close_follow,delta=0.1)


    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

