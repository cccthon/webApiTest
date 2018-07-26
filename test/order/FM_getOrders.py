#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getOrders
# 用例标题: 获取当前用户的交易订单
# 预置条件: 
# 测试步骤:
#   1.登陆获取当前用户的交易订单
# 预期结果:
#   1.检查响应码为：200，nickname正确
#   2.平掉所有订单
# 脚本作者: shencanhui
# 写作日期: 20171212
#=========================================================
import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import Auth,FMCommon,Order,TradeOnline,Account
from socketIO_client import SocketIO
from base64 import b64encode

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
orderData = FMCommon.loadOrderYML()
tradeOnlineData = FMCommon.loadTradeOnlineYML()

class Orders(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        datas = {"account":webAPIData['account'], "password":webAPIData['passwd'], "remember":"false"}
        signinRes = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], datas)
        #登录成功，返回200 ok
        self.assertEqual(signinRes.status_code, webAPIData['status_code_200'])
        #保存登录时的token，待登出使用
        self.token = json.loads(signinRes.text)['data']['token']
        #规整headers
        self.tradeHeaders = dict(webAPIData['headers'], **{webAPIData['Authorization'] : webAPIData['Bearer'] + self.token})
        #获取交易token
        self.tradeToken = Account.getToken(self.tradeHeaders, onlyTokn="true", printLogs=1)

    def test_close_Orders(self):
        '''获取当前用户的所有交易订单，并平掉'''
        params = {webAPIData['orderStatus']:webAPIData['orderStatus_open']}
        getOrders = Order.getOrders(webAPIData['hostName'] + orderData['getOrders_url'], self.tradeHeaders, params=params)
        #获取订单成功，返回200 ok
        self.assertEqual(getOrders.status_code, webAPIData['status_code_200'])
        ordersIDList = Order.getOrdersID(getOrders)

        #平掉当前用户所有订单,如果有
        # #web sockets批量平仓
        closeParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_219'], tradeOnlineData['orderParam_tickets']: ordersIDList }
        closePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.tradeToken}, closeParam)
        #校验code等于0，为及时单平仓成功
        self.assertEqual(closePositionRes["code"], tradeOnlineData['ws_code_0'])
        #校验rcmd等于210，为及时单开仓
        self.assertEqual(closePositionRes["rcmd"], tradeOnlineData['ws_code_219'])
        #校验平掉的单号，为本测试及时单开仓的单号
        self.assertEqual(closePositionRes['success_tickets'], ordersIDList)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        signoutRes = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = webAPIData['headers'])
        self.assertEqual(signoutRes.status_code, webAPIData['status_code_200'])

if __name__ == '__main__':
    unittest.main()

