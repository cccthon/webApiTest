# -*- coding:utf-8 -*
import sys,yaml,uuid,time
import unittest,json,grpc
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
sys.path.append("../../lib/proto")
sys.path.append("../../test/follow")
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
class Accountfunds(unittest.TestCase):
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
        print("self.dealerStub:",self.dealerStub)

    def test_Accountfunds(self):
        '''验证没有持仓单时，账户资金信息：总收益，余额，净值，持仓总手数，浮动收益，可以用保证金，已用保证金'''
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})

        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=5)

        # 切换到MT4账号
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 userData['headers'],self.tradeAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])

        # 获取交易token
        getTokenRes = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], userData['headers'])
        FMCommon.printLog('getTokenRes: ' + getTokenRes.text)
        self.assertEqual(getTokenRes.status_code, userData['status_code_200'])
        tradeToken = str(json.loads(getTokenRes.content)["data"]["Token"]).replace("=", "@")
        MT4Account = json.loads(getTokenRes.content)["data"]["MT4Account"]

        # 获取当前用户的交易订单
        params = {userData['orderStatus']: userData['orderStatus_open']}
        getOrders = Order.getOrders(userData['hostName'] + order['getOrders_url'], userData['headers'], params=params)
        self.assertEqual(getOrders.status_code, userData['status_code_200'])
        ordersIDList = Order.getOrdersID(getOrders)

        # 平掉当前用户所有订单
        closeParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_219'],
                      userDataWebSocket['orderParam_tickets']: ordersIDList}
        closePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
                            userDataWebSocket['ws_port'],{'token': tradeToken}, closeParam)
        self.assertEqual(closePositionRes["code"], userDataWebSocket['ws_code_0'])
        self.assertEqual(closePositionRes["rcmd"], userDataWebSocket['ws_code_219'])
        self.assertEqual(closePositionRes['success_tickets'], ordersIDList)

        time.sleep(3)

        # 获取当前用户的交易订单
        params = {userData['orderStatus']: userData['orderStatus_open']}
        getOrders = Order.getOrders(userData['hostName'] + order['getOrders_url'], userData['headers'], params=params)
        self.assertEqual(getOrders.status_code, userData['status_code_200'])
        self.assertEqual(json.loads(getOrders.text)['data']['total'], 0, "持仓总手数不对")

        #获取当前用户的账户资产getProperty
        params={"accountIndex": str(self.tradeAccountIndex[0])}
        getPropertyRES= Trade.getProperty(userData['hostName'] + userDataTrade["getProperty_url"], userData['headers'], params=params)
        FMCommon.printLog('getPropertyRES:' ,getPropertyRES.text)
        self.assertEqual(getPropertyRES.status_code, userData['status_code_200'])
        #总收益
        TotalProfit = json.loads(getPropertyRES.text)['data']['TotalProfit']
        #余额
        Balance = round(json.loads(getPropertyRES.text)['data']['Balance'],2)
        print("Balance:", Balance)
        #净值
        NetValue = round(json.loads(getPropertyRES.text)['data']['NetValue'],2)
        print("NetValue:", NetValue)
        #浮动收益
        FloatProfit = round(json.loads(getPropertyRES.text)['data']['FloatProfit'],2)
        #入金
        InMoney = round(json.loads(getPropertyRES.text)['data']['InMoney'],2)
        #出金
        OutMoney = round(json.loads(getPropertyRES.text)['data']['OutMoney'],2)
        #杠杆
        Leverage = round(json.loads(getPropertyRES.text)['data']['Leverage'],2)
        #已用保证金
        MARGIN = round(json.loads(getPropertyRES.text)['data']['MARGIN'],2)
        #可用保证金
        MARGIN_FREE =  round(json.loads(getPropertyRES.text)['data']['MARGIN_FREE'],2)
        print("MARGIN_FREE:", MARGIN_FREE)
        #信用
        Credit = round(json.loads(getPropertyRES.text)['data']['Credit'],2)

        #获取grpc账户信息rpc GetAccount(Account) returns (Account) {}
        GetAccount = self.dealerStub.GetAccount(mt4dealer_pb2.Account(Login=int(MT4Account),BrokerID=1))
        print("GetAccount:",GetAccount)

        sql ="select BALANCE,CREDIT,EQUITY,MARGIN,MARGIN_FREE,Leverage FROM T_MT4Users WHERE LOGIN='%s'"%(MT4Account)
        row = FollowOperation.Operation.operationV3DB(sql)
        print("row:",row)

        # self.assertEqual(GetAccount.Login, int(MT4Account), "账户不相同")
        # self.assertEqual(GetAccount.Leverage, Leverage, "杠杆不相同")
        # self.assertEqual(GetAccount.Balance, Balance,"余额不相同")
        # self.assertEqual(GetAccount.Equity, NetValue, "净值不相同")
        # self.assertEqual(GetAccount.FreeMargin, NetValue, "可用保证金不相同")
        # self.assertEqual(GetAccount.Credit, row[0][1], "信用额度不相同")
        # self.assertEqual(GetAccount.Margin, 0, "已用保证金不相同")
        # self.assertEqual(GetAccount.Profit, 0, "浮动收益不相同")
        # self.assertEqual(FloatProfit, 0, "浮动收益不相同")

        #result
        tpspParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_222']}
        tpspParamRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken},tpspParam)
        print("tpspParamRes:",tpspParamRes)
        self.assertEqual(tpspParamRes["code"], userDataWebSocket['ws_code_0'])
        login = tpspParamRes['account']["login"]
        balance=tpspParamRes['account']["balance"]
        credit=tpspParamRes['account']["credit"]
        margin = tpspParamRes['account']["margin"]
        free_margin = tpspParamRes['account']["free_margin"]
        margin_level = tpspParamRes['account']["margin_level"]
        equity = tpspParamRes['account']["equity"]

        self.assertEqual(GetAccount.Login, int(MT4Account), "账户不相同")
        self.assertEqual(GetAccount.Login, login, "账户不相同")
        self.assertEqual(GetAccount.Leverage, Leverage, "杠杆不相同")
        self.assertEqual(GetAccount.Balance, balance, "余额不相同")
        self.assertEqual(GetAccount.Equity, equity, "净值不相同")
        self.assertEqual(GetAccount.FreeMargin, free_margin, "可用保证金不相同")
        self.assertEqual(GetAccount.Credit, credit, "信用额度不相同")
        self.assertEqual(GetAccount.Margin, margin, "已用保证金不相同")
        self.assertEqual(GetAccount.Profit, 0, "浮动收益不相同")
        self.assertEqual(FloatProfit, 0, "浮动收益不相同")


    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.makeSuite(Accountfunds)
    unittest.TextTestRunner(verbosity=2).run(suite)

