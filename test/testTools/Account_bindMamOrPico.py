#========================================================
#+++++++++++++++++  测试工具信息   ++++++++++++++++
#可以绑定man或pico到某个帐号上
#入参："UserID": 169202,   followme的userid
#		"isTrader": 1,		交易员还是跟随者。交易员：1，跟随者：0
#		"accountType": 3	pico:1 , mam: 3
#		"price": 5000		入金金额
#=========================================================
import grpc,sys,unittest,yaml,uuid,json,time
sys.path.append("../../lib/proto")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
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
userDataAPI = FMCommon.loadWebAPIYML()
with open("Account_bindMamPico.json",'r',encoding='utf-8') as load_file:
    load_dict = json.load(load_file)

class Account_bindMamOrPico(unittest.TestCase):
    def setUp(self):

        # alibeta 环境连接account测试服务器
        consulAccountHost = FMCommon.consul_operater(host=userData['consulHost'], port=userData['consulPort'],
                                                     server='followme.srv.account', key='ServiceAddress')
        consulAccountPort = FMCommon.consul_operater(host=userData['consulHost'], port=userData['consulPort'],
                                                     server='followme.srv.account', key='ServicePort')
        accountChannel = grpc.insecure_channel(consulAccountHost + ':' + str(consulAccountPort))
        self.accountStub = account_pb2_grpc.AccountSrvStub(accountChannel)
        # 连接dealer测试服务器  http://10.1.0.4:8500
        consulDealerHost = FMCommon.consul_operater(host=userData['consulHost'], port=userData['consulPort'],
                                                    server='followme.srv.copytrade.dealer.pico', key='ServiceAddress')
        consulDealerPort = FMCommon.consul_operater(host=userData['consulHost'], port=userData['consulPort'],
                                                    server='followme.srv.copytrade.dealer.pico', key='ServicePort')
        # print(consulDealerHost + ':' + str(consulDealerPort))
        dealerChannel = grpc.insecure_channel(consulDealerHost + ':' + str(consulDealerPort))
        self.dealerStub = mt4dealer_pb2_grpc.MT4DealerSrvStub(dealerChannel)


        ###dev 环境连接信息 ++++++++++++++++++++++++++++++++
        #连接account测试服务器
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

    def test_test1(self):
        # self.userID = 169204
        # self.isTrader = False      #交易员：1， 跟随者：0
        # self.accountType = 3

        for userInfo in load_dict["items"]:
            print("isTrader:",userInfo["isTrader"])
            if userInfo["accountType"] == 3:
                self.group = 'a_balance'
            elif userInfo["accountType"] == 1:
                self.group = 'ct_pico'

            bindPico = self.dealerStub.CreateAccount(mt4dealer_pb2.Account(Name='MAM_ACCOUNT_' + str(userInfo["UserID"]),
                                                                       Password='abc123', BrokerID=1, Group=self.group,
                                                                       City='sz'))
            print(bindPico)
            self.login = bindPico.Login
            self.assertEqual(bindPico.Name, "MAM_ACCOUNT_" + str(userInfo["UserID"]))
            # 断言绑定的经济商为：1. 晋峰
            self.assertEqual(bindPico.BrokerID, 1)

            # 将注册的用户提取到t_useraccount表
            # accounttype:Demo = 0,Real = 1,Sam  = 2,Mam  = 3
            saveUserAccount = self.accountStub.SaveUserAccount(
                account_pb2.SaveUserAccountRequest(User=account_pb2.User(Id=userInfo["UserID"]),
                                                   BrokerID=1, MT4Account=str(self.login), IsTrader=userInfo["isTrader"],
                                                   AccountCreateType=0, IsBind=2, AccountType=userInfo["accountType"]))
            self.assertEqual(saveUserAccount.Success, 0)


            # pico入金
            self.dealerStub.DepositWithdraw(mt4dealer_pb2.DepositWithdrawMessage(Login=self.login,
                                                                             Price=userInfo["price"],
                                                                             Comment='Deposit With script.'))
    def test_CreateKVBOrMiniOrFXCM(self):
         for userInfo in load_dict["items"]:
             print("isTrader:",userInfo["isTrader"])
             # # 将注册的用户提取到t_useraccount表
             # accounttype:Demo = 0,Real = 1,Sam  = 2,Mam  = 3
             # Mt4Account: 是str类型，必填
             # saveUserAccount = self.accountStub.SaveUserAccount(
             #    account_pb2.SaveUserAccountRequest(User=account_pb2.User(Id=userInfo["UserID"]),
             #                                       BrokerID=userInfo["BrokerID"], MT4Account=userInfo["Mt4Account"], IsTrader=userInfo["isTrader"],
             #                                       AccountCreateType=0, IsBind=2, AccountType=userInfo["accountType"]))
             # self.assertEqual(saveUserAccount.Success, 0,'开设账户失败！')

             if userInfo["BrokerID"] == 5 or userInfo["BrokerID"] == 4:
                    #T_MT4Users表插入数与账号审核
                    sql1 = """INSERT INTO [dbo].[T_MT4Users]
           ([LOGIN],[BrokerID],[ENABLE],[GROUP],[REGDATE],[LASTDATE],[BALANCE],[PREVMONTHBALANCE]
           ,[PREVBALANCE],[CREDIT],[INTERESTRATE],[EQUITY],[MARGIN],[MARGIN_LEVEL],[MARGIN_FREE],[MODIFY_TIME]
           ,[gidt],[ManagerAccount])
     VALUES ('%s',%d,0,NULL,getdate(),getdate(),0,0,0,0,0,0,0,0,0,getdate(),NULL,'')""" % (userInfo["Mt4Account"],userInfo["BrokerID"])
                    #账号升级审核
                    sql2 = """INSERT INTO [FM_OS_V3].[dbo].[U_UserAccountAudit]
           ([UserId],[BrokerId],[IsBind],[UserType],[AuditStatus],[MT4Account],[ManageerAccount],
           [CreateTime],[AuditTime],[BALANCE],[JoinStatus],[Remark],[GetedAccountTime],[BindTime])
     VALUES (%d,%d,0,%d,3,'%s','d16994402',getdate(),getdate(),0,1,NULL,getdate(),getdate())""" % (userInfo["UserID"],userInfo["BrokerID"],userInfo["UserType"],userInfo["Mt4Account"])
                    time.sleep(3)
                    fmrs=FMCommon.mssql_operater_commit(host=userDataAPI['dataHost'],port=userDataAPI['dataPost'],database=userDataAPI['database_V3'],uid=userDataAPI['dataID'],pwd=userDataAPI['dataPWD'],sql=sql1)
                    time.sleep(3)
                    fmrs2=FMCommon.mssql_operater_commit(host=userDataAPI['dataHost'],port=userDataAPI['dataPost'],database=userDataAPI['database_V3'],uid=userDataAPI['dataID'],pwd=userDataAPI['dataPWD'],sql=sql2)
    def tearDown(self):
        pass
if __name__ == '__main__':
    unittest.main()
