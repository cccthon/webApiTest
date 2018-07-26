# -*-coding:utf-8-*- 
#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getCommissions
# 用例标题: 获取交易员的跟随服务费核算列表（需要登录）
# 预置条件: 
# 测试步骤:
#   1. 跟随交易员下单3笔，平仓之后返佣12美金  2. 申请服务费    3. 申请服务费的金额变化  
#   4. 查看服务费申请记录   5. OA设置汇率  6. 获取OA审核金额  7.  获取0A今日汇率  
#   8. OA审核跟随服务费成功   9. OA支付跟随服务费  10. 支付跟随服务费之后金额会有变化
# 预期结果:
#   1.风控设置返回成功
#   2.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180508
#=========================================================
import sys,unittest,json,requests,time,datetime
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,Auth,RiskControl,Follow,FollowManage,TradeOnline,Account,Order,Social,Commissions
from socketIO_client import SocketIO
from base64 import b64encode

tradeOnlineData = FMCommon.loadTradeOnlineYML()
webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
riskControlData = FMCommon.loadRiskControlYML()
followData = FMCommon.loadFollowYML()
orderData = FMCommon.loadOrderYML()
accountData = FMCommon.loadAccountYML() 
commissionsData = FMCommon.loadCommissionsYML()
userData = FMCommon.loadWebAPIYML()
userDataAccountUrl=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()

