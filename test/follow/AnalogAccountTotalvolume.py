# -*- coding:utf-8 -*
import sys,yaml
import unittest,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
sys.path.append("../../test/follow")
import FMCommon,TradeOnline,Auth,Follow,Trade,Account
from socketIO_client import SocketIO
from RegisterByEmail import RegisterByEmail
import FollowOperation

userData = FMCommon.loadWebAPIYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()
userDataFollow=FMCommon.loadFollowYML()
userDataAuth=FMCommon.loadAuthYML()
userDataTrade=FMCommon.loadTradeYML()
userDataAccount=FMCommon.loadAccountYML()

class AnalogAccountTotalvolume(unittest.TestCase):
    def setUp(self):
        #通过邮箱注册账号，获取模拟账户
        accountEmail =RegisterByEmail.RegisterByEmail()
        print(accountEmail)
        datas = {"account": accountEmail, "password": '123456', "remember": "false"}
        loginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(loginRes.status_code, userData['status_code_200'])
        self.token = json.loads(loginRes.text)['data']['token']

    def test_AnalogAccountTotalvolume(self):
        '''验证模拟账号最大持仓为3手'''
        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})

        # 获取模拟账户的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], brokerID=3, accountType=0)

        #模拟账号切换账户
        Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'], userData['headers'],
                              self.tradeAccountIndex[0])

        # 获取模拟账号交易token
        traderTokenRes = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], userData['headers'])
        self.assertEqual(traderTokenRes.status_code, userData['status_code_200'])
        tradeToken = str(json.loads(traderTokenRes.content)["data"]["Token"]).replace("=", "@")

        # 模拟账号开仓
        openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                     userDataWebSocket['orderParam_symbol']: userDataWebSocket['broker_EURCAD'],
                     userDataWebSocket['orderParam_volume']: 3100}
        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(
            self, userDataWebSocket['ws_host'], userDataWebSocket['ws_port'], {'token': "" + tradeToken}, openParam)
        self.assertEqual(openPositionRes["code"], 19)
        print("模拟账号最大持仓为3手!")

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(AnalogAccountTotalvolume))
    unittest.TextTestRunner(verbosity=2).run(suite)