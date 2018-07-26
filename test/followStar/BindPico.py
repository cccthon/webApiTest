#========================================================
#+++++++++++++++++  测试工具信息   ++++++++++++++++
#可以绑定man或pico到某个帐号上
#入参："UserID": 169202,   followme的userid
#		"isTrader": 1,		交易员还是跟随者。交易员：1，跟随者：0
#		"accountType": 3	pico:1 , mam: 3
#		"price": 5000		入金金额
#=========================================================
import grpc,sys,unittest,yaml,uuid,json
sys.path.append("../../lib/proto")
sys.path.append("../../lib/common")
import FMCommon,consul
from account import account_pb2
from account import account_pb2_grpc
from page import page_pb2
from page import page_pb2_grpc
from copytrade import copytrade_pb2
from copytrade import copytrade_pb2_grpc
from tradesignal import tradesignal_pb2
from tradesignal import tradesignal_pb2_grpc
from mt4dealer import mt4dealer_pb2
from mt4dealer import mt4dealer_pb2_grpc

userData = yaml.load(open('../../conf/common/common.yml', 'r',encoding='utf-8'))

class BindPico(object):
    @staticmethod
    def bindPico(UserID,group,IsTrader,accountType):
        # 连接account测试服务器
        consulAccountHost = FMCommon.consul_operater(host=userData['consulHost'], port=userData['consulPort'],
                                                     server='followme.srv.account', key='ServiceAddress')
        consulAccountPort = FMCommon.consul_operater(host=userData['consulHost'], port=userData['consulPort'],
                                                     server='followme.srv.account', key='ServicePort')
        accountChannel = grpc.insecure_channel(consulAccountHost + ':' + str(consulAccountPort))
        accountStub = account_pb2_grpc.AccountSrvStub(accountChannel)

        # 连接dealer测试服务器  http://10.1.0.4:8500
        consulDealerHost = FMCommon.consul_operater(host=userData['consulHost'], port=userData['consulPort'],
                                                    server='followme.srv.copytrade.dealer.pico', key='ServiceAddress')
        consulDealerPort = FMCommon.consul_operater(host=userData['consulHost'], port=userData['consulPort'],
                                                    server='followme.srv.copytrade.dealer.pico', key='ServicePort')
        dealerChannel = grpc.insecure_channel(consulDealerHost + ':' + str(consulDealerPort))
        dealerStub = mt4dealer_pb2_grpc.MT4DealerSrvStub(dealerChannel)

        bindPico = dealerStub.CreateAccount(mt4dealer_pb2.Account(Name='MAM_ACCOUNT_' + str(UserID),
                                                                       Password='abc123', BrokerID=1, Group=group,
                                                                       City='sz'))
        login = bindPico.Login

        # 将注册的用户提取到t_useraccount表
        accountStub.SaveUserAccount(account_pb2.SaveUserAccountRequest(User=account_pb2.User(Id=UserID),
                                                   BrokerID=1, MT4Account=str(login),IsTrader=IsTrader,
                                                   AccountCreateType=0, IsBind=2, AccountType=accountType))

        # pico入金
        dealerStub.DepositWithdraw(mt4dealer_pb2.DepositWithdrawMessage(Login=login,Price=10000000,
                                                                        Comment='Deposit With script.'))
        return bindPico
