#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_SamOpenPosition
# 用例标题: Sam
# 预置条件:
# 测试步骤:
#   1.Sam经纪商开仓
#   2.平仓
#   3.检查历史订单
# 预期结果:
#   1.开仓平仓成功及数据正确
# 脚本作者: wangmingli
# 写作日期: 20180621
#=========================================================
import sys,unittest,json,requests,time,yaml,uuid,grpc
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
import Auth,FMCommon,Account
from socketIO_client import SocketIO
from base64 import b64encode
sys.path.append("../../lib/proto")
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


webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
userData = yaml.load(open('../../conf/common/common.yml', 'r',encoding='utf-8'))
accountList = yaml.load(open('account.yml', 'r',encoding='utf-8'))

class Signin(unittest.TestCase):
    def setUp(self):
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
    
    # def test_signin(self):
    #     url = 'http://10.1.0.19:8000/app/'
    #     add = 'add'
    #     update = 'update'
    #     start = 'start'
    #     headers = {"content-type": "application/json"}

    #     #users info
    #     broker_id = 106
    #     serverName = "GKFX-Demo-1"

    #     #
    #     #账号后缀
    #     self.accountPostfix = '@qq.com'
    #     #注册的账号，唯。由于需要批量注册，做自增，所以请传入整形。int
    #     self.account = 99991104
    #     #注册密码
    #     self.userPassword = '123456'

    #     for i in accountList["accountList"]:
    #         print(i)


    #         #注册的nickname，唯一
    #         self.nickName = str(self.account) + '_nickName'
    #         register = self.accountStub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = str(self.account)+self.accountPostfix ,UserPassword = self.userPassword)))
    #         print(register)
    #         # #断言帐号状态为5，未激活
    #         # #AccountStatus: 0 新申请, 1 审核中, 2 正常, 3 锁定（此时交易员才可提取服务费）, 4 注销, 5 未激活,6 注销
    #         # self.assertEqual(register.AccountStatus, 5)
    #         # self.assertEqual(register.AccountEmail, str(self.account)+self.accountPostfix)
    #         self.userID = register.Id
            
    #         # 新注册的账号需要先激活才能登录
    #         # 发送验证码邮件到邮箱
    #         sendActivationEmail = self.accountStub.SendActivationEmail(account_pb2.SendActivationEmailRequest(UserId = self.userID,
    #             ActivationCode = 'thisisactivationcode',Email = 'shencanhui@followme-inc.com' ,Subject = '注册followme验证码' ))
    #         #断言验证码邮件发送成功，返回0
    #         self.assertEqual(sendActivationEmail.Success, 0)
    #         #获取验证码
    #         getActivationByObj = self.accountStub.GetActivationByObj(account_pb2.ActivationRequest(ObjectId = self.userID))
    #         vercode = getActivationByObj.VerCode
    #         activationCode = getActivationByObj.ActivationCode
    #         #激活账号。
    #         #AccountStatus: 0 新申请, 1 审核中, 2 正常, 3 锁定（此时交易员才可提取服务费）, 4 注销, 5 未激活,6 注销
    #         validateEmailLink = self.accountStub.ValidateEmailLink(account_pb2.ValidateEmailLinkRequest(UserId = self.userID, VerCode = vercode,
    #             ActivationCode = activationCode,Token = str(uuid.uuid1())))
    #         self.assertEqual(validateEmailLink.Success, 0)

    #         #设置用户昵称
    #         setNickName = self.accountStub.SetNickName(account_pb2.User(Id = self.userID,NickName = self.nickName))
    #         #检查设置成功后，返回值为：0
    #         self.assertEqual(setNickName.Success, 0)

    #         #绑定pico帐号
    #         bindPico = self.dealerStub.CreateAccount(mt4dealer_pb2.Account(Name = 'DEMO_ACCOUNT_' + str(self.userID),
    #             Password = 'abc123', BrokerID = 1, Group = 'ct_pico', City = 'sz'))
    #         print(bindPico)
    #         self.login = bindPico.Login
    #         self.assertEqual(bindPico.Name, "DEMO_ACCOUNT_" + str(self.userID))
    #         #断言绑定的经济商为：1. 晋峰
    #         self.assertEqual(bindPico.BrokerID, 1)

    #         #将注册的用户提取到t_useraccount表
    #         #accounttype:Demo = 0,Real = 1,Sam  = 2,Mam  = 3
    #         saveUserAccount = self.accountStub.SaveUserAccount(account_pb2.SaveUserAccountRequest(User = account_pb2.User(Id = self.userID),
    #             BrokerID = 1, MT4Account = str(self.login), IsTrader = 0, AccountCreateType = 0, IsBind = 2,AccountType = 1))
    #         self.assertEqual(saveUserAccount.Success, 0)

    #         #pico入金
    #         self.dealerStub.DepositWithdraw(mt4dealer_pb2.DepositWithdrawMessage(Login = self.login,
    #             Price = 9999999, Comment = 'Deposit With script.'))

    #         self.account += 1
    #         time.sleep(5)


    #         # #bind app
    #         print(url + add)
    #         # bind_from 0 trader,follower 5
    #         createDates = {"server_name": serverName,"broker_id": broker_id,"login": i["account"],"fm_user_id": self.userID,"password": i["mainPWd"],"bind_from": 0}
    #         createRes = requests.post(url + add, headers = headers, data = json.dumps(createDates))
    #         print(createRes.status_code,createRes.text)
    #         app_id = json.loads(createRes.text)['data']['app_id']
    #         print(app_id)
        
        
    #         # #start app
    #         time.sleep(1)
    #         print(url + start)
    #         startRes = requests.get(url + start + '/' + str(app_id))
    #         print(startRes.status_code,startRes.text)

    #         print("create succ:",self.account,self.userID,i["account"],app_id)

    def test_bind_single(self):
        url = 'http://10.1.0.19:8000/app/'
        add = 'add'
        update = 'update'
        start = 'start'
        headers = {"content-type": "application/json"}

        #users info
        broker_id = 106
        serverName = "GKFX-Demo-1"
        
        # #bind app
        print(url + add)
        # bind_from 0 trader,follower 5
        createDates = {"server_name": serverName,"broker_id": broker_id,"login": "500387171","fm_user_id": "169204","password": "oan6fpz","bind_from": 5}
        createRes = requests.post(url + add, headers = headers, data = json.dumps(createDates))
        print(createRes.status_code,createRes.text)
        app_id = json.loads(createRes.text)['data']['app_id']
        print(app_id)
    
    
        # #start app
        time.sleep(1)
        print(url + start)
        startRes = requests.get(url + start + '/' + str(app_id))
        print(startRes.status_code,startRes.text)

        # print("create succ:",self.account,self.userID,i["account"],app_id)



    def tearDown(self):
        #清空测试环境，还原测试数据
        pass

if __name__ == '__main__':
    unittest.main()
