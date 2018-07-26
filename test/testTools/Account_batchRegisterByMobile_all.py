#========================================================
#+++++++++++++++++  测试工具信息   ++++++++++++++++
# 批量注册帐号，绑定pico、fxcm、kvb、kvbmini，入金等
#=========================================================
import grpc,sys,unittest,yaml,json,uuid,pymysql,time
sys.path.append("../../lib/proto")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
import FMCommon,consul,Account,Auth
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

# userData = json.loads(open('register1.json', 'r',encoding='utf-8'))
userData = yaml.load(open('../../conf/common/common.yml', 'r',encoding='utf-8'))
webApiData = FMCommon.loadWebAPIYML()
userDataAccountUrl=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()

with open("register.json",'r',encoding='utf-8') as load_file:
    load_dict = json.load(load_file)

class RegisterByEmail(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        consulAccountHost = FMCommon.consul_operater(host=userData['consulHost'],port=userData['consulPort'],server='followme.srv.account',key='ServiceAddress')
        consulAccountPort = FMCommon.consul_operater(host=userData['consulHost'],port=userData['consulPort'],server='followme.srv.account',key='ServicePort')
        print(consulAccountHost + ':' + str(consulAccountPort))
        accountChannel = grpc.insecure_channel(consulAccountHost + ':' + str(consulAccountPort))
        self.accountStub = account_pb2_grpc.AccountSrvStub(accountChannel)

        #连接dealer测试服务器  http://10.1.0.4:8500   
        consulDealerHost = FMCommon.consul_operater(host=userData['consulHost'],port=userData['consulPort'],server='followme.srv.copytrade.dealer.pico',key='ServiceAddress')
        consulDealerPort = FMCommon.consul_operater(host=userData['consulHost'],port=userData['consulPort'],server='followme.srv.copytrade.dealer.pico',key='ServicePort')  
        print(consulDealerHost + ':' + str(consulDealerPort))
        dealerChannel = grpc.insecure_channel(consulDealerHost + ':' + str(consulDealerPort))
        self.dealerStub = mt4dealer_pb2_grpc.MT4DealerSrvStub(dealerChannel)
        
    def test_RegisterByEmail(self):
        for userInfo in load_dict["items"]:
            # print(userInfo["Mobile"])
            # 注册一个测试账号
            print("bind.")

            #获取图形验证码
            captchaUrl=webApiData['hostName']+userDataAuthUrl['getCaptcha_url']
            self.user_token=Account.getTokenForCaptcha(captchaUrl)
            self.header={'content-type': 'application/json', 'Authorization': 'Bearer ' + str(self.user_token)}
            #读取图形验证码
            self.ccap =Account.getCaptchaForRedis(self.user_token)
            #根据图形验证码获取短信验证码
            smsUrl=webApiData['hostName'] + userDataAuthUrl['getSMSScode_url'] + userInfo["Mobile"]+'&captcha='+ self.ccap
            # print(smsUrl)
            '''获取短信验证码成功'''
            self.smsCode = Account.getSMSCodeForRedis(smsUrl, headers=self.header,userToken=str(self.user_token),registerAccount=userInfo["Mobile"])

            '''注册场景验证'''
            #注册
            url=webApiData['hostName']+userDataAuthUrl['register_url']
            res=Auth.register(url,headers=self.header,account=userInfo["Mobile"],
                                  password=webApiData['registerPwd'],platform=webApiData['platform'],captcha=str(self.ccap),
                                  smscode=self.smsCode,invite=webApiData['invite'],oauth2=webApiData['oauth2'])
            #请求成功，返回200 ok
            '''注册成功'''
            self.assertEqual(res.status_code,webApiData['status_code_200'])
            self.userID = json.loads(res.text)["data"]["id"]

            #设置用户昵称
            setNickName = self.accountStub.SetNickName(account_pb2.User(Id = self.userID,NickName = userInfo["NickName"]))
            #检查设置成功后，返回值为：0
            self.assertEqual(setNickName.Success, 0)

            for key in userInfo["AccountList"]:
                
                if key["bind"] == "true": 
                    time.sleep(2)
                    #将注册的用户提取到t_useraccount表
                    #accounttype:Demo = 0,Real = 1,Sam  = 2,Mam  = 3
                    print("select * from ",self.userID,key["BrokerID"],key["Mt4Account"],key["UserType"],key["AccountType"])
                    saveUserAccount = self.accountStub.SaveUserAccount(account_pb2.SaveUserAccountRequest(User = account_pb2.User(Id = self.userID),
                        BrokerID = key["BrokerID"], MT4Account = str(key["Mt4Account"]), IsTrader = key["UserType"], AccountCreateType = 0, IsBind = 2,AccountType = key["AccountType"]))
                    self.assertEqual(saveUserAccount.Success, 0)

                if key["BrokerID"] == 1:
                    #pico入金
                    print("Deposit")
                    self.dealerStub.DepositWithdraw(mt4dealer_pb2.DepositWithdrawMessage(Login = int(key["Mt4Account"]),
                        Price = 999999, Comment = 'Deposit With script.'))

                if key["BrokerID"] == 5 or key["BrokerID"] == 4:
                    #T_MT4Users表插入数与账号审核
                    sql1 = """INSERT INTO [dbo].[T_MT4Users]
           ([LOGIN],[BrokerID],[ENABLE],[GROUP],[REGDATE],[LASTDATE],[BALANCE],[PREVMONTHBALANCE]
           ,[PREVBALANCE],[CREDIT],[INTERESTRATE],[EQUITY],[MARGIN],[MARGIN_LEVEL],[MARGIN_FREE],[MODIFY_TIME]
           ,[gidt],[ManagerAccount])
     VALUES ('%s',%d,0,NULL,getdate(),getdate(),0,0,0,0,0,0,0,0,0,getdate(),NULL,'')""" % (key["Mt4Account"],key["BrokerID"])
                    #账号升级审核
                    sql2 = """INSERT INTO [FM_OS_V3].[dbo].[U_UserAccountAudit]
           ([UserId],[BrokerId],[IsBind],[UserType],[AuditStatus],[MT4Account],[ManageerAccount],
           [CreateTime],[AuditTime],[BALANCE],[JoinStatus],[Remark],[GetedAccountTime],[BindTime])
     VALUES (%d,%d,0,%d,3,'%s','d16994402',getdate(),getdate(),0,1,NULL,getdate(),getdate())""" % (self.userID,key["BrokerID"],key["UserType"],key["Mt4Account"])
                    time.sleep(1)
                    FMCommon.mssql_operaters(host=webApiData['dataHost'],port=webApiData['dataPost'],database=webApiData['database_V3'],uid=webApiData['dataID'],pwd=webApiData['dataPWD'],sql=sql1)
                    time.sleep(1)
                    FMCommon.mssql_operaters(host=webApiData['dataHost'],port=webApiData['dataPost'],database=webApiData['database_V3'],uid=webApiData['dataID'],pwd=webApiData['dataPWD'],sql=sql2)




            # 注销测试账号
            # unregister = self.accountStub.DeleteUserById(account_pb2.User(Id = self.userID))
            # # 断言注销账号成功，返回0
            # print(unregister)
            # self.assertEqual(unregister.Success, 0)




    def tearDown(self):
        #本用例由于空密码未注册成功，所以不需要注销账号。故注销账号步骤单独写到注销成功的测试方法里
        #清空测试环境
        #退出登录
        pass
        # 注销测试账号
        # unregister = self.accountStub.CloseAccount(account_pb2.User(Id = 169121))
        # # 断言注销账号成功，返回0
        # print(unregister)
        # self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()