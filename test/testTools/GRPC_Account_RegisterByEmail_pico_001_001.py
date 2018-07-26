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

        # ###dev 环境连接信息 ++++++++++++++++++++++++++++++++
        # #连接account测试服务器
        # consulAccountHost = FMCommon.consul_operater(host='192.168.8.6',port=userData['consulPort'],server='followme.srv.account',key='ServiceAddress')
        # consulAccountPort = FMCommon.consul_operater(host='192.168.8.6',port=userData['consulPort'],server='followme.srv.account',key='ServicePort')
        # accountChannel = grpc.insecure_channel(consulAccountHost + ':' + str(consulAccountPort))
        # self.accountStub = account_pb2_grpc.AccountSrvStub(accountChannel)
        # #连接dealer测试服务器  http://10.1.0.4:8500
        # consulDealerHost = FMCommon.consul_operater(host='192.168.8.6',port=userData['consulPort'],server='followme.srv.copytrade.dealer.pico',key='ServiceAddress')
        # consulDealerPort = FMCommon.consul_operater(host='192.168.8.6',port=userData['consulPort'],server='followme.srv.copytrade.dealer.pico',key='ServicePort')
        # # print(consulDealerHost + ':' + str(consulDealerPort))
        # dealerChannel = grpc.insecure_channel(consulDealerHost + ':' + str(consulDealerPort))
        # self.dealerStub = mt4dealer_pb2_grpc.MT4DealerSrvStub(dealerChannel)

    def test_RegisterByEmail(self):
        self.accountEmail = '181160733655@qq.com'
        self.userPassword = '123456'
        self.nickName = 'fsa005555'
        print(self.nickName)
        # 注册一个测试账号
        register = self.accountStub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = self.accountEmail ,UserPassword = self.userPassword)))
        # print(register)
        # #断言帐号状态为5，未激活
        # #AccountStatus: 0 新申请, 1 审核中, 2 正常, 3 锁定（此时交易员才可提取服务费）, 4 注销, 5 未激活,6 注销
        self.assertEqual(register.AccountStatus, 5)
        self.assertEqual(register.AccountEmail, self.accountEmail)
        self.userID = register.Id

        #新注册的账号需要先激活才能登录
        #发送验证码邮件到邮箱
        sendActivationEmail = self.accountStub.SendActivationEmail(account_pb2.SendActivationEmailRequest(UserId = self.userID,
            ActivationCode = 'thisisactivationcode',Email = 'shencanhui@followme-inc.com' ,Subject = '注册followme验证码' ))
        #断言验证码邮件发送成功，返回0
        self.assertEqual(sendActivationEmail.Success, 0)
        #获取验证码
        getActivationByObj = self.accountStub.GetActivationByObj(account_pb2.ActivationRequest(ObjectId = self.userID))
        vercode = getActivationByObj.VerCode
        activationCode = getActivationByObj.ActivationCode
        #激活账号。
        #AccountStatus: 0 新申请, 1 审核中, 2 正常, 3 锁定（此时交易员才可提取服务费）, 4 注销, 5 未激活,6 注销
        validateEmailLink = self.accountStub.ValidateEmailLink(account_pb2.ValidateEmailLinkRequest(UserId = self.userID, VerCode = vercode,
            ActivationCode = activationCode,Token = str(uuid.uuid1())))
        self.assertEqual(validateEmailLink.Success, 0)

        #设置用户昵称
        setNickName = self.accountStub.SetNickName(account_pb2.User(Id = self.userID,NickName = self.nickName))
        #检查设置成功后，返回值为：0
        self.assertEqual(setNickName.Success, 0)

        #绑定pico帐号
        bindPico = self.dealerStub.CreateAccount(mt4dealer_pb2.Account(Name = 'DEMO_ACCOUNT_' + str(self.userID),
            Password = 'abc123', BrokerID = 1, Group = 'ct_pico', City = 'sz'))
        print(bindPico)
        self.login = bindPico.Login
        self.assertEqual(bindPico.Name, "DEMO_ACCOUNT_" + str(self.userID))
        #断言绑定的经济商为：1. 晋峰
        self.assertEqual(bindPico.BrokerID, 1)

        #将注册的用户提取到t_useraccount表
        #accounttype:Demo = 0,Real = 1,Sam  = 2,Mam  = 3
        saveUserAccount = self.accountStub.SaveUserAccount(account_pb2.SaveUserAccountRequest(User = account_pb2.User(Id = self.userID),
            BrokerID = 1, MT4Account = str(self.login), IsTrader = 0, AccountCreateType = 0, IsBind = 2,AccountType = 1))
        self.assertEqual(saveUserAccount.Success, 0)

        #pico入金
        self.dealerStub.DepositWithdraw(mt4dealer_pb2.DepositWithdrawMessage(Login = self.login,
            Price = 9999999, Comment = 'Deposit With script.'))

        #登录
        self.signinToken = str(uuid.uuid1())
        signin = self.accountStub.Login(account_pb2.LoginRequest(User = account_pb2.User(AccountEmail = self.accountEmail,
            UserPassword = self.userPassword) ,Token = self.signinToken))
        self.assertEqual(signin.Id, self.userID)
        print("signin:>>>>>>>", signin)

    def tearDown(self):
        #本用例由于空密码未注册成功，所以不需要注销账号。故注销账号步骤单独写到注销成功的测试方法里
        #清空测试环境
        #退出登录
        pass
        # signout = self.accountStub.Logout(account_pb2.TokenAndVcode(Token = self.signinToken))
        # self.assertEqual(signout.Success, 0)
        # # 注销测试账号
        # unregister = self.accountStub.DeleteUserById(account_pb2.User(Id = self.userID))
        # # 断言注销账号成功，返回0
        # print(unregister)
        # self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()