#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_TradeScore_001_001
# 用例标题: 交易员评分
# 预置条件: 
# 测试步骤:
#   1.传入mt4帐号、brokerid
#   2.分别计算每个指标的得分值
#   3.统计总得分
# 预期结果:
#   1.得分与tradescore表的得分一致
# 脚本作者: shencanhui
# 写作日期: 20171102
#=========================================================
import sys,unittest,json,grpc,time
sys.path.append("../../lib/proto")
sys.path.append("../../lib/common")
sys.path.append("../../lib/tradeScore")
sys.path.append("../../lib/WebAPI")
import FMCommon
import numpy as np
from copytrade import copytrade_pb2
from backtesting import backtesting_pb2_grpc
from backtesting import backtesting_pb2

tradeScoreData = FMCommon.loadTradeScoreYML()
webAPIData = FMCommon.loadWebAPIYML()
commonConf = FMCommon.loadPublicYML()


class tradeScore(unittest.TestCase):
    @classmethod
    def setUpClass(self):

        #申明需要测试的经纪商。当前为：kvb
        self.brokerID = 6
        #获取指定经纪商的mt4账号。当前为：kvb
        self.login = '32900'
        startTime = '2018-03-26 00:00:00'
        endTime = '2018-06-20 00:00:00'

        #时间转为时间戳
        self.startTimeStamp = int(time.mktime(time.strptime(startTime, "%Y-%m-%d %H:%M:%S")))
        self.endTimeStamp = int(time.mktime(time.strptime(endTime, "%Y-%m-%d %H:%M:%S")))

        ##alibeta 环境连接信息 ++++++++++++++++++++++++++++++++
        #连接account测试服务器
        consulBackTestingHost = FMCommon.consul_operater(host=commonConf['consulHost'],port=commonConf['consulPort'],server='followme.srv.backtesting',key='ServiceAddress')
        consulBackTestingPort = FMCommon.consul_operater(host=commonConf['consulHost'],port=commonConf['consulPort'],server='followme.srv.backtesting',key='ServicePort')
        backTestingChannel = grpc.insecure_channel(consulBackTestingHost + ':' + str(consulBackTestingPort))
        self.backTestingStub = backtesting_pb2_grpc.BacktestingSrvStub(backTestingChannel)

    def test_01_FactorProfitEquity(self):
        '''回测净值'''
        print("")
        btUser = self.backTestingStub.BacktestingUser(backtesting_pb2.BacktestingUserRequest(BrokerID = self.brokerID, Account = self.login,
            From = self.startTimeStamp, To = self.endTimeStamp, TimeRange=12))
        # print(btUser)

        # for i in btUser:
        #     print(i)
        for i in btUser.EquityList:
            time_local = time.localtime(i.Time)
            dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            print("EquityList:", dt, " Value:", i.Value)

        for i in btUser.BalanceList:
            time_local = time.localtime(i.Time)
            dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            # print("BalanceList:", dt, " Value:", i.Value)

        for i in btUser.DepositList:
            time_local = time.localtime(i.Time)
            dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            print("DepositList:", dt, " Value:", i.Value)

        for i in btUser.DepositChangeList:
            time_local = time.localtime(i.Time)
            dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            print("DepositChangeList:", dt, " Before:", i.Before, " After:", i.After)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #将测试订单平掉。平仓
        pass


if __name__ == '__main__':
    unittest.main()