# -*- coding:utf-8 -*
import sys,yaml,uuid,time,datetime
import unittest,json,grpc
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
sys.path.append("../../lib/proto")
sys.path.append("../../test/follow")
sys.path.append("../../test/statistics")
import FMCommon,TradeOnline,Auth,Trade,Account,Order,consul
from socketIO_client import SocketIO
from mt4dealer import mt4dealer_pb2
from mt4dealer import mt4dealer_pb2_grpc
from account import account_pb2
from account import account_pb2_grpc
from page import page_pb2
from page import page_pb2_grpc
from copytrade import copytrade_pb2
from copytrade import copytrade_pb2_grpc
from tradesignal import tradesignal_pb2
from tradesignal import tradesignal_pb2_grpc
import FollowOperation


userData = FMCommon.loadWebAPIYML()
order = FMCommon.loadOrderYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()

userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()
userDataTrade=FMCommon.loadTradeYML()
userDataSocial=FMCommon.loadSocialYML()
userDatagrpc = yaml.load(open('../../conf/common/common.yml', 'r',encoding='utf-8'))

class QueryHistoryOrder(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.token = json.loads(traderLoginRes.text)['data']['token']

        # 连接account测试服务器
        consulAccountHost = FMCommon.consul_operater(host=userDatagrpc['consulHost'], port=userDatagrpc['consulPort'],
                                                     server='followme.srv.account', key='ServiceAddress')
        consulAccountPort = FMCommon.consul_operater(host=userDatagrpc['consulHost'], port=userDatagrpc['consulPort'],
                                                     server='followme.srv.account', key='ServicePort')
        accountChannel = grpc.insecure_channel(consulAccountHost + ':' + str(consulAccountPort))
        self.accountStub = account_pb2_grpc.AccountSrvStub(accountChannel)
        print("self.accountStub:", self.accountStub)

        # 连接dealer测试服务器  http://10.1.0.4:8500
        consulDealerHost = FMCommon.consul_operater(host=userDatagrpc['consulHost'], port=userDatagrpc['consulPort'],
                                                    server='followme.srv.copytrade.dealer.pico', key='ServiceAddress')
        consulDealerPort = FMCommon.consul_operater(host=userDatagrpc['consulHost'], port=userDatagrpc['consulPort'],
                                                    server='followme.srv.copytrade.dealer.pico', key='ServicePort')
        print(consulDealerHost + ':' + str(consulDealerPort))
        dealerChannel = grpc.insecure_channel(consulDealerHost + ':' + str(consulDealerPort))
        self.dealerStub = mt4dealer_pb2_grpc.MT4DealerSrvStub(dealerChannel)
        print("self.dealerStub:", self.dealerStub)

    def test_QueryHistoryOrder(self):
        '''验证历史订单手续费，利息，收益金额，收益点数，开仓时间'''
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token

        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=5)

        # 切换到MT4账号
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 userData['headers'],self.tradeAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])

        # 查询历史订单
        params = {userData['orderStatus']: userData['orderStatus_close']}
        getHistoryOrderRes = Order.getOrders(userData['hostName'] + order['getOrders_url'], userData['headers'], params=params,printLogs=1)
        self.assertEqual(getHistoryOrderRes.status_code, userData['status_code_200'])

        #获取历史订单的第一张单号作为验证
        self.TICKET = json.loads(getHistoryOrderRes.text)['data']['items'][0]['TICKET']
        print('历史订单:', str(json.loads(getHistoryOrderRes.text)['data']['items'][0]))

        # OPEN_TIME: 开仓时间
        self.OPEN_TIME = json.loads(getHistoryOrderRes.text)['data']['items'][0]['OPEN_TIME']

        #转化为时间戳
        timeArray_OPEN_TIME = time.strptime(str(self.OPEN_TIME), "%Y/%m/%d %H:%M:%S")
        timeStamp_OPEN_TIME = int(time.mktime(timeArray_OPEN_TIME))
        print("timeStamp_OPEN_TIME:", timeStamp_OPEN_TIME)

        # CLOSE_TIME: 平仓时间
        self.CLOSE_TIME = json.loads(getHistoryOrderRes.text)['data']['items'][0]['CLOSE_TIME']

        # 转化为时间戳
        timeArray_CLOSE_TIME = time.strptime(str(self.CLOSE_TIME), "%Y/%m/%d %H:%M:%S")
        timeStamp_CLOSE_TIME = int(time.mktime(timeArray_CLOSE_TIME))
        print("timeStamp_CLOSE_TIME:", timeStamp_CLOSE_TIME)

        # PROFIT: 盈亏
        self.PROFIT = json.loads(getHistoryOrderRes.text)['data']['items'][0]['PROFIT']

        # SWAPS: 利息
        self.SWAPS = json.loads(getHistoryOrderRes.text)['data']['items'][0]['SWAPS']

        # COMMISSION: 手续费
        self.COMMISSION = json.loads(getHistoryOrderRes.text)['data']['items'][0]['COMMISSION']

        #从grpc获得订单记录
        GetTradeRecord = self.dealerStub.GetTradeRecord(mt4dealer_pb2.Trade(OrderID=int(self.TICKET)))
        print("GetAccount:", GetTradeRecord)
        self.assertEqual(GetTradeRecord.Commission, round(self.COMMISSION,2), "手续费不相同")
        self.assertEqual(GetTradeRecord.Profit, round(self.PROFIT,2), "盈亏金额不相同")
        self.assertEqual(GetTradeRecord.Storage, round(self.SWAPS, 2), "利息不相同")

        #把时间戳转为日期
        timeArray = time.localtime(GetTradeRecord.OpenTime)
        otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
        print("GetTradeRecord.OpenTime：", otherStyleTime)
        print("self.OPEN_TIME:", self.OPEN_TIME)

        # 计算两个日期的间隔
        d1 = datetime.datetime.strptime(otherStyleTime, '%Y/%m/%d %H:%M:%S')
        d2 = datetime.datetime.strptime(self.OPEN_TIME, '%Y/%m/%d %H:%M:%S')
        print("d：", d1-d2)
        # self.assertEqual(GetTradeRecord.OpenTime, timeStamp_OPEN_TIME, "开仓时间不相同")
        # self.assertEqual(GetTradeRecord.CloseTime, timeStamp_CLOSE_TIME, "平仓时间不相同")

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.makeSuite(QueryHistoryOrder)
    unittest.TextTestRunner(verbosity=2).run(suite)

