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
# 写作日期: 20171213
#=========================================================
import sys,unittest,json,requests,time,grpc
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,Auth,RiskControl,Follow,FollowManage,TradeOnline,Account,Order,Social
from socketIO_client import SocketIO
from base64 import b64encode
sys.path.append("../../lib/proto")
sys.path.append("../../lib/tradeSAM")
import FMCommon,TradeSAM
from mt4api import mt4api_pb2
from mt4api import mt4api_pb2_grpc
from tradesignal import tradesignal_pb2
from tradesignal import tradesignal_pb2_grpc

commonConf = FMCommon.loadPublicYML()
tradeOnlineData = FMCommon.loadTradeOnlineYML()
webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
riskControlData = FMCommon.loadRiskControlYML()
followData = FMCommon.loadFollowYML()
orderData = FMCommon.loadOrderYML()
accountData = FMCommon.loadAccountYML()

class MaxAccountPlsitionLots(unittest.TestCase):
    def setUp(self):
        '''测试Sam经纪商开仓,平仓,历史订单'''
        host = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],
                                                         server='followme.srv.mt4api.3', key='ServiceAddress')
        port = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],
                                                         server='followme.srv.mt4api.3', key='ServicePort')
        channel = grpc.insecure_channel(host + ':' + str(port))
        print(channel,host + ':' + str(port))
        self.stub = mt4api_pb2_grpc.MT4APISrvStub(channel)

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

    def test_maxPositionLots_tradeEqual(self):
        #交易员登陆---------------------
        tradeDatas = {"account":webAPIData['account1'], "password":webAPIData['passwd'], "remember":"false"}
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
        # self.tradePicoAccountIndex = Account.getSpecialAccountIndex(headers = self.tradeHeaders, brokerID=riskControlData["testBrokerID"])[0]
        #获取账户列表
        self.getAccounts = Account.getAccounts(webAPIData['hostName'] + accountData['getAccounts_url'] + accountData['getAccounts_url2'],headers = self.tradeHeaders)
        print("获取账户列表")
        print(self.getAccounts.text)
        self.tradeTokenList = []
        self.tradeAccountIndexList = []

        for i in json.loads(self.getAccounts.text)["data"]["accounts"]:
            if i["AccountIndex"] != -1:



                self.switchTradeAccount = Account.switchAccount(webAPIData['hostName'] + accountData['switchAccount'], self.tradeHeaders, index=str(i["AccountIndex"]))
                #账号切换成功
                self.assertEqual(self.switchTradeAccount.status_code, webAPIData['status_code_200'])
                # 获取交易员交易token
                self.tradeToken = Account.getToken(self.tradeHeaders, onlyTokn="true", printLogs=0)
                self.tradeTokenList.append(self.tradeToken)
                self.tradeAccountIndexList.append(i["AccountIndex"])
                print("获取交易token")
                print(self.tradeTokenList)
                print(self.tradeAccountIndexList)

                if i["AccountIndex"] != 1:
                    #一倍建立跟随
                    self.tradeIndex = str(self.tradeUserID) + '_' + str(i["AccountIndex"])
                    #设置跟随策略
                    followDatas = {"accountIndex": self.followPicoAccountIndex, webAPIData['followStrategy']: webAPIData['follow_ratio'], 
                    webAPIData['follow_setting']: 1, webAPIData['followDirection']: webAPIData['follow_positive']}
                    createFollow = FollowManage.createFollow(webAPIData['hostName'] + followData['createFollow_url'] + self.tradeIndex, headers = self.followHeaders, datas =followDatas, interfaceName="createFollow")
                    #断言跟随成功
                    self.assertEqual(createFollow.status_code, webAPIData['status_code_200'])

                # #设置全局风控参数。账号最大持仓为：3
                # globalRiskControlData = {webAPIData['signalSwitch']: webAPIData['signalSwitch_open'], webAPIData['maxPositionLots']: 3}
                # setRiskControl = RiskControl.setRiskControl(webAPIData['hostName'] + riskControlData['setRiskControl_url'], accountIndex=self.followPicoAccountIndex, headers = self.followHeaders, datas=globalRiskControlData)
                # self.assertEqual(setRiskControl.status_code, webAPIData['status_code_200'])

                # #设置针对单个交易员的风控参数。初始为默认值
                # specialTradeDatas = { "accountIndex": self.followPicoAccountIndex}
                # setRiskControlForTrader = RiskControl.setRiskControlForTrader(webAPIData['hostName'] + riskControlData['setRiskControlForTrader_url'] + self.tradeIndex, headers=self.followHeaders, datas=specialTradeDatas, interfaceName="setRiskControlForTrader")
                # self.assertEqual(setRiskControlForTrader.status_code, webAPIData['status_code_200'])
                # '''账号持仓总手数设置为3，交易员买3手。验证跟随者跟随订单情况'''

        client = TradeSAM.TradeSAMStream

        for i in self.tradeTokenList:
            for j in self.tradeAccountIndexList:
                if j == 7:
                    openRes = client.OpenPosition(stub=self.stub,account='500387412',brokerID=106,symbol='AUDCAD',cmd=1,lots=0.1)
                    self.tradeID = openRes.Signal.TradeID
                    self.assertEqual(openRes.Signal.Symbol, 'AUDCAD')
                if i != 'aXfzzechszGEcZz/x2WZ+bDRpzjzAOvx':
                    print("jjjjjjjjjjjjjjjjjjjjj",j,i)

                    openParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_210'], tradeOnlineData['orderParam_symbol']: tradeOnlineData['broker_EURCAD'], tradeOnlineData['orderParam_volume']: 300 }
                    openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': i}, openParam)
                    #校验code等于0，为及时单开仓成功
                    self.assertEqual(openPositionRes["code"], tradeOnlineData['ws_code_0'])
                if j == 3:
                    print("fxcm,mmmmmmmmmmmmmmmm",j,i)

                    openParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_210'], tradeOnlineData['orderParam_symbol']: 'EUR/CAD', tradeOnlineData['orderParam_volume']: 300 }
                    openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': i}, openParam)
                    #校验code等于0，为及时单开仓成功
                    self.assertEqual(openPositionRes["code"], tradeOnlineData['ws_code_0'])
        
        # #获取订单的跟随订单
        # getFollowOrdersOfOrder = Order.getFollowOrdersOfOrder(webAPIData['hostName'] + orderData['getFollowOrdersOfOrder_url1'], headers = self.tradeHeaders,params={"pageSize":100}, tradeOrderID = str(self.orderID))
        # #断言获取跟随订单成功
        # self.assertEqual(getFollowOrdersOfOrder.status_code, webAPIData['status_code_200'])
        # #断言当前的测试用户有跟随订单
        # nickNameOfOrderList = []
        # for item in json.loads(getFollowOrdersOfOrder.text)["data"]["items"]:
        #     nickNameOfOrderList.append(item['CustomerNickName'])
        # self.assertIn(self.followNickName, nickNameOfOrderList,"当前测试用户未生成跟随订单")

        # getFollowOrder = FollowManage.getFollowOrder(getFollowOrdersOfOrder, nickName=self.followNickName, accountIndex=self.followPicoAccountIndex)
        # #断言跟随者订单跟随的品种为：EURCAD
        # self.assertEqual(getFollowOrder['SYMBOL'], tradeOnlineData['broker_EURCAD'])
        # #断言跟随者订单跟随的手数为：3手
        # self.assertEqual(getFollowOrder['VOLUME'], 3)


        
    # def test_maxPositionLots_tradeEqual(self):
    #     print("test")
    #     '''账号持仓总手数设置为3，交易员买3手。验证跟随者跟随订单情况'''
    #     #下单时的手数为实际值除以100(300/100)
    #     openParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_210'], tradeOnlineData['orderParam_symbol']: tradeOnlineData['broker_EURCAD'], tradeOnlineData['orderParam_volume']: 300 }
    #     openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.tradeToken}, openParam)
    #     #校验code等于0，为及时单开仓成功
    #     self.assertEqual(openPositionRes["code"], tradeOnlineData['ws_code_0'])
    #     #校验手数为下单时的手数为实际值除以100(300/100)
    #     self.assertEqual(openPositionRes["order"]["volume"], 300)
    #     #保存orderID,待开仓使用
    #     self.orderID = openPositionRes["order"]["order_id"]

    #     #获取订单的跟随订单
    #     getFollowOrdersOfOrder = Order.getFollowOrdersOfOrder(webAPIData['hostName'] + orderData['getFollowOrdersOfOrder_url1'], headers = self.tradeHeaders,params={"pageSize":100}, tradeOrderID = str(self.orderID))
    #     #断言获取跟随订单成功
    #     self.assertEqual(getFollowOrdersOfOrder.status_code, webAPIData['status_code_200'])
    #     #断言当前的测试用户有跟随订单
    #     nickNameOfOrderList = []
    #     for item in json.loads(getFollowOrdersOfOrder.text)["data"]["items"]:
    #         nickNameOfOrderList.append(item['CustomerNickName'])
    #     self.assertIn(self.followNickName, nickNameOfOrderList,"当前测试用户未生成跟随订单")

    #     getFollowOrder = FollowManage.getFollowOrder(getFollowOrdersOfOrder, nickName=self.followNickName, accountIndex=self.followPicoAccountIndex)
    #     #断言跟随者订单跟随的品种为：EURCAD
    #     self.assertEqual(getFollowOrder['SYMBOL'], tradeOnlineData['broker_EURCAD'])
    #     #断言跟随者订单跟随的手数为：3手
    #     self.assertEqual(getFollowOrder['VOLUME'], 3)

    #     #平掉测试订单
    #     closeParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_211'], tradeOnlineData['orderParam_ticket']: self.orderID, tradeOnlineData['orderParam_volume']: 300 }
    #     closePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.tradeToken}, closeParam)
    #     #校验code等于0，为及时单平仓成功
    #     self.assertEqual(closePositionRes["code"], tradeOnlineData['ws_code_0'])
    #     #校验rcmd等于210，为及时单开仓
    #     self.assertEqual(closePositionRes["rcmd"], tradeOnlineData['ws_code_211'])
    #     #校验平掉的单号，为本测试及时单开仓的单号
    #     self.assertEqual(closePositionRes['order']["order_id"], self.orderID)


    def tearDown(self):
        #清空测试环境，还原测试数据
        #清除所有测试订单，如果有
        '''获取交易员的所有交易订单，并平掉'''
        tradeOrderParams = {webAPIData['orderStatus']:webAPIData['orderStatus_open']}
        getTradeOrders = Order.getOrders(webAPIData['hostName'] + orderData['getOrders_url'], self.tradeHeaders, params=tradeOrderParams)
        #获取订单成功，返回200 ok
        self.assertEqual(getTradeOrders.status_code, webAPIData['status_code_200'])
        tradeOrdersIDList = Order.getOrdersID(getTradeOrders)
        #平掉当前用户所有订单,如果有
        # #web sockets批量平仓
        closeParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_219'], tradeOnlineData['orderParam_tickets']: tradeOrdersIDList }
        closePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.tradeToken}, closeParam)
        #校验code等于0，为及时单平仓成功
        # self.assertEqual(closePositionRes["code"], tradeOnlineData['ws_code_0'])

        '''获取跟随者的所有交易订单，并平掉'''
        followOrderParams = {webAPIData['orderStatus']:webAPIData['orderStatus_open']}
        getFollowOrders = Order.getOrders(webAPIData['hostName'] + orderData['getOrders_url'], self.followHeaders, params=followOrderParams)
        #获取订单成功，返回200 ok
        self.assertEqual(getFollowOrders.status_code, webAPIData['status_code_200'])
        followOrdersIDList = Order.getOrdersID(getFollowOrders)
        #平掉当前用户所有订单,如果有
        # #web sockets批量平仓
        closeParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_219'], tradeOnlineData['orderParam_tickets']: followOrdersIDList }
        closePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.followToken}, closeParam)
        #校验code等于0，为及时单平仓成功
        # self.assertEqual(closePositionRes["code"], tradeOnlineData['ws_code_0'])

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

