#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_statistic_oenTIme_totalHour
# 用例标题: opentime hour表统计
# 预置条件: 
# 测试步骤:
# 预期结果:
# 脚本作者: shencanhui
# 写作日期: 20180711
#=========================================================
import sys
import unittest
import time
import numpy
sys.path.append("../../lib/common")
sys.path.append("../../lib/statistic")
import FMCommon
import Statistic_V2

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
        self.login = '830005'
        self.brokerID = 5

        table = 'mg_result_hour'
        #查询星期几的数据
        self.hour = 17
        mongoFind = {"login": self.login,"brokerid": self.brokerID,"close_hour": self.hour}

        ##获取mongo DB数据库中的相关指标值
        mongoUrl = "mongodb://%s:%s@%s" % (statisticConf.mongo_userName, statisticConf.mongo_passwd, statisticConf.mongo_host)
        self.mongoList = Statistic_V2.mongoData(host = mongoUrl, port = statisticConf.mongo_port,db=statisticConf.mongo_DB,table=table,find = mongoFind)
        #获取mongoDB中数据最后统计时间
        self.updatets = time.strftime("%Y-%m-%d %H:%M:%S.0", time.localtime(self.mongoList.updatets / 1000))

    def setUp(self):
        pass

    def test_1_pointop_close_profit(self):
        '''openTIme: 平仓盈利总点数'''
        pointop_close_profit = Statistic_V2.getPrestoData(login=self.login,brokerID=self.brokerID,hour=self.hour,quotaValue='pointop_close_profit',updatets=self.updatets)
        self.assertAlmostEqual(pointop_close_profit ,self.mongoList.pointop_close_profit,delta=0.01)

    def test_2_pointop_close_loss(self):
        '''openTIme: 平仓亏损总点数'''
        pointop_close_loss = Statistic_V2.getPrestoData(login=self.login,brokerID=self.brokerID,hour=self.hour,quotaValue='pointop_close_loss',updatets=self.updatets)
        self.assertAlmostEqual(pointop_close_loss ,self.mongoList.pointop_close_loss,delta=0.01)

    def test_3_moneyop_close_profit(self):
        '''openTIme: 平仓盈利总收益'''
        moneyop_close_profit = Statistic_V2.getPrestoData(login=self.login,brokerID=self.brokerID,hour=self.hour,quotaValue='moneyop_close_profit',updatets=self.updatets)
        self.assertAlmostEqual(moneyop_close_profit ,self.mongoList.moneyop_close_profit,delta=0.01)
   
    def test_4_moneyop_close_loss(self):
        '''openTIme: 平仓亏损总收益'''
        moneyop_close_loss = Statistic_V2.getPrestoData(login=self.login,brokerID=self.brokerID,hour=self.hour,quotaValue='moneyop_close_loss',updatets=self.updatets)
        self.assertAlmostEqual(moneyop_close_loss ,self.mongoList.moneyop_close_loss,delta=0.01)

    def test_5_standardlotsop_close(self):
        '''openTIme: 平仓总标准手'''
        standardlotsop_close = Statistic_V2.getPrestoData(login=self.login,brokerID=self.brokerID,hour=self.hour,quotaValue='standardlotsop_close',updatets=self.updatets)
        self.assertAlmostEqual(standardlotsop_close ,self.mongoList.standardlotsop_close,delta=0.01)

    def test_6_standardlotsop_close_profit(self):
        '''openTIme: 平仓盈利总标准手'''
        standardlotsop_close_profit = Statistic_V2.getPrestoData(login=self.login,brokerID=self.brokerID,hour=self.hour,quotaValue='standardlotsop_close_profit',updatets=self.updatets)
        self.assertAlmostEqual(standardlotsop_close_profit ,self.mongoList.standardlotsop_close_profit,delta=0.01)

    def test_7_standardlotsop_close_loss(self):
        '''openTIme: 平仓亏损总标准手'''
        standardlotsop_close_loss = Statistic_V2.getPrestoData(login=self.login,brokerID=self.brokerID,hour=self.hour,quotaValue='standardlotsop_close_loss',updatets=self.updatets)
        self.assertAlmostEqual(standardlotsop_close_loss ,self.mongoList.standardlotsop_close_loss,delta=0.01)

    def test_8_standardlotsop_close_short(self):
        '''openTIme: 平仓做空总标准手'''
        standardlotsop_close_short = Statistic_V2.getPrestoData(login=self.login,brokerID=self.brokerID,hour=self.hour,quotaValue='standardlotsop_close_short',updatets=self.updatets)
        self.assertAlmostEqual(standardlotsop_close_short ,self.mongoList.standardlotsop_close_short,delta=0.01)

    def test_9_standardlotsop_close_long(self):
        '''openTIme: 平仓做多总标准手'''
        standardlotsop_close_long = Statistic_V2.getPrestoData(login=self.login,brokerID=self.brokerID,hour=self.hour,quotaValue='standardlotsop_close_long',updatets=self.updatets)
        self.assertAlmostEqual(standardlotsop_close_long ,self.mongoList.standardlotsop_close_long,delta=0.01)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

