# -*-coding:utf-8-*- 
#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_stopFollowPeriods_pcio
# 用例标题: 风控停止跟随时间验证
# 预置条件: 
# 测试步骤:
#   1.
# 预期结果:
#   1.风控设置返回成功
#   2.检查响应码为：200
# 脚本作者: shencanhui
# 写作日期: 20171213
#=========================================================
import sys,unittest,json,requests,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,Auth,RiskControl,Follow,FollowManage,TradeOnline,Account,Order,Social
from socketIO_client import SocketIO
from base64 import b64encode

tradeOnlineData = FMCommon.loadTradeOnlineYML()
webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
riskControlData = FMCommon.loadRiskControlYML()
followData = FMCommon.loadFollowYML()
orderData = FMCommon.loadOrderYML()
accountData = FMCommon.loadAccountYML()

class StopFollowPeriods(unittest.TestCase):
    def setUp(self):
        #交易员登陆 ---------------------
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
        self.tradePicoAccountIndex = Account.getSpecialAccountIndex(headers = self.tradeHeaders, brokerID=riskControlData["testBrokerID"])[0]
        self.switchTradeAccount = Account.switchAccount(webAPIData['hostName'] + accountData['switchAccount'], self.tradeHeaders, index=self.tradePicoAccountIndex)
        #账号切换成功
        self.assertEqual(self.switchTradeAccount.status_code, webAPIData['status_code_200'])
        #获取交易员交易token
        self.tradeToken = Account.getToken(self.tradeHeaders, onlyTokn="true", printLogs=1)
        
        #跟随者登陆---------------------
        followDatas = {"account":webAPIData['followAccount'], "password":webAPIData['followPasswd'], "remember":"false"}
        followSignin = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], followDatas)
        #登录成功，返回200 ok
        self.assertEqual(followSignin.status_code, webAPIData['status_code_200'])
        # #保存登录时的token，待登出使用
        self.followUserToken = json.loads(followSignin.text)['data']['token']
        #规整headers
        self.followHeaders = dict(webAPIData['headers'], **{webAPIData['Authorization'] : webAPIData['Bearer'] + self.followUserToken})
        
        print(self.followHeaders)
        #获取指定经纪商的accountIndex。当前为：pcio
        self.followPicoAccountIndex = Account.getSpecialAccountIndex(headers = self.followHeaders, brokerID=riskControlData["testBrokerID"])[0]
        self.switchFollowAccount = Account.switchAccount(webAPIData['hostName'] + accountData['switchAccount'], self.followHeaders, index=self.followPicoAccountIndex)
        #账号切换成功
        self.assertEqual(self.switchFollowAccount.status_code, webAPIData['status_code_200'])
        #获取跟随者交易token
        self.followToken = Account.getToken(self.followHeaders, onlyTokn="true", printLogs=1)
        #一倍建立跟随
        self.tradeIndex = str(self.tradeUserID) + '_' + self.tradePicoAccountIndex
        
        print(self.tradeIndex)
        #设置跟随策略
        followDatas = {"accountIndex": self.followPicoAccountIndex, webAPIData['followStrategy']: webAPIData['follow_ratio'], 
        webAPIData['follow_setting']: 1, webAPIData['followDirection']: webAPIData['follow_positive']}
        createFollow = FollowManage.createFollow(webAPIData['hostName'] + followData['createFollow_url'] + self.tradeIndex, headers = self.followHeaders, datas =followDatas, interfaceName="createFollow")
        #断言跟随成功
        self.assertEqual(createFollow.status_code, webAPIData['status_code_200'])
        
    def test_stopFollowPeriods_currTime(self):
        '''当前时间点勾选时间保护设置，交易员下单。检查跟随者跟单情况(不能跟上)'''
        #设置针对单个交易员的风控参数。当前小时为时间保护，不交易
        currWeek = FMCommon.getCurrWeek()  #获取当前为周几
        currHour = FMCommon.getCurrHour()  #获取当前时间为几点
        specialTradeDatas = { "accountIndex": self.followPicoAccountIndex, webAPIData['stopFollowPeriods']:[{webAPIData["Weekday"]:currWeek, webAPIData["Hours"]:[currHour]}]}
        setRiskControlForTrader = RiskControl.setRiskControlForTrader(webAPIData['hostName'] + riskControlData['setRiskControlForTrader_url'] + self.tradeIndex, headers=self.followHeaders, datas=specialTradeDatas, interfaceName="setRiskControlForTrader")
        self.assertEqual(setRiskControlForTrader.status_code, webAPIData['status_code_200'])

        #下单时的手数为实际值除以100
        openParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_210'], tradeOnlineData['orderParam_symbol']: tradeOnlineData['broker_EURCAD'], tradeOnlineData['orderParam_volume']: 300 }
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.tradeToken}, openParam)
        #校验code等于0，为及时单开仓成功
        self.assertEqual(openPositionRes["code"], tradeOnlineData['ws_code_0'])
        #校验手数为下单时的手数为实际值除以100(300/100)
        self.assertEqual(openPositionRes["order"]["volume"], 300)
        #保存orderID,待开仓使用
        self.orderID = openPositionRes["order"]["order_id"]

        #获取跟随者订单信息
        followOrderParams = {webAPIData['orderStatus']:webAPIData['orderStatus_open']}
        getFollowOrder = Order.getOrders(webAPIData['hostName'] + orderData['getOrders_url'], headers=self.followHeaders, params=followOrderParams)
        #断言获取跟随订单成功
        self.assertEqual(getFollowOrder.status_code, webAPIData['status_code_200'])
        # #断言订单列表为空
        self.assertEqual(json.loads(getFollowOrder.text)['data']['items'], [])

        #平掉测试订单
        closeParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_211'], tradeOnlineData['orderParam_ticket']: self.orderID, tradeOnlineData['orderParam_volume']: 300 }
        closePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.tradeToken}, closeParam)
        #校验code等于0，为及时单平仓成功
        self.assertEqual(closePositionRes["code"], tradeOnlineData['ws_code_0'])
        #校验rcmd等于210，为及时单开仓
        self.assertEqual(closePositionRes["rcmd"], tradeOnlineData['ws_code_211'])
        #校验平掉的单号，为本测试及时单开仓的单号
        self.assertEqual(closePositionRes['order']["order_id"], self.orderID)

    def test_disableFollowPeriods_currTime(self):
        '''当前时间点清空时间保护设置，交易员下单。检查跟随者跟单情况(可以跟上)'''
        #设置针对单个交易员的风控参数。当前小时为时间保护，不交易
        currWeek = FMCommon.getCurrWeek()  #获取当前为周几
        currHour = FMCommon.getCurrHour()  #获取当前时间为几点
        specialTradeDatas = { "accountIndex": self.followPicoAccountIndex}
        setRiskControlForTrader = RiskControl.setRiskControlForTrader(webAPIData['hostName'] + riskControlData['setRiskControlForTrader_url'] + self.tradeIndex, headers=self.followHeaders, datas=specialTradeDatas, interfaceName="setRiskControlForTrader")
        self.assertEqual(setRiskControlForTrader.status_code, webAPIData['status_code_200'])

        #下单时的手数为实际值除以100
        openParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_210'], tradeOnlineData['orderParam_symbol']: tradeOnlineData['broker_EURCAD'], tradeOnlineData['orderParam_volume']: 300 }
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.tradeToken}, openParam)
        #校验code等于0，为及时单开仓成功
        self.assertEqual(openPositionRes["code"], tradeOnlineData['ws_code_0'])
        #校验手数为下单时的手数为实际值除以100(300/100)
        self.assertEqual(openPositionRes["order"]["volume"], 300)
        #保存orderID,待开仓使用
        self.orderID = openPositionRes["order"]["order_id"]

        #获取跟随者订单信息
        followOrderParams = {webAPIData['orderStatus']:webAPIData['orderStatus_open']}
        getFollowOrder = Order.getOrders(webAPIData['hostName'] + orderData['getOrders_url'], headers=self.followHeaders, params=followOrderParams)
        #断言获取跟随订单成功
        self.assertEqual(getFollowOrder.status_code, webAPIData['status_code_200'])
        #断言跟随者订单跟随的品种为：EURCAD
        self.assertEqual(json.loads(getFollowOrder.text)['data']['items'][0]['SYMBOL'], tradeOnlineData['broker_EURCAD'])
        #断言跟随者订单跟随的手数为：0.1手
        self.assertEqual(float(json.loads(getFollowOrder.text)['data']['items'][0]['VOLUME']), 3)

        #平掉测试订单
        closeParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_211'], tradeOnlineData['orderParam_ticket']: self.orderID, tradeOnlineData['orderParam_volume']: 300 }
        closePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.tradeToken}, closeParam)
        #校验code等于0，为及时单平仓成功
        self.assertEqual(closePositionRes["code"], tradeOnlineData['ws_code_0'])
        #校验rcmd等于210，为及时单开仓
        self.assertEqual(closePositionRes["rcmd"], tradeOnlineData['ws_code_211'])
        #校验平掉的单号，为本测试及时单开仓的单号
        self.assertEqual(closePositionRes['order']["order_id"], self.orderID)

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
        self.assertEqual(closePositionRes["code"], tradeOnlineData['ws_code_0'])

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
        self.assertEqual(closePositionRes["code"], tradeOnlineData['ws_code_0'])

        #还原风控参数
        #设置全局风控参数。关闭风控信号
        globalRiskControlData = {webAPIData['signalSwitch']: webAPIData['signalSwitch_open']}
        setRiskControl = RiskControl.setRiskControl(webAPIData['hostName'] + riskControlData['setRiskControl_url'], accountIndex=self.followPicoAccountIndex, headers = self.followHeaders, datas=globalRiskControlData)
        self.assertEqual(setRiskControl.status_code, webAPIData['status_code_200'])
        #设置针对单个交易员的风控参数。初始为默认值
        specialTradeDatas = { "accountIndex": self.followPicoAccountIndex}
        setRiskControlForTrader = RiskControl.setRiskControlForTrader(webAPIData['hostName'] + riskControlData['setRiskControlForTrader_url'] + self.tradeIndex, headers=self.followHeaders, datas=specialTradeDatas, interfaceName="setRiskControlForTrader")
        self.assertEqual(setRiskControlForTrader.status_code, webAPIData['status_code_200'])

        #取消跟随关系
        deleteFollow = FollowManage.deleteFollow(webAPIData['hostName'] + followData['deleteFollow_url'] + self.tradeIndex, headers = self.followHeaders, accountIndex=self.followPicoAccountIndex)
        self.assertEqual(deleteFollow.status_code, webAPIData['status_code_200'])

        #登出followme系统
        tradeSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.tradeHeaders)
        self.assertEqual(tradeSignout.status_code, webAPIData['status_code_200'])
        followSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.followHeaders)
        self.assertEqual(followSignout.status_code, webAPIData['status_code_200'])

if __name__ == '__main__':
    unittest.main()

