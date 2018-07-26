#========================================================
#+++++++++++++++++  测试工具信息   ++++++++++++++++
# 通过rpc接口创建一个followme帐号，并绑定一个demo和pico帐号并入金。
# 可以直接使用的测试帐号。
# 设置入参在40-42行
#=========================================================
import grpc,sys,unittest,yaml,uuid,time
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

class RegisterByEmail(object):
    @staticmethod
    def RegisterByEmail():
        ##alibeta 环境连接信息 ++++++++++++++++++++++++++++++++
        #连接account测试服务器
        consulAccountHost = FMCommon.consul_operater(host=userData['consulHost'],port=userData['consulPort'],server='followme.srv.account',key='ServiceAddress')
        consulAccountPort = FMCommon.consul_operater(host=userData['consulHost'],port=userData['consulPort'],server='followme.srv.account',key='ServicePort')
        accountChannel = grpc.insecure_channel(consulAccountHost + ':' + str(consulAccountPort))
        accountStub = account_pb2_grpc.AccountSrvStub(accountChannel)
        #连接dealer测试服务器  http://10.1.0.4:8500
        consulDealerHost = FMCommon.consul_operater(host=userData['consulHost'],port=userData['consulPort'],server='followme.srv.copytrade.dealer.pico',key='ServiceAddress')
        consulDealerPort = FMCommon.consul_operater(host=userData['consulHost'],port=userData['consulPort'],server='followme.srv.copytrade.dealer.pico',key='ServicePort')
        # print(consulDealerHost + ':' + str(consulDealerPort))
        dealerChannel = grpc.insecure_channel(consulDealerHost + ':' + str(consulDealerPort))
        mt4dealer_pb2_grpc.MT4DealerSrvStub(dealerChannel)


        accountEmail = 'test'+str(int(time.time()))+'@followme-inc.com'
        userPassword = '123456'
        nickName = 'Demo'+str(int(time.time()))
        print(nickName)
        # 注册一个测试账号
        register = accountStub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = accountEmail ,UserPassword = userPassword)))
        # #断言帐号状态为5，未激活
        # #AccountStatus: 0 新申请, 1 审核中, 2 正常, 3 锁定（此时交易员才可提取服务费）, 4 注销, 5 未激活,6 注销
        userID = register.Id

        #新注册的账号需要先激活才能登录
        #发送验证码邮件到邮箱
        accountStub.SendActivationEmail(account_pb2.SendActivationEmailRequest(UserId = userID,
            ActivationCode = 'thisisactivationcode',Email = 'shencanhui@followme-inc.com' ,Subject = '注册followme验证码' ))
        #获取验证码
        getActivationByObj = accountStub.GetActivationByObj(account_pb2.ActivationRequest(ObjectId = userID))
        vercode = getActivationByObj.VerCode
        activationCode = getActivationByObj.ActivationCode
        #激活账号。
        #AccountStatus: 0 新申请, 1 审核中, 2 正常, 3 锁定（此时交易员才可提取服务费）, 4 注销, 5 未激活,6 注销
        accountStub.ValidateEmailLink(account_pb2.ValidateEmailLinkRequest(UserId = userID, VerCode = vercode,
                                                                           ActivationCode = activationCode,
                                                                           Token = str(uuid.uuid1())))

        #设置用户昵称
        accountStub.SetNickName(account_pb2.User(Id = userID,NickName = nickName))
        return accountEmail
