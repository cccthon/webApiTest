# -*-coding:utf-8-*- 
#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_get_Accounts
# 用例标题: 获取交易大赛的账户列表
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
        print(self.jydstradeSignin.cookies)
        print("HTTP Cookies响应结束")
        localCookies = {'Cookie' : 'followme-jyds-beta=' + self.jydstradeSignin.cookies['followme-jyds-beta']}
        self.get_Accounts = Tradegame.get_Accounts(webAPIData['hostName'] + tradegameData['get_accounts_url'] ,headers = localCookies ,interfaceName='get_Account')
        

    def test_1_getChoiceTrades_checkscore(self):
        # 展示账号所有的交易员
        target=[]
        data = json.loads(self.get_Accounts.text)["data"]["items"]
        print(data)
        print('输出源数据：')
        for  i in data:          
            temp = {'MT4Account':i['MT4Account'] , 'BrokerName':i['BrokerName'] }
            print(temp)
            target.append(temp)

        MT4AccountList=[]
        BrokerNameList=[]
        for item in target:
            MT4AccountList.append(item["MT4Account"])
            BrokerNameList.append(item["BrokerName"])
        MT4AccountList.sort()
        BrokerNameList.sort()

        MT4Account = ['2100000005', '00996393', '830005','79935','2100004852','8955007','12279626','8449223','9442065','20001252','942607','44123750','434252547']
        BrokerName = ['RH晋峰环球国际','FXCM福汇','KVB昆仑国际','KVB昆仑国际','RH晋峰环球国际','ADS达汇','Alpari艾福瑞','AxiTrader','easyMarkets易信','IFMTrade','Pepperstone激石','ThinkMarkets智汇','FOREX.COM嘉盛']
        MT4Account.sort()
        BrokerName.sort()
        self.assertListEqual(MT4AccountList,MT4Account)
        self.assertListEqual(BrokerNameList,BrokerName)

    def tearDown(self):
        
        #清空测试环境，还原测试数据
        #登出followme系统
        tradeSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.tradeHeaders,printLogs=0)
        self.assertEqual(tradeSignout.status_code, webAPIData['status_code_200'])


if __name__ == '__main__':
    unittest.main()

