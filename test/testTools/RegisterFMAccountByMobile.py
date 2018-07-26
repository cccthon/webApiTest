#========================================================
#+++++++++++++++++  测试工具信息   ++++++++++++++++
# 通过手机号注册单个fm帐号
# 注意修改47-50行的配置
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

class UpgradeStar(unittest.TestCase):

    def setUp(self):
        # 连接account测试服务器
        consulAccountHost = FMCommon.consul_operater(host=userData['consulHost'], port=userData['consulPort'],
                                                     server='followme.srv.account', key='ServiceAddress')
        consulAccountPort = FMCommon.consul_operater(host=userData['consulHost'], port=userData['consulPort'],
                                                     server='followme.srv.account', key='ServicePort')
        print(consulAccountHost + ':' + str(consulAccountPort))
        accountChannel = grpc.insecure_channel(consulAccountHost + ':' + str(consulAccountPort))
        self.accountStub = account_pb2_grpc.AccountSrvStub(accountChannel)

        # 连接dealer测试服务器  http://10.1.0.4:8500
        consulDealerHost = FMCommon.consul_operater(host=userData['consulHost'], port=userData['consulPort'],
                                                    server='followme.srv.copytrade.dealer.pico', key='ServiceAddress')
        consulDealerPort = FMCommon.consul_operater(host=userData['consulHost'], port=userData['consulPort'],
                                                    server='followme.srv.copytrade.dealer.pico', key='ServicePort')
        print(consulDealerHost + ':' + str(consulDealerPort))
        dealerChannel = grpc.insecure_channel(consulDealerHost + ':' + str(consulDealerPort))
        self.dealerStub = mt4dealer_pb2_grpc.MT4DealerSrvStub(dealerChannel)

    def test_registerAndLogin(self):
        #注册账号
        #开户
        #验证是否升级为2星
        self.mobile = '18766666668'
        self.password = '123456'
        self.invite = '220432'  # vcode 信息。
        # 注册一个测试账号
        # 获取图形验证码
        captchaUrl = webApiData['hostName'] + userDataAuthUrl['getCaptcha_url']
        self.user_token = Account.getTokenForCaptcha(captchaUrl)
        self.header = {'content-type': 'application/json', 'Authorization': 'Bearer ' + str(self.user_token)}
        # 读取图形验证码
        self.ccap = Account.getCaptchaForRedis(self.user_token)
        # 根据图形验证码获取短信验证码
        smsUrl = webApiData['hostName'] + userDataAuthUrl['getSMSScode_url'] + self.mobile + '&captcha=' + self.ccap
        # print(smsUrl)
        '''获取短信验证码成功'''
        self.smsCode = Account.getSMSCodeForRedis(smsUrl, headers=self.header, userToken=str(self.user_token),
                                                  registerAccount=self.mobile)

        '''注册场景验证'''
        # 注册
        url = webApiData['hostName'] + userDataAuthUrl['register_url']
        res = Auth.register(url, headers=self.header, account=self.mobile,
                            password=self.password, platform=webApiData['platform'], captcha=str(self.ccap),
                            smscode=self.smsCode, invite=self.invite, oauth2=webApiData['oauth2'])
        # 请求成功，返回200 ok
        '''注册成功'''
        self.assertEqual(res.status_code, webApiData['status_code_200'])
        self.userID = json.loads(res.text)["data"]["id"]
        print("userID ", self.userID)
        print("mobile ", self.mobile)
        # 设置用户昵称
        setNickName = self.accountStub.SetNickName(account_pb2.User(Id=self.userID, NickName=str(self.userID)))
        # 检查设置成功后，返回值为：0
        self.assertEqual(setNickName.Success, 0)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()