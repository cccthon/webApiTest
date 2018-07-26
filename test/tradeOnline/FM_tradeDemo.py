#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_TradeOnLine_open_001_001
# 用例标题: 开仓与平仓
# 预置条件: 
# 测试步骤:
#   1.建立socket链接
#   2.发起开仓请求
#   3.监听socket响应，检查开仓返回值
# 预期结果:
#   1.开仓成功，返回0.订单信息正常
# 脚本作者: shencanhui
# 写作日期: 20171102
#=========================================================
import sys,unittest,json,requests
sys.path.append("../../lib/common")
sys.path.append("../../lib/tradeOnline")
sys.path.append("../../lib/WebAPI")
import FMCommon,TradeOnline,Auth,Account
from socketIO_client import SocketIO
from base64 import b64encode
from Timer import func_timer
userData = FMCommon.loadTradeOnlineYML()
webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
accountData = FMCommon.loadAccountYML()

class openAndClosePosition(unittest.TestCase):
    def setUp(self):
        #登录followme系统
        #交易员登陆---------------------
        tradeDatas = {"account":webAPIData['account'], "password":webAPIData['passwd'], "remember":"false"}
        tradeSignin = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], tradeDatas)
        #登录成功，返回200 ok
        self.assertEqual(tradeSignin.status_code, webAPIData['status_code_200'])
        # #保存登录时的token，待登出使用
        self.tradeUserToken = json.loads(tradeSignin.text)['data']['token']
        #规整headers
        self.tradeHeaders = dict(webAPIData['headers'], **{webAPIData['Authorization'] : webAPIData['Bearer'] + self.tradeUserToken})
        #获取交易员交易token
        self.tradeToken = Account.getToken(self.tradeHeaders, onlyTokn="true", printLogs=1)
    @func_timer
    def test_openAndClosePosition(self):
        '''web sockets开仓后再平仓'''
        openParam = { userData['orderParam_code']: userData['ws_code_210'], userData['orderParam_symbol']: userData['broker_EURCAD'], userData['orderParam_volume']: 300 }
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userData['ws_host'], userData['ws_port'], {'token': self.tradeToken}, openParam)
        # print(openPositionRes)
        # print(type(openPositionRes))
        #校验code等于0，为及时单开仓成功
        self.assertEqual(openPositionRes["code"], userData['ws_code_0'])
        #校验rcmd等于210，为及时单开仓
        self.assertEqual(openPositionRes["rcmd"], userData['ws_code_210'])
        #校验手数为下单时的手数
        self.assertEqual(openPositionRes["order"]["volume"], 300)
        #校验品种为下单时的经纪商品种
        self.assertEqual(openPositionRes["order"]["symbol"], userData['broker_EURCAD'])
        #保存orderID,待开仓使用
        self.orderID = openPositionRes["order"]["order_id"]

        #web sockets部分平仓
        partClose = { userData['orderParam_code']: userData['ws_code_211'], userData['orderParam_ticket']: self.orderID, userData['orderParam_volume']: 100 }
        partClosePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userData['ws_host'], userData['ws_port'], {'token': self.tradeToken}, partClose)
        self.newOrderID = int(partClosePositionRes["order"]["comment"].split('#')[-1])
        #校验code等于0，为及时单平仓成功
        self.assertEqual(partClosePositionRes["code"], userData['ws_code_0'])
        #校验rcmd等于210，为及时单开仓
        self.assertEqual(partClosePositionRes["rcmd"], userData['ws_code_223'])
        #校验平掉的单号，为本测试及时单开仓的单号
        self.assertEqual(partClosePositionRes['order']["order_id"], self.orderID)

        # #web sockets部分平仓
        closeParam = { userData['orderParam_code']: userData['ws_code_211'], userData['orderParam_ticket']: self.newOrderID, userData['orderParam_volume']: 200 }
        closePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, userData['ws_host'], userData['ws_port'], {'token': self.tradeToken}, closeParam)
        #校验code等于0，为及时单平仓成功
        self.assertEqual(closePositionRes["code"], userData['ws_code_0'])
        #校验rcmd等于210，为及时单开仓
        self.assertEqual(closePositionRes["rcmd"], userData['ws_code_211'])
        #校验平掉的单号，为本测试及时单开仓的单号
        self.assertEqual(closePositionRes['order']["order_id"], self.newOrderID)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #将测试订单平掉。平仓
        #登出followme系统
        tradeSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.tradeHeaders)
        self.assertEqual(tradeSignout.status_code, webAPIData['status_code_200'])

if __name__ == '__main__':
    unittest.main()