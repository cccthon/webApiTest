#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: 
# 用例标题: MT4 开仓
# 预置条件:
# 测试步骤:
# 预期结果:
# 脚本作者: chenyy
# 写作日期: 20180717
# -*- coding:utf-8 -*
import sys,unittest,json,grpc,time,threading
sys.path.append("../../lib/proto")
sys.path.append("../../lib/common")
sys.path.append("../../lib/WebAPI")
sys.path.append("../../lib/tradeSAM")
import FMCommon
from mt4dealer import mt4dealer_pb2
from mt4dealer import mt4dealer_pb2_grpc

webAPIData = FMCommon.loadWebAPIYML()
commonConf = FMCommon.loadPublicYML()

class SamPosition(unittest.TestCase):
    @classmethod
    def setUp(self):
        '''连接KVB 的Dealer服务'''
        host = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],
                                                         server='followme.srv.copytrade.dealer.kvb', key='ServiceAddress')
        port = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],
                                                         server='followme.srv.copytrade.dealer.kvb', key='ServicePort')
        channel = grpc.insecure_channel(host + ':' + str(port))
        print(channel,host + ':' + str(port))

        self.stub = mt4dealer_pb2_grpc.MT4DealerSrvStub(channel)
        self.account = 830001
        self.brokerID = 5
        self.symbol = 'GBPJPY'
        self.cmd = 1
        self.lots = 0.01
        self.volume = 1

    def test_Mt4OpenPosition(self):
        '开仓'
        openRes=self.stub.OpenPosition(mt4dealer_pb2.Order(Login=self.account,Cmd=self.cmd,Symbol=self.symbol,Volume=self.volume))
        # print('openPostion: ',openRes)
        self.tradeId=openRes.OrderID
        # print('tradeid: ',self.tradeId)
        self.assertEqual(self.volume,openRes.Volume)
        self.assertEqual(self.symbol, openRes.Symbol)


    def tearDown(self):
        '退出登录'
        closeRes=self.stub.ClosePosition(mt4dealer_pb2.Order(Login=self.account,Volume=self.volume,OrderID=self.tradeId))
        self.assertEqual(self.tradeId,closeRes.OrderID)

if __name__ == '__main__':
    unittest.main()