class GetCommissions(unittest.TestCase):
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
        #获取指定经纪商的accountIndex。当前为：kvb
        self.tradePicoAccountIndex = Account.getSpecialAccountIndex(headers = self.tradeHeaders, brokerID=riskControlData["testBrokerID"])[0]
        print(self.tradePicoAccountIndex)
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
        #保存账号的nickName
        self.followNickName = json.loads(followSignin.text)['data']['nickname']
        # #保存登录时的token，待登出使用
        self.followUserToken = json.loads(followSignin.text)['data']['token']
        #规整headers
        self.followHeaders = dict(webAPIData['headers'], **{webAPIData['Authorization'] : webAPIData['Bearer'] + self.followUserToken})
        #获取指定经纪商的accountIndex。当前为：kvb
        self.followPicoAccountIndex = Account.getSpecialAccountIndex(headers = self.followHeaders,brokerID=riskControlData["testBrokerID"])[0]
        print(self.followPicoAccountIndex)
        self.switchFollowAccount = Account.switchAccount(webAPIData['hostName'] + accountData['switchAccount'], self.followHeaders, index=self.followPicoAccountIndex)
        print(self.switchFollowAccount.text)
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

        # OA登录
        getUserTokenRes = Auth.getUserToken(
            userData['hostNameSwagger'] + userDataAuthUrl['loginOA_url'] + userData['oaClientId']
            + "&userName=" + userData['oaUsername'] + "&password=" + userData['oapassword'],
            userData['headersOA'], interfaceName="getUserToken")

        self.assertEqual(getUserTokenRes.status_code, userData['status_code_200'])
        self.tokenOA = json.loads(getUserTokenRes.text)['accessToken']

        '''登录OA成功'''
        self.headerOA={'content-type': 'application/json', 'Accept' : 'application/json','Authorization': 'Bearer ' + str(self.tokenOA)}

        
    def test_1_getCommissions(self):
        '''账号持仓总手数设置为3，交易员买3手。验证跟随者跟随订单情况'''
        # 下单时的手数为实际值除以100(300/100)
        openParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_210'], tradeOnlineData['orderParam_symbol']: tradeOnlineData['broker_EURCAD'], tradeOnlineData['orderParam_volume']: 300 }
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.tradeToken}, openParam)
        #校验code等于0，为及时单开仓成功
        self.assertEqual(openPositionRes["code"], tradeOnlineData['ws_code_0'])
        #校验手数为下单时的手数为实际值除以100(300/100)
        self.assertEqual(openPositionRes["order"]["volume"], 300)
        #保存orderID,待开仓使用
        self.orderID = openPositionRes["order"]["order_id"]

        #获取订单的跟随订单
        getFollowOrdersOfOrder = Order.getFollowOrdersOfOrder(webAPIData['hostName'] + orderData['getFollowOrdersOfOrder_url1'], headers = self.tradeHeaders,params={"pageSize":100}, tradeOrderID = str(self.orderID))
        #断言获取跟随订单成功
        self.assertEqual(getFollowOrdersOfOrder.status_code, webAPIData['status_code_200'])
        #断言当前的测试用户有跟随订单
        nickNameOfOrderList = []
        for item in json.loads(getFollowOrdersOfOrder.text)["data"]["items"]:
            nickNameOfOrderList.append(item['CustomerNickName'])

            followOrder=item["TICKET"]
        self.assertIn(self.followNickName, nickNameOfOrderList,"当前测试用户未生成跟随订单")

        getFollowOrder = FollowManage.getFollowOrder(getFollowOrdersOfOrder, nickName=self.followNickName, accountIndex=self.followPicoAccountIndex)
        #断言跟随者订单跟随的品种为：EURCAD
        self.assertEqual(getFollowOrder['SYMBOL'], tradeOnlineData['broker_EURCAD'])
        #断言跟随者订单跟随的手数为：3手
        self.assertEqual(getFollowOrder['VOLUME'], 3)


        #平掉测试订单
        closeParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_211'], tradeOnlineData['orderParam_ticket']: self.orderID, tradeOnlineData['orderParam_volume']: 300 }
        closePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.tradeToken}, closeParam)
        #校验code等于0，为及时单平仓成功
        self.assertEqual(closePositionRes["code"], tradeOnlineData['ws_code_0'])
        #校验rcmd等于210，为及时单开仓
        self.assertEqual(closePositionRes["rcmd"], tradeOnlineData['ws_code_211'])
        #校验平掉的单号，为本测试及时单开仓的单号
        self.assertEqual(closePositionRes['order']["order_id"], self.orderID)

    
        #获取交易员的跟随服务费概览（需要登录），查看申请服务费之前的跟随服务费概览
        commissionSummary = Commissions.getCommissionSummary(webAPIData['hostName'] + commissionsData['getCommissionSummary_url'],self.tradeHeaders)
        self.assertEqual(commissionSummary.status_code, webAPIData['status_code_200'])
        applied =  json.loads(commissionSummary.text)["data"]["Applied"]
        balance =  json.loads(commissionSummary.text)["data"]["Balance"]
        daily =  json.loads(commissionSummary.text)["data"]["Daily"]
        followReturnAmount =  json.loads(commissionSummary.text)["data"]["FollowReturnAmount"]
        paidAmount =  json.loads(commissionSummary.text)["data"]["PaidAmount"]
        #申请超过30元的服务费
        applyCommission = Commissions.applyCommission(webAPIData['hostName'] + commissionsData['applyCommission_url'],self.tradeHeaders,datas={"amount":30})
        self.assertEqual(applyCommission.status_code, webAPIData['status_code_200'])
        commissionSummary = Commissions.getCommissionSummary(webAPIData['hostName'] + commissionsData['getCommissionSummary_url'],self.tradeHeaders)
        self.assertEqual(commissionSummary.status_code, webAPIData['status_code_200'])
        applied_1 =  json.loads(commissionSummary.text)["data"]["Applied"]
        balance_1 =  json.loads(commissionSummary.text)["data"]["Balance"]
        #获取跟随服务费,判断跟随服务费是否获取到
        getCommissions = Commissions.getCommissions(webAPIData['hostName'] + commissionsData['getCommissions_url'], self.tradeHeaders)
        #断言获取跟随订单成功
        self.assertEqual(getCommissions.status_code, webAPIData['status_code_200'])
        for i in json.loads(getCommissions.text)["data"]["items"]:
            if i["FollowerTicket"] == followOrder:
                self.assertEqual(12,i["FollowReturn"])
        daily_1 =  json.loads(commissionSummary.text)["data"]["Daily"]
        followReturnAmount_1 =  json.loads(commissionSummary.text)["data"]["FollowReturnAmount"]
        paidAmount_1 =  json.loads(commissionSummary.text)["data"]["PaidAmount"]
        #断言申请服务费之后申请中的金额会变化，其他数据金额不变
        self.assertEqual(applied + 30, applied_1)
        self.assertEqual(balance, balance_1)
        self.assertEqual(daily, daily_1)
        self.assertEqual(followReturnAmount, followReturnAmount_1)
        self.assertEqual(paidAmount, paidAmount_1)



    def test_2_applyCommission(self):
        #申请不超过超过30元的服务费
        applyCommission = Commissions.applyCommission(webAPIData['hostName'] + commissionsData['applyCommission_url'],self.tradeHeaders,datas={"amount":29})
        self.assertEqual(json.loads(applyCommission.text)["message"], "每次至少提取 $30!" )

    def test_3_getCommissionApplyHistories(self):       
        #查看服务费申请记录
        commissionApplyHistories = Commissions.getCommissionApplyHistories(webAPIData['hostName'] + commissionsData['getCommissionApplyHistories_url'],self.tradeHeaders)
        self.assertEqual(commissionApplyHistories.status_code, webAPIData['status_code_200'])
        applyDate = []
        for item in json.loads(commissionApplyHistories.text)["data"]["items"]:
            applyDate.append(item["ApplyDate"])
        # print(applyDate[0])
        # print(str)
        print ((applyDate[0].split(' '))[0])
        #通过断言申请时间来判断每申请一条新的服务费有生成新的申请记录
        self.assertEqual((applyDate[0].split(' '))[0], datetime.datetime.now().strftime("%Y-%m-%d"))

    def test_4_getCommissionApplyHistories(self):       
        #查看服务费申请记录
        commissionApplyHistories = Commissions.getCommissionApplyHistories(webAPIData['hostName'] + commissionsData['getCommissionApplyHistories_url'],self.tradeHeaders)
        self.assertEqual(commissionApplyHistories.status_code, webAPIData['status_code_200'])
        amount = []
        for item in json.loads(commissionApplyHistories.text)["data"]["items"]:
            amount.append(item["Amount"])
        #通过断言申请的服务费金额
        self.assertEqual(amount[0], 30)

    def test_5_TraderCommissionApplyList(self):
        #设置汇率为6.55
        addExchangeRate=Commissions.addExchangeRate(userData['hostNameOA']+commissionsData['addExchangeRate_url'],self.headerOA,datas= {'ExchangeRate': "6.55"},printLogs=0)

        #获取OA申请中的跟随服务费列表明细
        # datas={'pageIndex': 1,'pageSize': 10,'status':0}
        traderCommissionApplyList=Commissions.getTraderCommissionApplyList(userData['hostNameOA']+commissionsData['getTraderCommissionApplyList_url'],self.headerOA,datas= {'pageIndex': 1,'pageSize': 10,'status':0},printLogs=0)

        # traderCommissionApplyList = Commissions.getTraderCommissionApplyList(webAPIData['hostName'] + commissionsData['getCommissionApplyHistories_url'],self.tradeHeaders)
        self.assertEqual(traderCommissionApplyList.status_code, webAPIData['status_code_200'])
        applyDate = []
        ID = []
        for item in json.loads(traderCommissionApplyList.text)["Items"]:
            if item["UserID"] == 169193:
                applyDate.append(item["ApplyDate"])
                ID.append(item["ID"])
        print(applyDate[0])
        print(ID[0])
        # 通过断言申请时间来判断每申请一条新的服务费在OA有生成新的申请记录
        # self.assertEqual((applyDate[0].split(' '))[0], datetime.datetime.now().strftime("%Y-%m-%d"))

        #获取OA审核金额
        calcFee=Commissions.getCalcFee(userData['hostNameOA']+commissionsData['getCalcFee_url'],self.headerOA,params="account=30",printLogs=0)
        self.assertEqual(calcFee.status_code, webAPIData['status_code_200'])

        #获取OA今日汇率
        todayExchangeRate=Commissions.getTodayExchangeRate(userData['hostNameOA']+commissionsData['getTodayExchangeRate_url'],self.headerOA,printLogs=0)
        self.assertEqual(todayExchangeRate.status_code, webAPIData['status_code_200'])


        #OA审核跟随服务费成功
        datas={'status': 1,"Amount":30,"UserID":169193, 'auditMoney': "30", 'remark': "",'exchangeRate':6.55, 'applyID': ID[0], 'traderID': "2100004852", 'traderBrokerID': "1"}

        commApplySubmit=Commissions.commApplySubmit(userData['hostNameOA']+commissionsData['commApplySubmit_url'],self.headerOA,datas,printLogs=0)

    def test_6_TraderCommissionApplyList(self):
        #获取交易员的跟随服务费概览（需要登录）
        commissionSummary = Commissions.getCommissionSummary(webAPIData['hostName'] + commissionsData['getCommissionSummary_url'],self.tradeHeaders)
        self.assertEqual(commissionSummary.status_code, webAPIData['status_code_200'])
        applied =  json.loads(commissionSummary.text)["data"]["Applied"]
        balance =  json.loads(commissionSummary.text)["data"]["Balance"]
        daily =  json.loads(commissionSummary.text)["data"]["Daily"]
        followReturnAmount =  json.loads(commissionSummary.text)["data"]["FollowReturnAmount"]
        paidAmount =  json.loads(commissionSummary.text)["data"]["PaidAmount"]
        print(applied)
        print(followReturnAmount)
        #获取OA审核通过(status:1)的订单列表
        traderCommissionApplyList=Commissions.getTraderCommissionApplyList(userData['hostNameOA']+commissionsData['getTraderCommissionApplyList_url'],self.headerOA,datas= {'pageIndex': 1,'pageSize': 10,'status':1},printLogs=0)
        self.assertEqual(traderCommissionApplyList.status_code, webAPIData['status_code_200'])
        applyDate = []
        ID = []
        for item in json.loads(traderCommissionApplyList.text)["Items"]:
            if item["UserID"] == 169193:
                applyDate.append(item["ApplyDate"])
                ID.append(item["ID"])
        print(applyDate[0])
        print(ID[0])

        #获取OA今日汇率
        todayExchangeRate=Commissions.getTodayExchangeRate(userData['hostNameOA']+commissionsData['getTodayExchangeRate_url'],self.headerOA,printLogs=0)
        self.assertEqual(todayExchangeRate.status_code, webAPIData['status_code_200'])

        #OA支付跟随服务费
        datas={'status': 2,"Amount":30,"UserID":169193, 'auditMoney': 30, 'realPay':20, 'remark': "", 'applyID': ID[0], 'traderID': "2100004852", 'traderBrokerID': "1"}
        traderCommissionApplyList=Commissions.commPlaymoneyApplySubmit(userData['hostNameOA']+commissionsData['commPlaymoneyApplySubmit_url'],self.headerOA,datas,printLogs=0)
        self.assertEqual(traderCommissionApplyList.status_code, webAPIData['status_code_200'])
        #重新获取交易员的跟随服务费概览（需要登录），支付跟随服务费之后金额会有变化
        commissionSummary = Commissions.getCommissionSummary(webAPIData['hostName'] + commissionsData['getCommissionSummary_url'],self.tradeHeaders)
        self.assertEqual(commissionSummary.status_code, webAPIData['status_code_200'])
        applied_1 =  json.loads(commissionSummary.text)["data"]["Applied"]
        balance_1 =  json.loads(commissionSummary.text)["data"]["Balance"]
        daily_1 =  json.loads(commissionSummary.text)["data"]["Daily"]
        followReturnAmount_1 =  json.loads(commissionSummary.text)["data"]["FollowReturnAmount"]
        paidAmount_1 =  json.loads(commissionSummary.text)["data"]["PaidAmount"]
        #断言打款之后服务费余额会减少
        self.assertEqual(balance_1, balance -30 )
        #断言打款之后申请中的服务费会减少
        self.assertEqual(applied_1, applied - 30)
        #断言打款之后已打款金额会增多
        self.assertEqual(paidAmount_1, paidAmount + 30)

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

        # 取消跟随关系
        deleteFollow = FollowManage.deleteFollow(webAPIData['hostName'] + followData['deleteFollow_url'] + self.tradeIndex, headers = self.followHeaders, accountIndex=self.tradePicoAccountIndex)
        self.assertEqual(deleteFollow.status_code, webAPIData['status_code_200'])

        #登出followme系统
        tradeSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.tradeHeaders)
        self.assertEqual(tradeSignout.status_code, webAPIData['status_code_200'])
        followSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.followHeaders)
        self.assertEqual(followSignout.status_code, webAPIData['status_code_200'])

if __name__ == '__main__':
    unittest.main()

