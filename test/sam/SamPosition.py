#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID:
# 用例标题: Sam
# 预置条件:
# 测试步骤:
# 预期结果:
# 脚本作者: wangmingli
# 写作日期: 20180705
# -*- coding:utf-8 -*
import sys,unittest,json,grpc,time,threading
sys.path.append("../../lib/proto")
sys.path.append("../../lib/common")
sys.path.append("../../lib/WebAPI")
sys.path.append("../../lib/tradeSAM")
import FMCommon,TradeSAM
from mt4api import mt4api_pb2
from mt4api import mt4api_pb2_grpc
from tradesignal import tradesignal_pb2
from tradesignal import tradesignal_pb2_grpc

webAPIData = FMCommon.loadWebAPIYML()
commonConf = FMCommon.loadPublicYML()

class SamPosition(unittest.TestCase):
    def setUp(self):
        '''测试Sam经纪商开仓,平仓,历史订单'''
        host = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],
                                                         server='followme.srv.mt4api.2', key='ServiceAddress')
        port = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],
                                                         server='followme.srv.mt4api.2', key='ServicePort')
        channel = grpc.insecure_channel(host + ':' + str(port))
        print(channel)

        channel = grpc.insecure_channel(host + ':' + str(port))
        self.stub = mt4api_pb2_grpc.MT4APISrvStub(channel)

    def test_SamPosition(self):
        account = '3017068'  #dev
       # account = '500383407'
        brokerID = 120
        symbol = 'AUDCAD'
        cmd = 0
        lots = 0.1
        # 循环开仓
        TradeIDList=[]
        for i in range(0, 3):
            openRes = TradeSAM.TradeSAMStream.OpenPosition(stub=self.stub, account=account, brokerID=brokerID, symbol=symbol, cmd=cmd, lots=lots)
            print(openRes)
            self.assertEqual(openRes.Signal.Symbol, symbol)
            tradeID = openRes.Signal.TradeID
            TradeIDList.append(tradeID)

        # 循环平仓
        for i in TradeIDList:
            closeRes = TradeSAM.TradeSAMStream.ClosePosition(stub=self.stub, account=account, brokerID=brokerID, tradeID=i, lots=lots)
            print(closeRes)
            self.assertEqual(closeRes.Signal.TradeID, i)
            self.assertEqual(closeRes.Signal.Symbol, symbol)

        print(TradeIDList)

    def tearDown(self):
        # 退出登录
        pass

if __name__ == '__main__':
    unittest.main()