#========================================================
#+++++++++++++++++  测试工具信息   ++++++++++++++++
# 通过rpc接口创建一个followme帐号，并绑定一个demo和pico帐号并入金。
# 可以直接使用的测试帐号。
# 设置入参在40-42行
#=========================================================
import grpc,sys,unittest,yaml,uuid
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

class RegisterByEmail(unittest.TestCase):
    def setUp(self):
        ##alibeta 环境连接信息 ++++++++++++++++++++++++++++++++
        #连接account测试服务器
        consulAccountHost = FMCommon.consul_operater(host=userData['consulHost'],port=userData['consulPort'],server='followme.srv.account',key='ServiceAddress')
        consulAccountPort = FMCommon.consul_operater(host=userData['consulHost'],port=userData['consulPort'],server='followme.srv.account',key='ServicePort')
        accountChannel = grpc.insecure_channel(consulAccountHost + ':' + str(consulAccountPort))
        self.accountStub = account_pb2_grpc.AccountSrvStub(accountChannel)
        #连接dealer测试服务器  http://10.1.0.4:8500
        consulDealerHost = FMCommon.consul_operater(host=userData['consulHost'],port=userData['consulPort'],server='followme.srv.copytrade.dealer.pico',key='ServiceAddress')
        consulDealerPort = FMCommon.consul_operater(host=userData['consulHost'],port=userData['consulPort'],server='followme.srv.copytrade.dealer.pico',key='ServicePort')
        # print(consulDealerHost + ':' + str(consulDealerPort))
        dealerChannel = grpc.insecure_channel(consulDealerHost + ':' + str(consulDealerPort))
        self.dealerStub = mt4dealer_pb2_grpc.MT4DealerSrvStub(dealerChannel)
