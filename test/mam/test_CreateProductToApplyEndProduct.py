# -*- coding:utf-8 -*
import requests,json,gc,sys,yaml,time,datetime,redis
import unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,TradeOnline,Auth,MAM

userData = FMCommon.loadWebAPIYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()
userDataMam=FMCommon.loadMamYML()
userDataAuth=FMCommon.loadAuthYML()
userDataSocial=FMCommon.loadSocialYML()

class CreateProduct(unittest.TestCase):
    def setUp(self):
        # 交易员登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.traderToken = json.loads(traderLoginRes.text)['data']['token']
        self.traderUserId = json.loads(traderLoginRes.text)['data']['id']

        # OA登录
        loginOARes = Auth.loginOA(userData['hostNameOA']+userDataAuth['loginOA_url'], userData['headersOA'],
                                  userData["usernameOA"],userData["passwordOA"],printLogs=1)
        self.assertEqual(loginOARes.status_code, userData['status_code_200'])
        self.tokenOA = json.loads(loginOARes.text)['Result']['Token']

        # 跟随者登录
        datas = {"account": userData['wfollowAccount'], "password": userData['wfollowpasswd'], "remember": "false"}
        loginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(loginRes.status_code, userData['status_code_200'])
        self.token = json.loads(loginRes.text)['data']['token']

    def test_CreateProductToEndProduct(self):
        '''场景步骤：1，交易员登录2，交易员创建产品并验证产品信息3，登录OA4，OA审核产品通过5，获取产品信息,并验证产品状态6，跟随者登录7，跟随者参与产品（2个跟随者）
        8，OA修改产品开始时间 9，交易员开仓10，交易员平仓11，申请提前结束产品前查看产品状态的，验证是否还有持仓单12，获取短信验证码（申请提前结束产品）
        13，校验短信验证码（申请提前结束产品）14，提交申请提前结束产品15，OA产品提前终止申请通过16，获取交易员的订单列表，验证交易员的收益和盈亏点数
        17，获取跟随者的订单列表，验证跟随者的收益和盈亏点数18，验证产品状态为已结束19，验证产品的结算数据20，退出登录 '''
        # # 获取今天
        # today = datetime.date.today()
        #
        # # 获取明天转为时间戳
        # tomorrow = today + datetime.timedelta(days=3)
        # timeArray_tomorrow = time.strptime(str(tomorrow), "%Y-%m-%d")
        # timeStamp_tomorrow = int(time.mktime(timeArray_tomorrow))
        #
        # # 获得后天转为时间戳
        # after_tomorrow = today + datetime.timedelta(days=6)
        # timeArray_after_tomorrow = time.strptime(str(after_tomorrow), "%Y-%m-%d")
        # timeStamp_after_tomorrow = int(time.mktime(timeArray_after_tomorrow))
        #
        # #交易员创建产品
        # datas = {"accountIndex":5,
        #         "name":"testCI",
        #         "description": "descriptionCI",
        #         "profitModeID":1,
        #         "retreatModeID":2,
        #         "expectROI":0.3,
        #         "expectFollowerCount":2,
        #         "expectDays":1,
        #         "expectStartTime": timeStamp_tomorrow,
        #         "expectEndTime": timeStamp_after_tomorrow,
        #         "isShowHistoryOrder": True,
        #         "signature": "test"}
        # userData['headers'][userData['Authorization']] = userData['Bearer'] + self.traderToken
        # CreateProductRes = MAM.createProduct(userData['hostName']+userDataMam['createProduct_url'],userData['headers'],
        #                                      datas)
        # FMCommon.printLog('CreateProductRes: ' + CreateProductRes.text)
        # self.assertEqual(CreateProductRes.status_code, userData['status_code_200'])
        # #返回产品ID
        # self.product_id = json.loads(CreateProductRes.text)['data']['ID']
        # #返回创建人的UserID
        # self.createrUserId = int(json.loads(CreateProductRes.text)['data']['Trader']['UserID'])
        #
        # self.headerOA = {'content-type': 'application/json', 'Accept': 'application/json','Authorization': 'Bearer ' + str(self.tokenOA)}
        #
        # #查询产品自增长ID
        # select_id_sql = 'SELECT id from t_product_propose WHERE product_id='+str(self.product_id)
        # idRES = FMCommon.mysql_operater(userData['beta_mysql_host'],userData['beta_mysql_port'],userData['beta_mysql_db'],
        #                                 userData['beta_mysql_user'],userData['beta_mysql_passwd'],select_id_sql)
        # for mtuple in idRES:
        #     for item in mtuple:
        #         id = item
        # time.sleep(5)
        #
        # #OA审核产品通过
        # ProductProposeActiondatas ={"Action": 0,
        #                             "ProductProposeID": id,
        #                             "DeclineReason": "",
        #                             "ProposerUserID": self.createrUserId}
        # ProductProposeActionRes = MAM.ProductProposeAction(userData['hostNameOA'] + userDataMam['ProductProposeAction_url'],
        #                                                    self.headerOA, ProductProposeActiondatas)
        # FMCommon.printLog('ProductProposeActionRes: ' ,ProductProposeActionRes.text)
        # self.assertEqual(ProductProposeActionRes.status_code, userData['status_code_200'])
        #
        # time.sleep(5)
        #
        # #获取产品信息
        # GetProductRES = MAM.GetProduct(userData['hostName'] + userDataMam['getProduct_url']+str(self.product_id), userData['headers'])
        # FMCommon.printLog('GetProductRES: ', GetProductRES.text)
        # self.assertEqual(GetProductRES.status_code, userData['status_code_200'])
        #
        # #验证产品状态为"发布中"
        # self.product_status = json.loads(GetProductRES.text)['data']['Status']
        # self.assertEqual(self.product_status, "Pending")

        #
        # #跟随者参与产品(第一个跟随者)
        # datas={"accountIndex": 5, "signature": "test1"}
        # self.followHeaders = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})
        # joinProductRES =MAM.JoinProduct(userData['hostName']+userDataMam['joinProduct_url']+str(self.product_id) +
        #                                 userDataMam['joinProduct_join_url'],self.followHeaders, datas)
        # FMCommon.printLog('joinProductRES: ', joinProductRES.text)
        # self.assertEqual(joinProductRES.status_code, userData['status_code_200'])
        #
        # #跟随者参与产品(第二个跟随者)
        # datas = {"accountIndex": 6, "signature": "test2"}
        # self.followHeaders = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})
        # joinProductRES = MAM.JoinProduct(userData['hostName'] + userDataMam['joinProduct_url'] + str(self.product_id) +
        #                                  userDataMam['joinProduct_join_url'], self.followHeaders, datas)
        # FMCommon.printLog('joinProductRES: ', joinProductRES.text)
        # self.assertEqual(joinProductRES.status_code, userData['status_code_200'])

        #获取当前时间后一分钟的时间戳
        TimeNowAfterOneMinute = (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        print(TimeNowAfterOneMinute)
        timeArray_TimeNowAfterOneMinute = time.strptime(str(TimeNowAfterOneMinute), "%Y-%m-%d %H:%M:%S")
        timeStamp_TimeNowAfterOneMinute = int(time.mktime(timeArray_TimeNowAfterOneMinute))
        print(timeStamp_TimeNowAfterOneMinute)

        #获取当前时间一天后的时间戳
        TimeNowAfterOneDay = (datetime.datetime.now() + datetime.timedelta(minutes=1440)).strftime("%Y-%m-%d %H:%M:%S")
        print(TimeNowAfterOneDay)
        timeArray_TimeNowAfterOneDay = time.strptime(str(TimeNowAfterOneDay), "%Y-%m-%d %H:%M:%S")
        timeStamp_TimeNowAfterOneDay = int(time.mktime(timeArray_TimeNowAfterOneDay))
        print(timeStamp_TimeNowAfterOneDay)

        # #人数达标后，修改产品开始时间
        # updatePendingProductdatas={
        #       "MinFollowBalance": 100000.0,
        #       "ExpectROI": 0.3,
        #       "MaxRetreatRatio": 0.15,
        #       "StopOutRatio": 0.15,
        #       "ProfitModeID": 1,
        #       "RetreatModeID": 2,
        #       "ExpectFollowerCount": 2,
        #       "ExpectStartTime": timeStamp_TimeNowAfterOneMinute,
        #       "ExpectEndTime": timeStamp_TimeNowAfterOneDay,
        #       "ExpectDays": 1,
        #       "IsShowHistoryOrder": True,
        #       "Description": "update startTime",
        #       "ProductID": self.product_id,
        #       "Name": "testCI",
        #       "Account": "FMCITS012 2100002036 #5",
        #       "Mt4Account": "2100002036",
        #       "BrokerID": 1,
        #       "Productstatus": 1,
        #       "Remark": "update product startTime"}
        # updatePendingProductRES = MAM.updatePendingProduct(userData['hostNameOA'] + userDataMam['UpdatePendingProduct_url'],
        #                                                    self.headerOA,updatePendingProductdatas)
        # FMCommon.printLog('updatePendingProductRES: ', updatePendingProductRES.text)
        # self.assertEqual(updatePendingProductRES.status_code, userData['status_code_200'])

        time.sleep(2)
        # #交易员开仓
        # openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
        #              userDataWebSocket['orderParam_symbol']: userDataWebSocket['broker_EURCAD'],
        #              userDataWebSocket['orderParam_volume']: userDataWebSocket['broker_volume']}
        # openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(
        #     self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + self.traderToken}, openParam)
        # self.assertEqual(openPositionRes["code"], userDataWebSocket['ws_code_0'])
        # self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
        # self.assertEqual(openPositionRes["order"]["volume"], userDataWebSocket['broker_volume'])
        # self.orderID = openPositionRes["order"]["order_id"]
        #
        # #交易员平仓
        # closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_211'],
        #               userDataWebSocket['orderParam_ticket']: self.orderID,
        #               userDataWebSocket['orderParam_volume']: userDataWebSocket['broker_volume']}
        # closeOrderRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
        #                                                         userDataWebSocket['ws_port'],
        #                                                         {'token': "" + self.tradeToken}, closeOrder)
        # self.assertEqual(closeOrderRes["code"], userDataWebSocket['ws_code_0'])
        # self.assertEqual(closeOrderRes["rcmd"], userDataWebSocket['ws_code_211'])
        # self.assertEqual(closeOrderRes['order']["order_id"], self.orderID)
        # self.assertEqual(closeOrderRes["order"]["volume"], userDataWebSocket['broker_volume'])
        #
        # #申请提前结束产品前查看产品状态的，是否还有持仓单
        # getProductStatusRES = MAM.GetProductStatus(userData['hostName'] + userDataMam['getProductStatus_url'] + self.product_id +
        #                                            userDataMam["getProductStatus_status_url"], userData['headers'])
        # FMCommon.printLog("getProductStatusRES:", getProductStatusRES.text)
        # self.assertEqual(getProductStatusRES.status_code, userData['status_code_200'])
        #
        # #获取短信验证码
        # datas={"mobile": "13751151018"}
        # endProductSMSCodeRES = MAM.endProductSMSCode(userData['hostName']+userDataMam["endProductSMSCode_url"],
        #                                              userData['headers'],datas)
        # FMCommon.printLog("endProductSMSCodeRES:", endProductSMSCodeRES.text)
        # self.assertEqual(endProductSMSCodeRES.status_code, userData['status_code_200'])
        # #从redis中获取验证码
        # self.readRedis = redis.Redis(host='192.168.8.6', port=7002, db=0, password='myredis')
        # #从redis读取短信验证码
        # self.mySmsCode=self.readRedis.get('MAM:SMSCODE:13751151018')
        #
        # #校验短信验证码（申请提前结束产品）
        # datas={"mobile": "13751151018", "code": self.mySmsCode}
        # endProductSMSCodeVerifyRES = MAM.endProductSMSCodeVerify(userData['hostName']+userDataMam["endProductSMSCodeVerify_url"],
        #                                              userData['headers'], datas)
        # FMCommon.printLog("endProductSMSCodeVerifyRES:", endProductSMSCodeVerifyRES.text)
        # self.assertEqual(endProductSMSCodeVerifyRES.status_code, userData['status_code_200'])
        #
        # #申请提前结束产品endProduct
        # datas={"mobile": "13751151018","code": self.mySmsCode,"remark": "test"}
        # EndProductRES = MAM.EndProduct(userData['hostName'] + userDataMam['endProduct_url'] + self.product_id +
        #                                userDataMam["endProduct_end_url"], userData['headers'], datas)
        # FMCommon.printLog("EndProductRES:", EndProductRES.text)
        # self.assertEqual(EndProductRES.status_code, userData['status_code_200'])
        #
        # #OA产品提前终止申请通过
        # select_endid_sql = 'SELECT id from t_product_propose WHERE product_id="+self.product_id +" and type=2'
        # endidRES = FMCommon.mysql_operater(userData['host'], userData['port'], userData['db'], userData['user'],
        #                                 userData['passwd'], select_endid_sql)
        # print("endidRES:", idRES[0][0])
        # ProductProposeActiondatas = {"Action": 0,
        #                             "ProductProposeID": endidRES[0][0],
        #                             "DeclineReason": "",
        #                             "ProposerUserID": 148235}
        # ProductProposeActionRes = MAM.ProductProposeAction(userData['hostNameOA'] + userDataMam['ProductProposeAction_url'],
        #                                                    self.headerOA, ProductProposeActiondatas)
        # FMCommon.printLog('ProductProposeActionRes: ' ,ProductProposeActionRes.text)
        # self.assertEqual(ProductProposeActionRes.status_code, userData['status_code_200'])
        #
        # #获取产品的交易员的订单列表
        # getTraderProductOrdersRES = MAM.getProductOrders(userData['hostName'] + userDataMam['getProductOrders_url'] + self.product_id
        #                                            + userDataMam['getProductOrders_orders_url'],userData['headers'])
        # #获取交易员的收益和盈亏点数
        # FMCommon.printLog('getProductOrdersRES: ', getTraderProductOrdersRES.text)
        # self.assertEqual(getTraderProductOrdersRES.status_code, userData['status_code_200'])
        # self.traderProfit=json.loads(getTraderProductOrdersRES.text)['data']['items']['Profit']
        # self.traderPips=json.loads(getTraderProductOrdersRES.text)['data']['items']['Pips']
        #
        # #获取产品的跟随者的订单列表
        # getFollowerProductOrdersRES = MAM.getProductOrders(userData['hostName'] + userDataMam['getProductOrders_url'] + self.product_id
        #     + userDataMam['getProductOrders_orders_url'], self.followHeaders)
        # FMCommon.printLog('getProductOrdersRES: ', getFollowerProductOrdersRES.text)
        # self.assertEqual(getFollowerProductOrdersRES.status_code, userData['status_code_200'])
        # self.followerProfit = json.loads(getFollowerProductOrdersRES.text)['data']['items']['Profit']
        # self.followerPips = json.loads(getFollowerProductOrdersRES.text)['data']['items']['Pips']
        #
        # #验证产品状态为已结束getProduct,并验证产品的结算数据
        # # 获取产品信息，状态为“发布中”
        # GetProductRES = MAM.GetProduct(userData['hostName'] + userDataMam['getProduct_url'] + self.product_id,
        #                                userData['headers'])
        # FMCommon.printLog('GetProductRES: ', GetProductRES.text)
        # self.assertEqual(GetProductRES.status_code, userData['status_code_200'])
        # # 验证产品状态为"已结束"
        # self.product_status = json.loads(GetProductRES.text)['data']['items']['Status']
        # self.assertEqual(self.product_status, "Finished")
        # # 验证参与人数
        # self.assertEqual(json.loads(GetProductRES.text)['data']['FollowerCount'], 2)
        # # 验证发起产品人的身份
        # self.assertEqual(json.loads(GetProductRES.text)['data']['items']['Trader']['Type'], "Trader")
        # # 验证发起产品人的用户ID
        # self.assertEqual(json.loads(GetProductRES.text)['data']['items']['Trader']['UserID'], self.createrUserId)
        # # 验证发起产品人的AccountIndex
        # self.assertEqual(json.loads(GetProductRES.text)['data']['items']['Trader']['AccountIndex'], 5)
        # # 验证发起产品人的经纪商ID
        # self.assertEqual(json.loads(GetProductRES.text)['data']['items']['Trader']['BrokerID'], 1)
        # # 验证交易员的分成收益
        # self.assertEqual(json.loads(GetProductRES.text)['data']['items']['MyProfit'], self.traderProfit)
        # # 验证跟随者的分成收益
        # self.assertEqual(json.loads(GetProductRES.text)['data']['summary']['FollowerProfit'], self.followerProfit)

    def tearDown(self):
        #退出登录
        pass
        # userData['headers'][userData['Authorization']] = userData['Bearer'] + self.traderToken
        # signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        # self.assertEqual(signoutRes.status_code, userData['status_code_200'])

        # userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        # signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        # self.assertEqual(signoutRes.status_code, userData['status_code_200'])
        #
        # loginOutOAUrl = userData['hostNameOA'] + userDataAuth['loginOutOA_url']
        # self.headerOA = {'content-type': 'application/json', 'Accept': 'application/json',
        #                  'Authorization': 'Bearer ' + str(self.tokenOA)}
        # loginOutOARes = Auth.loginOut(loginOutOAUrl, headers=self.headerOA)
        # '''退出OA成功'''
        # self.assertEqual(loginOutOARes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(CreateProduct))
    unittest.TextTestRunner(verbosity=2).run(suite)