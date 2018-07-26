# -*- coding:utf-8 -*
import requests,json,gc,sys,yaml,time,datetime,redis,random
import unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,Auth,MAM,Trade,Account
import TradeOnline

userData = FMCommon.loadWebAPIYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()
userDataMam=FMCommon.loadMamYML()
userDataAuth=FMCommon.loadAuthYML()
userDataSocial=FMCommon.loadSocialYML()
userDataAccount=FMCommon.loadAccountYML()

class CreateProduct(unittest.TestCase):
    def setUp(self):
        # 交易员登录
        datas = {"account": "18198995508", "password": "123456", "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.traderToken = json.loads(traderLoginRes.text)['data']['token']
        self.traderUserId = json.loads(traderLoginRes.text)['data']['id']
        self.traderNickName = str(json.loads(traderLoginRes.text)['data']['nickname'])

        # OA登录
        clientId = "oa"
        userName = "mqwtkn69074@chacuo.net"
        password = "123456"
        getUserTokenRES = Auth.getUserToken(userData['hostNameSwagger'] + userDataAuth[
            'getUserToken_url'] + clientId + "&userName=" + userName + "&password=" + password,
                                            userData['headersOA'], interfaceName="getUserToken")
        self.assertEqual(getUserTokenRES.status_code, userData['status_code_200'])
        self.tokenOA = json.loads(getUserTokenRES.text)['accessToken']

        # 跟随者登录
        datas = {"account": "18198995507", "password": "123456", "remember": "false"}
        loginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(loginRes.status_code, userData['status_code_200'])
        self.token = json.loads(loginRes.text)['data']['token']

    def test_CreateProductToEndProduct(self):
        '''场景步骤：1，交易员登录2，交易员创建产品并验证产品信息3，登录OA4，OA审核产品通过5，获取产品信息,并验证产品状态6，跟随者登录
        7，跟随者参与产品（2个跟随者）8，OA修改产品开始时间 9，交易员开仓10，交易员平仓11，OA结束产品12，获取交易员的订单列表，验证交易员
        的收益和盈亏点数13，获取跟随者的订单列表，验证跟随者的收益和盈亏点数14，验证产品状态为已结束15，验证产品的结算数据16，退出登录 '''
        # 获取今天
        today = datetime.date.today()

        # 获取3天后转为时间戳
        tomorrow = today + datetime.timedelta(days=3)
        timeArray_tomorrow = time.strptime(str(tomorrow), "%Y-%m-%d")
        timeStamp_tomorrow = int(time.mktime(timeArray_tomorrow))

        # 获得6天后转为时间戳
        after_tomorrow = today + datetime.timedelta(days=6)
        timeArray_after_tomorrow = time.strptime(str(after_tomorrow), "%Y-%m-%d")
        timeStamp_after_tomorrow = int(time.mktime(timeArray_after_tomorrow))

        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.traderToken

        self.followHeaders = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})

        # 获取交易员的accountindex
        self.tradekvbminiAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=6, accountType=3)

        # 获取跟随者的accountindex
        self.followerkvbminiAccountIndex = Account.getSpecialAccountIndex(headers=self.followHeaders, brokerID=6, accountType=3)

        #交易员创建产品
        datas = {"accountIndex": self.tradekvbminiAccountIndex[0],
                "name":"testCI"+str(int(time.time())),
                "description": "testmamonci",
                "profitModeID":1,
                "retreatModeID":2,
                "expectROI":0.3,
                "expectFollowerCount":2,
                "expectDays":1,
                "expectStartTime": timeStamp_tomorrow,
                "expectEndTime": timeStamp_after_tomorrow,
                "isShowHistoryOrder": True,
                "signature": "test"}

        CreateProductRes = MAM.createProduct(userData['hostName']+userDataMam['createProduct_url'],userData['headers'],
                                             datas)

        self.assertEqual(CreateProductRes.status_code, userData['status_code_200'])
        #返回产品ID
        self.product_id = json.loads(CreateProductRes.text)['data']['ID']
        #返回创建人的UserID
        self.createrUserId = int(json.loads(CreateProductRes.text)['data']['Trader']['UserID'])
        # 返回产品Name
        self.product_name = json.loads(CreateProductRes.text)['data']['Name']


        self.headerOA = {'content-type': 'application/json', 'Accept': 'application/json','Authorization': 'Bearer ' + str(self.tokenOA)}

        #查询产品自增长ID
        select_id_sql = 'SELECT id from t_product_propose WHERE product_id='+str(self.product_id)
        idRES = FMCommon.mysql_operater(userData['beta_mysql_host'],userData['beta_mysql_port'],userData['beta_mysql_db'],
                                        userData['beta_mysql_user'],userData['beta_mysql_passwd'],select_id_sql)
        for mtuple in idRES:
            for item in mtuple:
                id = item
        time.sleep(10)

        #OA审核产品通过
        ProductProposeActiondatas ={"Action": 0,
                                    "ProductProposeID": id,
                                    "DeclineReason": "",
                                    "ProposerUserID": self.createrUserId}
        ProductProposeActionRes = MAM.ProductProposeAction(userData['hostNameOA'] + userDataMam['ProductProposeAction_url'],
                                                           self.headerOA, ProductProposeActiondatas)

        self.assertEqual(ProductProposeActionRes.status_code, userData['status_code_200'])
        time.sleep(5)

        #获取产品信息
        GetProductRES = MAM.GetProduct(userData['hostName'] + userDataMam['getProduct_url']+str(self.product_id), userData['headers'])

        self.assertEqual(GetProductRES.status_code, userData['status_code_200'])

        #验证产品状态为"发布中"
        self.product_status = json.loads(GetProductRES.text)['data']['Status']
        self.assertEqual(self.product_status, "Pending")

        #跟随者参与产品(第一个跟随者)
        datas={"accountIndex": self.followerkvbminiAccountIndex[0], "signature": "test1"}
        joinProductRES =MAM.JoinProduct(userData['hostName']+userDataMam['joinProduct_url']+str(self.product_id) +
                                        userDataMam['joinProduct_join_url'],self.followHeaders, datas)

        self.assertEqual(joinProductRES.status_code, userData['status_code_200'])

        #跟随者参与产品(第二个跟随者)
        datas = {"accountIndex": self.followerkvbminiAccountIndex[1], "signature": "test2"}
        joinProductRES = MAM.JoinProduct(userData['hostName'] + userDataMam['joinProduct_url'] + str(self.product_id) +
                                         userDataMam['joinProduct_join_url'], self.followHeaders, datas)

        self.assertEqual(joinProductRES.status_code, userData['status_code_200'])
        time.sleep(5)

        # 获取一分钟后
        TimeNowAfterOneMinute = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")

        # 切换到交易员账户
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 userData['headers'], self.tradekvbminiAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])

        # 获取交易token
        getTokenRes = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], userData['headers'])
        self.assertEqual(getTokenRes.status_code, userData['status_code_200'])
        tradeToken = str(json.loads(getTokenRes.content)["data"]["Token"]).replace("=", "@")
        traderMT4Account = str(json.loads(getTokenRes.content)["data"]["MT4Account"])


        # 人数达标后，修改产品开始时间
        updatePendingProductdatas={
            "Account": self.traderNickName +traderMT4Account + "#" +self.tradekvbminiAccountIndex[0],
            "Description": "testmamonci",
            "ExpectDays": 1,
            "ExpectFollowerCount": 2,
            "ExpectROI": 0.3,
            "ExpectStartTime": TimeNowAfterOneMinute,
            "IsShowHistoryOrder": True,
            "Mt4Account": traderMT4Account,
            "Name": self.product_name,
            "ProductID": self.product_id,
            "Productstatus": "1",
            "ProfitModeID": 1,
            "RetreatModeID": 2}
        updatePendingProductRES = MAM.updatePendingProduct(userData['hostNameOA'] + userDataMam['UpdatePendingProduct_url'],
                                                           self.headerOA,updatePendingProductdatas)

        self.assertEqual(updatePendingProductRES.status_code, userData['status_code_200'])

        time.sleep(100)
        openOrderList = []
        count = 0
        while count < 3:
            #交易员开仓
            openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                         userDataWebSocket['orderParam_symbol']: "AUDCAD",
                         userDataWebSocket['orderParam_volume']: 1}
            openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(
                self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken}, openParam)
            self.assertEqual(openPositionRes["code"], userDataWebSocket['ws_code_0'])
            self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
            self.orderID = openPositionRes["order"]["order_id"]
            openOrderList.append(self.orderID)
            count = count + 1

        time.sleep(15)
        # 批量平仓10张
        closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_219'],
                      userDataWebSocket['orderParam_tickets']: openOrderList}
        closeOrderRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],userDataWebSocket['ws_port'],
                                                                {'token': "" + tradeToken}, closeOrder)
        self.assertEqual(closeOrderRes["code"], userDataWebSocket['ws_code_0'])
        self.assertEqual(closeOrderRes["rcmd"], userDataWebSocket['ws_code_219'])
        time.sleep(15)

        #在OA里结束产品
        ProductEnddatas={
                "ProductID": self.product_id,
                "Name": self.product_name,
                "Account": self.traderNickName + traderMT4Account + "#" + self.tradekvbminiAccountIndex[0],
                "Mt4Account": traderMT4Account,
                "BrokerID": 6,
                "Productstatus": 2,
                "Remark": "end"
            }
        productEndOARES = MAM.productEndOA(userData['hostNameOA'] + userDataMam['ProductEnd_url'],
                                           self.headerOA, ProductEnddatas)

        self.assertEqual(productEndOARES.status_code, userData['status_code_200'])
        time.sleep(3)

        #获取产品的交易员的订单列表
        getTraderProductOrdersRES = MAM.getProductOrders(userData['hostName'] + userDataMam['getProductOrders_url'] +
                                                         str(self.product_id) + userDataMam['getProductOrders_orders_url']+
                                                         "?my=" + "false",userData['headers'])
        #获取交易员的收益和盈亏点数

        self.assertEqual(getTraderProductOrdersRES.status_code, userData['status_code_200'])
        self.traderProfit = json.loads(getTraderProductOrdersRES.text)['data']['summary']['Profit']
        self.traderPips = json.loads(getTraderProductOrdersRES.text)['data']['summary']['Pips']

        #切换到第一个跟随者，获取跟随者收益
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 self.followHeaders, self.followerkvbminiAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])
        getFollowerProductOrdersRES = MAM.getProductOrders(userData['hostName'] + userDataMam['getProductOrders_url'] +
                                                           str(self.product_id) + userDataMam['getProductOrders_orders_url']+
                                                           "?my=" + "true",self.followHeaders)

        self.assertEqual(getFollowerProductOrdersRES.status_code, userData['status_code_200'])
        self.followerProfit_first = json.loads(getFollowerProductOrdersRES.text)['data']['summary']['Profit']
        self.followerPips_first = json.loads(getFollowerProductOrdersRES.text)['data']['summary']['Pips']

        #切换到第二个跟随者，获取跟随者的收益
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 self.followHeaders, self.followerkvbminiAccountIndex[1])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])
        getFollowerProductOrdersRES = MAM.getProductOrders(userData['hostName'] + userDataMam['getProductOrders_url'] +
                                                           str(self.product_id) + userDataMam['getProductOrders_orders_url']+
                                                           "?my=" + "true",self.followHeaders)

        self.assertEqual(getFollowerProductOrdersRES.status_code, userData['status_code_200'])
        self.followerProfit_second = json.loads(getFollowerProductOrdersRES.text)['data']['summary']['Profit']
        self.followerPips_second = json.loads(getFollowerProductOrdersRES.text)['data']['summary']['Pips']

        #如果是亏损的，交易员百分百赔付跟随者
        if self.followerProfit_first<=0:
            self.traderProfit = self.traderProfit + self.followerProfit_first
            self.followerProfit_first=0

        if self.followerProfit_second<=0:
            self.traderProfit = self.traderProfit + self.followerProfit_second
            self.followerProfit_second=0

        #如果是盈利，交易员二八分成
        if self.followerProfit_first > 0:
            self.traderProfit = self.traderProfit + self.followerProfit_first*0.8
            self.followerProfit_first = self.followerProfit_first*0.2

        if self.followerProfit_second > 0:
            self.traderProfit = self.traderProfit + self.followerProfit_second*0.8
            self.followerProfit_second = self.followerProfit_second * 0.2

        #验证产品状态为已结束getProduct,并验证产品的结算数据
        GetProductRES = MAM.GetProduct(userData['hostName'] + userDataMam['getProduct_url'] + str(self.product_id),
                                       userData['headers'])

        self.assertEqual(GetProductRES.status_code, userData['status_code_200'])
        # 验证产品状态为"已结束"
        self.product_status = json.loads(GetProductRES.text)['data']['Status']
        self.assertEqual(self.product_status, "Settled")
        # 验证参与人数
        self.assertEqual(json.loads(GetProductRES.text)['data']['FollowerCount'], 2)
        # 验证发起产品人的身份
        self.assertEqual(json.loads(GetProductRES.text)['data']['Trader']['Type'], "Trader")
        # 验证发起产品人的用户ID
        self.assertEqual(json.loads(GetProductRES.text)['data']['Trader']['UserID'], self.createrUserId)
        # 验证发起产品人的AccountIndex
        self.assertEqual(str(json.loads(GetProductRES.text)['data']['Trader']['AccountIndex']), self.tradekvbminiAccountIndex[0])
        # 验证发起产品人的经纪商ID
        self.assertEqual(json.loads(GetProductRES.text)['data']['Trader']['BrokerID'], 6)
        # 验证交易员的分成收益
        self.assertAlmostEqual(json.loads(GetProductRES.text)['data']['MyProfit'], self.traderProfit, delta=100)
        # 验证跟随者的分成收益
        self.assertAlmostEqual(json.loads(GetProductRES.text)['data']['FollowerProfit'], self.followerProfit_first,
                               delta=100)
        self.assertAlmostEqual(json.loads(GetProductRES.text)['data']['FollowerProfit'],self.followerProfit_second ,
                               delta=100)

    def tearDown(self):
        #退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.traderToken
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(CreateProduct))
    unittest.TextTestRunner(verbosity=2).run(suite)