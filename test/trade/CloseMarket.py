# -*- coding:utf-8 -*
import sys,yaml
import unittest,json
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

userDataSocial=FMCommon.loadSocialYML()
class CloseMarket(unittest.TestCase):
    def setUp(self):
        # 登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.token = json.loads(traderLoginRes.text)['data']['token']

    def test_CloseMarket(self):
        '''验证休市时，直盘交易品种订单的收益点数和收益金额'''
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})

        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=5)

        # 切换到MT4账号
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 userData['headers'], self.tradeAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])

        # 获取持仓订单
        params = {userData['orderStatus']: userData['orderStatus_open']}
        getOrders = Order.getOrders(userData['hostName'] + order['getOrders_url'], userData['headers'], params=params)
        self.assertEqual(getOrders.status_code, userData['status_code_200'])
        # 获取开仓价格
        OPEN_PRICE = json.loads(getOrders.text)['data']['items'][0]['OPEN_PRICE']
        print("OPEN_PRICE:", OPEN_PRICE)
        # 获取现价
        CLOSE_PRICE = json.loads(getOrders.text)['data']['items'][0]['CLOSE_PRICE']
        print("CLOSE_PRICE:", CLOSE_PRICE)
        #计算收益点数
        pips = round(float(OPEN_PRICE)*10000 - float(CLOSE_PRICE)*10000, 2)
        print("pips:", pips)
        #计算收益金额
        profit = round(pips * 10 * 0.1, 2)
        print("profit:", profit)
        #收益金额
        PROFIT = round(json.loads(getOrders.text)['data']['items'][0]['PROFIT'], 2)
        print("PROFIT:", PROFIT)
        #收益点数
        POINT = round(json.loads(getOrders.text)['data']['items'][0]['POINT'], 2)
        print("POINT:", POINT)
        #验证点数和金额正确
        self.assertEqual(profit, PROFIT, "收益金额错误")
        self.assertEqual(pips, POINT, "收益点数错误")


    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.makeSuite(CloseMarket)
    unittest.TextTestRunner(verbosity=2).run(suite)

