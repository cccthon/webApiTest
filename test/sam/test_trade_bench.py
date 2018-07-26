                        #+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: 
# 用例标题: Sam rpc开仓，平仓
# 预置条件:
# 测试步骤:
# 预期结果:
# 脚本作者: shencanhui
# 写作日期: 20180705
# -*- coding:utf-8 -*
import sys,unittest,json,grpc,time,threading,datetime
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
    @classmethod
    def setUpClass(self):
        '''测试Sam经纪商开仓,平仓,历史订单'''
        host = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],
                                                         server='followme.srv.mt4api.3', key='ServiceAddress')
        port = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],
                                                         server='followme.srv.mt4api.3', key='ServicePort')
        channel = grpc.insecure_channel(host + ':' + str(port))
        print(channel,host + ':' + str(port))

        self.stub = mt4api_pb2_grpc.MT4APISrvStub(channel)
        self.account = '500383690'
        self.brokerID = 106
        self.symbol = 'AUDCAD'
        self.cmd = 1
        self.lots = 0.1

        self.accountList = ['500386473','500386474','500386475','500386476','500386477','500386478','500386479','500386480','500386481','500386482',]
    def test_SamPosition(self):
        client = TradeSAM.TradeSAMStream

        def myThread(account):
            '''sam 开仓'''
            print("curr time:",datetime.datetime.now())
            openRes = client.OpenPosition(stub=self.stub,account=account,brokerID=self.brokerID,symbol=self.symbol,cmd=self.cmd,lots=self.lots)
            self.tradeID = openRes.Signal.TradeID
            self.assertEqual(openRes.Signal.Symbol, self.symbol)
            self.assertEqual(openRes.Signal.Lots, self.lots)
            print("---------------------------------")
            # 平仓
            # closeRes = client.ClosePosition(stub=self.stub, account=self.account, brokerID=self.brokerID, tradeID=self.tradeID, lots=self.lots)
            # self.assertEqual(closeRes.Signal.TradeID, self.tradeID)
            # self.assertEqual(closeRes.Signal.Symbol, self.symbol)

        for account in self.accountList:
            for i in range(1000):
                t =threading.Thread(target=myThread,args=(account,))
                t.start()


    def tearDown(self):
        # 退出登录
        pass

if __name__ == '__main__':
    unittest.main()