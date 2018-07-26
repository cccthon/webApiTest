# -*-coding:utf-8-*- 
#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_maxAccountPositionLots_pcio
# 用例标题: 风控全局最大账户持仓手数测试
# 预置条件: 
# 测试步骤:
#   1.
# 预期结果:
#   1.风控设置返回成功
#   2.检查响应码为：200
# 脚本作者: shencanhui
# 写作日期: 20180708
#=========================================================
import sys,unittest,json,requests,time,grpc,datetime,threading
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
sys.path.append("../../lib/tradeSAM")
sys.path.append("../../lib/proto")
import FMCommon,Auth,RiskControl,Follow,FollowManage,TradeOnline,Account,Order,Social,TradeSAM
from socketIO_client import SocketIO
from threading import Thread
from base64 import b64encode
from mt4api import mt4api_pb2
from mt4api import mt4api_pb2_grpc
from tradesignal import tradesignal_pb2
from tradesignal import tradesignal_pb2_grpc

tradeOnlineData = FMCommon.loadTradeOnlineYML()
webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
riskControlData = FMCommon.loadRiskControlYML()
followData = FMCommon.loadFollowYML()
orderData = FMCommon.loadOrderYML()
accountData = FMCommon.loadAccountYML()
commonConf = FMCommon.loadPublicYML()

