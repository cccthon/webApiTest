#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PrestoCompareMongo_foll_day
# 用例标题: 跟随者近一天统计
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
# from Statistic import t_mt4trades,t_followorders,TD_followorders,t_mt4tradesinfo
# from socketIO_client import SocketIO
# from base64 import b64encode
# from prettytable import PrettyTable
# from pymongo import MongoClient
# from pyhive import presto
# from sqlalchemy import *
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from GetPeriodStartTime import GetPeriodStartTime


webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
accountData = FMCommon.loadAccountYML()
commonData = FMCommon.loadCommonYML()
statisticConf = FMCommon.loadStatisticYML()


class UserInfo(unittest.TestCase):
    @classmethod
    def setUpClass(self):

        '''登录followme系统'''
        self.login = '81144'#'32829' #'409987775' #'210060270'
        self.brokerID =4#6
        # #最近存在交易数据帐号
        # self.login = '2100000014'
        # self.brokerID = 1

        table = 'mg_result_all'
        mongoFind = {"login": self.login}

        curr_tiem = datetime.datetime.now() + datetime.timedelta(days=-1)
        self.yesterDay = '2018-04-28 00:00:00'
            #curr_tiem.strftime('%Y-%m-%d %H:%M:%S')
        self.period=30

        initialTime=datetime.datetime.strptime(self.yesterDay,'%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")

        self.bjStarTime = GetPeriodStartTime.getPeriodStartTime(initialTime=initialTime,
                                                           period=self.period, brokerid=self.brokerID, timeType='start')

        self.bjEndTime=GetPeriodStartTime.getPeriodStartTime(initialTime=initialTime,
                                                           period=self.period, brokerid=self.brokerID, timeType='end')
        print(self.bjStarTime)
        print(self.bjEndTime)

        ##获取mongo DB数据库中的相关指标值
        mongoUrl = "mongodb://%s:%s@%s" % (statisticConf.mongo_userName, statisticConf.mongo_passwd, statisticConf.mongo_host)
        self.mongoList = Statistic.mongoData(host = mongoUrl, port = statisticConf.mongo_port,db=statisticConf.mongo_DB,table=table,find = mongoFind)
        #从presto读取原始数据，计算后得出的指标值保存到字典
        self.prestoList = Statistic.prestoData(login=self.login,brokerID=self.brokerID,startTime=self.bjStarTime,endTime=self.bjEndTime)

        print("+" * 100)
        print("Test info: mongoUrl -",mongoUrl,statisticConf.mongo_port,table)
        print("Test info: prestoUrl -",statisticConf.sqlalchemy_presto)
        print("Test info: login -",self.login," brokerID -", self.brokerID)
        print("+" * 100)
        
    def test_1_deal_close(self):
        if self.period == 1:
            '''交易笔数'''
            # print('交易笔数 和 deal_close 对比')
            # print(self.mongoList.deal_close_day'])
            self.assertAlmostEqual(len(self.prestoList.deal_close),self.mongoList.deal_close_day,delta=0.01)

        if self.period == 7:
            '''交易笔数'''
            # print('交易笔数 和 deal_close 对比')
            # print(self.mongoList.deal_close_week)
            self.assertAlmostEqual(len(self.prestoList.deal_close),self.mongoList.deal_close_week,delta=0.01)

        if self.period == 30:
            '''交易笔数'''
            # print('交易笔数 和 deal_close 对比 '+str(self.login)+'经纪商 '+str(self.brokerID))
            # print(self.mongoList.deal_close_month)
            self.assertAlmostEqual(len(self.prestoList.deal_close),self.mongoList.deal_close_month,delta=0.01)

    def test_2_point_close(self):
        if self.period == 1:
            '''盈亏点数'''
            # print('盈亏点数 和 point_close_day 对比 '+str(self.login)+'经纪商 '+str(self.brokerID))
            # print(self.mongoList.point_close_day)
            self.assertAlmostEqual(sum(self.prestoList.point_close),self.mongoList.point_close_day,delta=0.01)

        if self.period == 7:
            '''盈亏点数'''
            # print('盈亏点数 和 point_close_week 对比 '+str(self.login)+'经纪商 '+str(self.brokerID))
            # print(self.mongoList.point_close_week)
            self.assertAlmostEqual(sum(self.prestoList.point_close),self.mongoList.point_close_week,delta=0.01)

        if self.period == 30:
            '''盈亏点数'''
            # print('盈亏点数 和 point_close_month 对比 '+str(self.login)+'经纪商 '+str(self.brokerID))
            # print(self.mongoList.point_close_month)
            self.assertAlmostEqual(sum(self.prestoList.point_close),self.mongoList.point_close_month,delta=0.01)

    def test_3_money_follow_close(self):
        if self.period == 1:
            '''跟随获利'''
            # print('跟随获利 和 money_cf_day 对比'+str(self.login)+'经纪商 '+str(self.brokerID))
            # print(self.mongoList.money_cf_day)
            self.assertAlmostEqual(sum(self.prestoList.money_cf),self.mongoList.money_cf_day,delta=0.01)

        if self.period == 7:
            '''跟随获利'''
            # print('跟随获利 和 money_follow_close_week 对比'+str(self.login)+'经纪商 '+str(self.brokerID))
            # print(self.mongoList.money_cf_week)
            self.assertAlmostEqual(sum(self.prestoList.money_cf),self.mongoList.money_cf_week,delta=0.01)

        if self.period == 30:
            '''跟随获利'''
            # print('跟随获利 和 money_follow_close 对比 '+str(self.login)+'经纪商 '+str(self.brokerID))
            # print(self.mongoList.money_cf_month)
            self.assertAlmostEqual(sum(self.prestoList.money_cf),self.mongoList.money_cf_month,delta=0.01)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

