# -*- coding:utf-8 -*
import sys,yaml
import unittest,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
sys.path.append("../../test/follow")
import FMCommon,TradeOnline,Auth,Trade,Account,Order
from socketIO_client import SocketIO
import FollowOperation

userData = FMCommon.loadWebAPIYML()
order = FMCommon.loadOrderYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()

userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()
userDataTrade=FMCommon.loadTradeYML()

userDataSocial=FMCommon.loadSocialYML()
class PartClosePositionByPico(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.token = json.loads(traderLoginRes.text)['data']['token']

    def test_PartClosePositionByPico(self):
        '''验证部分平仓，交易员开仓，部分平仓，检查持仓单，检查历史订单'''
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})

        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=6)

        # 切换到MT4账号
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 userData['headers'],self.tradeAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])

        # 获取交易token
        getTokenRes = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], userData['headers'])
        FMCommon.printLog('getTokenRes: ' + getTokenRes.text)
        self.assertEqual(getTokenRes.status_code, userData['status_code_200'])
        tradeToken = str(json.loads(getTokenRes.content)["data"]["Token"]).replace("=", "@")
        MT4Account = str(json.loads(getTokenRes.content)["data"]["MT4Account"])

        # 开仓
        openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                     userDataWebSocket['orderParam_symbol']: "AUDCAD",
                     userDataWebSocket['orderParam_volume']: 2}
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(
            self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken}, openParam)
        if (openPositionRes["code"] == userDataWebSocket['ws_code_0']):
            self.assertEqual(openPositionRes["rcmd"], userDataWebSocket['ws_code_210'])
            self.assertEqual(openPositionRes["order"]["volume"], 2)
            self.assertEqual(openPositionRes["order"]["symbol"], "AUDCAD")
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

        time.sleep(5)
        # 获取开仓单
        params = {userData['orderStatus']: userData['orderStatus_open']}
        getOrders = Order.getOrders(userData['hostName'] + order['getOrders_url'], userData['headers'], params=params)
        self.assertEqual(getOrders.status_code, userData['status_code_200'])
        self.assertIn(str(self.orderID), str(json.loads(getOrders.content)["data"]["items"]), "持仓列表中没有包含此订单")

        # 部分平仓
        closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_211'],
                      userDataWebSocket['orderParam_ticket']: self.orderID,
                      userDataWebSocket['orderParam_volume']: 1}
        closeOrderRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userDataWebSocket['ws_host'],userDataWebSocket['ws_port'],
                                                                {'token': "" + tradeToken}, closeOrder)
        self.assertEqual(closeOrderRes["code"], userDataWebSocket['ws_code_0'])
        self.assertEqual(closeOrderRes["rcmd"], userDataWebSocket['ws_code_223'])
        self.assertEqual(closeOrderRes['order']["order_id"], self.orderID)
        self.assertEqual(closeOrderRes["order"]["volume"], 1)
        self.assertEqual(openPositionRes["order"]["symbol"], "AUDCAD")

        # 查询历史订单
        time.sleep(5)
        getHistoryOrderRes = Trade.getOrders(userData['hostName'] + userDataTrade["getOrders"], userData['headers'],
                                             userData['orderStatus_close'])
        FMCommon.printLog('getHistoryOrderRes: ' + getHistoryOrderRes.text)
        self.assertEqual(getHistoryOrderRes.status_code, userData['status_code_200'])
        self.assertIn(str(self.orderID), str(json.loads(getHistoryOrderRes.content)["data"]["items"]),"历史订单列表中不包含此订单")
        #验证此历史订单的手数是否与部分平仓手数一致
        sql = 'SELECT StandardLots,BrokerLots from t_trades WHERE TradeID='+str(self.orderID)+'and Account='+MT4Account
        row = FollowOperation.Operation.operationCopytradingDB(sql)
        self.assertEqual(1, int(row['StandardLots']), "部分平仓手数错误")
        self.assertEqual(1, int(row['BrokerLots']), "部分平仓手数错误")

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.makeSuite(PartClosePositionByPico)
    unittest.TextTestRunner(verbosity=2).run(suite)