class MaxAccountPlsitionLots(unittest.TestCase):
    def setUp(self):
        #交易员登陆---------------------
        tradeDatas = {"account":webAPIData['account'], "password":webAPIData['passwd'], "remember":"false"}
        tradeSignin = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], tradeDatas)
        #登录成功，返回200 ok
        self.assertEqual(tradeSignin.status_code, webAPIData['status_code_200'])
        #保存账号的nickName,待获取userID使用
        self.tradeNickName = json.loads(tradeSignin.text)['data']['nickname']
        # #保存登录时的token，待登出使用
        self.tradeUserToken = json.loads(tradeSignin.text)['data']['token']
        #保存userID
        self.tradeUserID = json.loads(tradeSignin.text)['data']['id']
        #规整headers
        self.tradeHeaders = dict(webAPIData['headers'], **{webAPIData['Authorization'] : webAPIData['Bearer'] + self.tradeUserToken})
        #获取指定经纪商的accountIndex。当前为：pcio
        self.tradePicoAccountIndex = Account.getSpecialAccountIndex(headers = self.tradeHeaders,accountType=2, brokerID=106)[4]
        self.switchTradeAccount = Account.switchAccount(webAPIData['hostName'] + accountData['switchAccount'], self.tradeHeaders, index=self.tradePicoAccountIndex)
        #账号切换成功
        self.assertEqual(self.switchTradeAccount.status_code, webAPIData['status_code_200'])
        #获取交易员交易token
        self.tradeToken = Account.getToken(self.tradeHeaders, onlyTokn="true", printLogs=1)
        tokenRes = Account.getToken(self.tradeHeaders, printLogs=0)
        self.tradeMt4Account = json.loads(tokenRes.content)["data"]["MT4Account"]
        self.tradeBrokerID = json.loads(tokenRes.content)["data"]["BrokerId"]

        #跟随者登陆---------------------
        followDatas = {"account":webAPIData['followAccount'], "password":webAPIData['followPasswd'], "remember":"false"}
        followSignin = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], followDatas)
        #登录成功，返回200 ok
        self.assertEqual(followSignin.status_code, webAPIData['status_code_200'])
        #保存账号的nickName
        self.followNickName = json.loads(followSignin.text)['data']['nickname']
        # #保存登录时的token，待登出使用
        self.followUserToken = json.loads(followSignin.text)['data']['token']
        #规整headers
        self.followHeaders = dict(webAPIData['headers'], **{webAPIData['Authorization'] : webAPIData['Bearer'] + self.followUserToken})
        #获取指定经纪商的accountIndex。当前为：pcio
        self.followPicoAccountIndex = Account.getSpecialAccountIndex(headers = self.followHeaders, brokerID=riskControlData["testBrokerID"])[0]
        self.switchFollowAccount = Account.switchAccount(webAPIData['hostName'] + accountData['switchAccount'], self.followHeaders, index=self.followPicoAccountIndex)
        #账号切换成功
        self.assertEqual(self.switchFollowAccount.status_code, webAPIData['status_code_200'])
        #获取跟随者交易token
        self.followToken = Account.getToken(self.followHeaders, onlyTokn="true", printLogs=1)

        #一倍建立跟随
        self.tradeIndex = str(self.tradeUserID) + '_' + self.tradePicoAccountIndex
        #设置跟随策略
        followDatas = {"accountIndex": self.followPicoAccountIndex, webAPIData['followStrategy']: webAPIData['follow_ratio'], 
        webAPIData['follow_setting']: 1, webAPIData['followDirection']: webAPIData['follow_positive']}
        createFollow = FollowManage.createFollow(webAPIData['hostName'] + followData['createFollow_url'] + self.tradeIndex, headers = self.followHeaders, datas =followDatas, interfaceName="createFollow")
        #断言跟随成功
        self.assertEqual(createFollow.status_code, webAPIData['status_code_200'])

        #设置全局风控参数。账号最大持仓为：3
        globalRiskControlData = {webAPIData['signalSwitch']: webAPIData['signalSwitch_open'], webAPIData['maxPositionLots']: 3}
        setRiskControl = RiskControl.setRiskControl(webAPIData['hostName'] + riskControlData['setRiskControl_url'], accountIndex=self.followPicoAccountIndex, headers = self.followHeaders, datas=globalRiskControlData)
        self.assertEqual(setRiskControl.status_code, webAPIData['status_code_200'])

        #设置针对单个交易员的风控参数。初始为默认值
        specialTradeDatas = { "accountIndex": self.followPicoAccountIndex}
        setRiskControlForTrader = RiskControl.setRiskControlForTrader(webAPIData['hostName'] + riskControlData['setRiskControlForTrader_url'] + self.tradeIndex, headers=self.followHeaders, datas=specialTradeDatas, interfaceName="setRiskControlForTrader")
        self.assertEqual(setRiskControlForTrader.status_code, webAPIData['status_code_200'])
        
        #
        '''测试Sam经纪商开仓,平仓,历史订单'''
        host = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],server='followme.srv.mt4api.3', key='ServiceAddress')
        port = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],server='followme.srv.mt4api.3', key='ServicePort')
        channel = grpc.insecure_channel(host + ':' + str(port))
        print(channel,host + ':' + str(port))
        self.stub = mt4api_pb2_grpc.MT4APISrvStub(channel)

    def test_maxPositionLots_tradeEqual(self):
        '''账号持仓总手数设置为3，交易员买3手。验证跟随者跟随订单情况'''
        #下单时的手数为实际值除以100(300/100)
        print("curr time:",datetime.datetime.now())
        client = TradeSAM.TradeSAMStream

        def myThread():
            print("curr time:",datetime.datetime.now())
            '''sam 开仓'''
            openRes = client.OpenPosition(stub=self.stub,account=self.tradeMt4Account,brokerID=self.tradeBrokerID,symbol=tradeOnlineData['broker_EURCAD'],cmd=1,lots=0.2)
            self.tradeID = openRes.Signal.TradeID
            self.assertEqual(openRes.Signal.Symbol, tradeOnlineData['broker_EURCAD'])
            self.assertEqual(openRes.Signal.Lots, 0.2)
            time.sleep(1)
            # 平仓
            closeRes = TradeSAM.TradeSAMStream.ClosePosition(stub=self.stub, account=self.tradeMt4Account, brokerID=self.tradeBrokerID, tradeID=self.tradeID, lots=0.2)
            self.assertEqual(closeRes.Signal.TradeID, self.tradeID)
            self.assertEqual(closeRes.Signal.Symbol, tradeOnlineData['broker_EURCAD'])
            # time.sleep(2)

        # 启动N个线程
        for i in range(500):
            t =threading.Thread(target=myThread)
            t.start()

    def tearDown(self):
        #清空测试环境，还原测试数据
        #清除所有测试订单，如果有
        #还原风控参数
        #设置全局风控参数。关闭风控信号
        globalRiskControlData = {webAPIData['signalSwitch']: webAPIData['signalSwitch_open']}
        setRiskControl = RiskControl.setRiskControl(webAPIData['hostName'] + riskControlData['setRiskControl_url'], accountIndex=self.followPicoAccountIndex, headers = self.followHeaders, datas=globalRiskControlData)
        self.assertEqual(setRiskControl.status_code, webAPIData['status_code_200'])
        #设置针对单个交易员的风控参数。初始为默认值
        specialTradeDatas = { "accountIndex": self.followPicoAccountIndex}
        setRiskControlForTrader = RiskControl.setRiskControlForTrader(webAPIData['hostName'] + riskControlData['setRiskControlForTrader_url'] + self.tradeIndex, headers=self.followHeaders, datas=specialTradeDatas, interfaceName="setRiskControlForTrader")
        self.assertEqual(setRiskControlForTrader.status_code, webAPIData['status_code_200'])

        # 取消跟随关系
        deleteFollow = FollowManage.deleteFollow(webAPIData['hostName'] + followData['deleteFollow_url'] + self.tradeIndex, headers = self.followHeaders, accountIndex=self.followPicoAccountIndex)
        self.assertEqual(deleteFollow.status_code, webAPIData['status_code_200'])

        #登出followme系统
        tradeSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.tradeHeaders)
        self.assertEqual(tradeSignout.status_code, webAPIData['status_code_200'])
        followSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.followHeaders)
        self.assertEqual(followSignout.status_code, webAPIData['status_code_200'])

if __name__ == '__main__':
    unittest.main()

