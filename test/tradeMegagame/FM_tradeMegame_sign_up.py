# -*-coding:utf-8-*- 
#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_trademagame_sign_up
# 用例标题: 交易大赛报名超过2个账户（需要登录） 
# 预置条件: 
# 测试步骤:
#   1.
# 预期结果:
#   1.风控设置返回成功
#   2.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20171213
#=========================================================
import sys,unittest,json,requests,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,Auth,RiskControl,Follow,FollowManage,TradeOnline,Account,Order,Social,Tradegame
from socketIO_client import SocketIO
from base64 import b64encode

tradeOnlineData = FMCommon.loadTradeOnlineYML()
webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
riskControlData = FMCommon.loadRiskControlYML()
followData = FMCommon.loadFollowYML()
orderData = FMCommon.loadOrderYML()
accountData = FMCommon.loadAccountYML()
tradegameData = FMCommon.loadTradegameYML()


class FollowMulti_pcio(unittest.TestCase):
    target=[]
    localCookies = {}
    def setUp(self):
        #交易员FMS004 晋峰登陆---------------------
        tradeDatas = {"account":webAPIData['account_1'], "password":webAPIData['passwd_1'], "remember":"false"}
        tradeSignin = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], tradeDatas)
        # 登录成功，返回200 ok
        self.assertEqual(tradeSignin.status_code, webAPIData['status_code_200'])
        #保存账号的nickName,待获取userID使用
        self.tradeNickName = json.loads(tradeSignin.text)['data']['nickname']
        
        # #保存登录时的token，待登出使用
        self.tradeUserToken = json.loads(tradeSignin.text)['data']['token']
        #保存userID
        self.tradeUserID = json.loads(tradeSignin.text)['data']['id']
        #规整headers
        self.tradeHeaders = dict(webAPIData['headers'], **{webAPIData['Authorization'] : webAPIData['Bearer'] + self.tradeUserToken})
        jydstradeDatas = {"token":self.tradeUserToken}
        self.jydstradeSignin = Tradegame.jydssignin(webAPIData['hostName'] + tradegameData['get_jydssignin_url'] , webAPIData['headers'], jydstradeDatas)
        print("HTTP Cookies响应：")
        print(self.jydstradeSignin.cookies['followme-jyds-beta'])
        print("HTTP Cookies响应结束")
        self.localCookies = {'Cookie' : 'followme-jyds-beta=' + self.jydstradeSignin.cookies['followme-jyds-beta']}
        self.get_Accounts = Tradegame.get_Accounts(webAPIData['hostName'] + tradegameData['get_accounts_url'] ,headers = self.localCookies ,interfaceName='get_Account')
        
        for  item in json.loads(self.get_Accounts.text)["data"]["items"]:          
            self.target.append(item["MT4Account"])

    def test_1_getChoiceTrades_checkscore(self):
        #同个账号的第3个账户参加交易大赛，可以参加
        self.trades = Tradegame.sign_up(webAPIData['hostName'] + tradegameData['sign_up_url'],headers = self.localCookies,datas = {"Account":self.target[0]},printLogs=0)
        self.assertEqual(self.trades.status_code, webAPIData['status_code_200'])
        data = json.loads(self.trades.text)

        self.assertEqual(data["msg"], "已过报名时间")

    def tearDown(self):
        #登出followme系统
        tradeSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.tradeHeaders,printLogs=0)
        self.assertEqual(tradeSignout.status_code, webAPIData['status_code_200'])
        #取消参加交易大赛

if __name__ == '__main__':
    unittest.main()

