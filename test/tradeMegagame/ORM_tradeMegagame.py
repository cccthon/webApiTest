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
import sys,unittest,json,numpy,datetime,time
from dateutil.parser import parse #pip3 install python-dateutil
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeMegagame")
import Auth,FMCommon,Common,Account,TradeMegagame
# from TradeMegagame import T_mt4trades,T_followorders,TD_followorders,T_mt4tradesinfo,T_followreport
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
    def setUp(self):
        '''登录followme系统'''
        #生产 十年一剑1688
        self.login = '2100000007'
        self.brokerID = 1
        curr_tiem = datetime.datetime.now() + datetime.timedelta(days=-1)
        self.yesterDay = curr_tiem.strftime('%Y-%m-%d 00:00:00.000')

        self.T_MT4TradesTable = TradeMegagame.getMssqlData(login=self.login,brokerID=self.brokerID,echo=True)
        # print(self.T_MT4TradesTable)

        #平仓收益
        self.profit_close = TradeMegagame.statisticQuota(table=self.T_MT4TradesTable,quota='profit_close')
        # #交易手数
        self.standard_lots = TradeMegagame.statisticQuota(table=self.T_MT4TradesTable,quota='standard_lots')
        # print(self.standard_lots)
        #交易笔数
        self.orders = TradeMegagame.statisticQuota(table=self.T_MT4TradesTable,quota='orders')
        # print(self.orders)
        # 实盘跟随人数
        # self.follower_count = TradeMegagame.statisticQuota(table=self.T_MT4TradesTable,quota='follower_count')
        # print(self.follower_count)


    def test_1_factor_profit_equity_all(self):
        '''净值利润因子：(平仓盈利金额+持仓盈利金额)/(平仓亏损金额+持仓亏损金额)'''
        #取小数点后17位
        print("hahahah")

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

