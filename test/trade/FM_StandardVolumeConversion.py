# -*- coding:utf-8 -*
import sys,yaml,time
import unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,TradeOnline,Auth,Trade,Account,Order
from socketIO_client import SocketIO

userData = FMCommon.loadWebAPIYML()
order = FMCommon.loadOrderYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()

userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()

userDataSocial=FMCommon.loadSocialYML()
class StandardVolumeConversion(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.token = json.loads(traderLoginRes.text)['data']['token']

    def test_StandardVolumeConversion(self):
        '''KVB标准手转换,XAGCNY，XAGUSD，HSI43'''
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})

        # 获取accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=5)

        # 切换到MT4账号
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 userData['headers'],self.tradeAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])

        # 获取交易token
        getTokenRes = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], userData['headers'])
        FMCommon.printLog('getTokenRes: ' + getTokenRes.text)
        self.assertEqual(getTokenRes.status_code, userData['status_code_200'])
        tradeToken = str(json.loads(getTokenRes.content)["data"]["Token"]).replace("=", "@")
        print("tradeToken:", tradeToken)

        # 开仓XAGCNY
        openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                     userDataWebSocket['orderParam_symbol']: "XAGCNY",
                     userDataWebSocket['orderParam_volume']: 50}
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken}, openParam)
        if (openPositionRes["code"] == userDataWebSocket['ws_code_0']):
            self.assertEqual(openPositionRes["code"], userDataWebSocket['ws_code_0'])
            self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
            self.assertEqual(openPositionRes["order"]["volume"], 50)
            self.assertEqual(openPositionRes["order"]["fm_volume"], 7.5)
            self.orderID = openPositionRes["order"]["order_id"]
        elif (openPositionRes["code"] == 4):
            print("保证金不足！")
        elif (openPositionRes["code"] == 10):
            print("市场关闭！")
        elif (openPositionRes["code"] == 300):
            print("服务器内部错误！")
        elif (openPositionRes["code"] == 3):
            print("客户不存在！")
        elif (openPositionRes["code"] == 7):
            print("获取价格失败！")
        elif (openPositionRes["code"] == 9):
            print("手数错误！")
        elif (openPositionRes["code"] == 18):
            print("此品种不能交易！")
        else:
            print("其它错误")

        # 获取当前用户的交易订单
        time.sleep(3)
        params = {userData['orderStatus']: userData['orderStatus_open']}
        getOrders = Order.getOrders(userData['hostName'] + order['getOrders_url'], userData['headers'], params=params)
        self.assertEqual(getOrders.status_code, userData['status_code_200'])
        ordersIDList = Order.getOrdersID(getOrders)
        self.assertIn(self.orderID, ordersIDList)

        # 平仓
        closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_211'],
                      userDataWebSocket['orderParam_ticket']: self.orderID,
                      userDataWebSocket['orderParam_volume']: 50}
        closeOrderRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],userDataWebSocket['ws_port'],
                                                                {'token': "" + tradeToken}, closeOrder)
        if(closeOrderRes["code"]==userDataWebSocket['ws_code_0']):
            self.assertEqual(closeOrderRes["rcmd"], userDataWebSocket['ws_code_211'])
            self.assertEqual(closeOrderRes['order']["order_id"], self.orderID)
            self.assertEqual(closeOrderRes["order"]["volume"], 50)
            self.assertEqual(closeOrderRes["order"]["fm_volume"], 7.5)
        if(closeOrderRes["code"] == 13):
            print("订单不存在！")

        # 品种：XAGUSD
        # 开仓
        openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                     userDataWebSocket['orderParam_symbol']: "XAGUSD",
                     userDataWebSocket['orderParam_volume']: 50}
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
                                                                  userDataWebSocket['ws_port'],
                                                                  {'token': "" + tradeToken}, openParam)
        if (openPositionRes["code"] == userDataWebSocket['ws_code_0']):
            self.assertEqual(openPositionRes["code"], userDataWebSocket['ws_code_0'])
            self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
            self.assertEqual(openPositionRes["order"]["volume"], 50)
            self.assertEqual(openPositionRes["order"]["fm_volume"], 0.01)
            self.orderID = openPositionRes["order"]["order_id"]
        if (openPositionRes["code"] == 4):
            print("保证金不足！")
        if (openPositionRes["code"] == 10):
            print("市场关闭！")
        if (openPositionRes["code"] == 300):
            print("服务器内部错误！")
        if (openPositionRes["code"] == 3):
            print("客户不存在！")
        if (openPositionRes["code"] == 7):
            print("获取价格失败！")
        if (openPositionRes["code"] == 9):
            print("手数错误！")
        if (openPositionRes["code"] == 18):
            print("此品种不能交易！")

        # 获取当前用户的交易订单
        time.sleep(3)
        params = {userData['orderStatus']: userData['orderStatus_open']}
        getOrders = Order.getOrders(userData['hostName'] + order['getOrders_url'], userData['headers'], params=params)
        self.assertEqual(getOrders.status_code, userData['status_code_200'])
        ordersIDList = Order.getOrdersID(getOrders)
        self.assertIn(self.orderID, ordersIDList)

        # 平仓
        closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_211'],
                      userDataWebSocket['orderParam_ticket']: self.orderID,
                      userDataWebSocket['orderParam_volume']: 50}
        closeOrderRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
                                                                userDataWebSocket['ws_port'],
                                                                {'token': "" + tradeToken}, closeOrder)
        if (closeOrderRes["code"] == userDataWebSocket['ws_code_0']):
            self.assertEqual(closeOrderRes["rcmd"], userDataWebSocket['ws_code_211'])
            self.assertEqual(closeOrderRes['order']["order_id"], self.orderID)
            self.assertEqual(closeOrderRes["order"]["volume"], 50)
            self.assertEqual(closeOrderRes["order"]["fm_volume"], 0.01)
        if (closeOrderRes["code"] == 13):
            print("订单不存在！")


        # 品种：HSI43
        # 开仓
        openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                     userDataWebSocket['orderParam_symbol']: "HSI43",
                     userDataWebSocket['orderParam_volume']: 100}
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
                                                                  userDataWebSocket['ws_port'],
                                                                  {'token': "" + tradeToken}, openParam)
        if (openPositionRes["code"] == userDataWebSocket['ws_code_0']):
            self.assertEqual(openPositionRes["code"], userDataWebSocket['ws_code_0'])
            self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
            self.assertEqual(openPositionRes["order"]["volume"], 100)
            self.assertEqual(openPositionRes["order"]["fm_volume"], 0.02)
            self.orderID = openPositionRes["order"]["order_id"]
        if (openPositionRes["code"] == 4):
            print("保证金不足！")
        if (openPositionRes["code"] == 10):
            print("市场关闭！")
        if (openPositionRes["code"] == 300):
            print("服务器内部错误！")
        if (openPositionRes["code"] == 3):
            print("客户不存在！")
        if (openPositionRes["code"] == 7):
            print("获取价格失败！")
        if (openPositionRes["code"] == 9):
            print("手数错误！")
        if (openPositionRes["code"] == 18):
            print("此品种不能交易！")

        # 获取当前用户的交易订单
        time.sleep(3)
        params = {userData['orderStatus']: userData['orderStatus_open']}
        getOrders = Order.getOrders(userData['hostName'] + order['getOrders_url'], userData['headers'], params=params)
        self.assertEqual(getOrders.status_code, userData['status_code_200'])
        ordersIDList = Order.getOrdersID(getOrders)

        self.assertIn(self.orderID, ordersIDList,ordersIDList)

        # 平仓
        closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_211'],
                      userDataWebSocket['orderParam_ticket']: self.orderID,
                      userDataWebSocket['orderParam_volume']: 100}
        closeOrderRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],
                                                                userDataWebSocket['ws_port'],
                                                                {'token': "" + tradeToken}, closeOrder)
        if (closeOrderRes["code"] == userDataWebSocket['ws_code_0']):
            self.assertEqual(closeOrderRes["rcmd"], userDataWebSocket['ws_code_211'])
            self.assertEqual(closeOrderRes['order']["order_id"], self.orderID)
            self.assertEqual(closeOrderRes["order"]["volume"], 100)
            self.assertEqual(closeOrderRes["order"]["fm_volume"], 0.02)
        if (closeOrderRes["code"] == 13):
            print("订单不存在！")

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.makeSuite(StandardVolumeConversion)
    unittest.TextTestRunner(verbosity=2).run(suite)


