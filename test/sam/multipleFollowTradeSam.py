#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID:
# 用例标题: Sam
# 预置条件:
# 测试步骤:
# 预期结果:
# 脚本作者: wangmingli
# 写作日期: 20180705
# -*- coding:utf-8 -*
import sys,yaml,unittest,json,time,grpc
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
sys.path.append("../../test/follow")
import FMCommon,TradeOnline,Auth,Follow,Trade,Account,Order,TradeSAM,FollowOperation
from socketIO_client import SocketIO
from mt4api import mt4api_pb2
from mt4api import mt4api_pb2_grpc
from tradesignal import tradesignal_pb2
from tradesignal import tradesignal_pb2_grpc

userData = FMCommon.loadWebAPIYML()
order = FMCommon.loadOrderYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()
userDataFollow=FMCommon.loadFollowYML()
userDataAuth=FMCommon.loadAuthYML()
userDataTrade=FMCommon.loadTradeYML()
userDataAccount=FMCommon.loadAccountYML()
commonConf = FMCommon.loadPublicYML()

class multipleFollowTradeSam(unittest.TestCase):
    def setUp(self):
        '''多个Sam跟随下单'''
        #跟随者登录
        datas = {"account": userData['wfollowAccount'], "password": userData['wfollowpasswd'], "remember": "false"}
        loginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(loginRes.status_code, userData['status_code_200'])
        self.token = json.loads(loginRes.text)['data']['token']

        # 交易员登录
        datas = {"account": userData['waccount'], "password": userData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, userData['status_code_200'])
        self.traderToken = json.loads(traderLoginRes.text)['data']['token']
        self.traderUserId = json.loads(traderLoginRes.text)['data']['id']
        self.traderNickname = json.loads(traderLoginRes.text)['data']['nickname']

        # 连接sam服务器
        host = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],
                                        server='followme.srv.mt4api.3', key='ServiceAddress')
        port = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],
                                        server='followme.srv.mt4api.3', key='ServicePort')
        channel = grpc.insecure_channel(host + ':' + str(port))
        self.stub = mt4api_pb2_grpc.MT4APISrvStub(channel)

    def test_BatchFollowTrade(self):
        '''建立批量跟随->跟随下单->跟随平仓->查看跟随交易历史订单->取消跟随'''
        account = '500383407'  # 跟随者身份
        brokerID = 106
        symbol = 'AUDCAD'
        cmd = 0
        lots = 0.1

        userData['headers'] = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.token})
        self.traderHeaders = dict(userData['headers'], **{'Authorization': userData['Bearer'] + self.traderToken})

        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=self.traderHeaders, accountType=2, brokerID=106)

        # 获取跟随者的accountindex
        self.followerAccountIndex = Account.getSpecialAccountIndex(headers=userData['headers'], accountType=2, brokerID=106)

        # 建立多个跟随
        createfollowList = []
        for i in self.followerAccountIndex:
            follower =FollowOperation.Operation.createFollow(self.traderUserId, self.tradeAccountIndex[0], userData['headers'], i)
            createfollowList.append(follower)
        print("创建跟随者：", createfollowList)

        # 交易员切换账户
        switchAccountRes = Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],
                                                 self.traderHeaders, self.tradeAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, userData['status_code_200'])

        # 获取交易员MT4Account
        traderTokenRes = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], self.traderHeaders)
        self.assertEqual(traderTokenRes.status_code, userData['status_code_200'])
        TraderAccount = str(json.loads(traderTokenRes.content)["data"]["MT4Account"])

        # 循环开仓
        TradeIDList = []
        for i in range(0, 10):
            openRes = TradeSAM.TradeSAMStream.OpenPosition(stub=self.stub, account=account, brokerID=brokerID,
                                                           symbol=symbol, cmd=cmd, lots=lots)
            print(openRes)
            self.assertEqual(openRes.Signal.Symbol, symbol)
            tradeID = openRes.Signal.TradeID
            TradeIDList.append(tradeID)
        print(TradeIDList)

        # 循环平仓
        for i in TradeIDList:
            closeRes = TradeSAM.TradeSAMStream.ClosePosition(stub=self.stub, account=account, brokerID=brokerID,
                                                             tradeID=i, lots=lots)
            print(closeRes)
            self.assertEqual(closeRes.Signal.TradeID, i)
            self.assertEqual(closeRes.Signal.Symbol, symbol)

        #  批量取消跟随者的跟随
        deletefollowList = []
        for j in self.followerAccountIndex:
            follower = FollowOperation.Operation.deleteFollow(self.traderUserId, self.tradeAccountIndex[0], userData['headers'], j)
            deletefollowList.append(follower)
        print("取消跟随者：", deletefollowList)

        # 验证交易员的跟随者订单
        followTraderid = []
        for i in TradeIDList:
            sql = "SELECT TradeID from t_followorder where TraderAccount=" + TraderAccount + " and TraderTradeID=" + str(i)
            row = FollowOperation.Operation.operationCopytradingDB(sql)
            self.assertIsNotNone(row['TradeID'], '跟随者订单号为空')
            followTraderid.append(str(row['TradeID']))
            self.assertTrue(len(followTraderid) >= len(self.followerAccountIndex))

    def tearDown(self):
        # 退出登录
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.token
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.traderToken
        signoutRes = Auth.signout(userData['hostName'] + userDataAuth['signout_url'], datas=userData['headers'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    suite = unittest.TestSuite(unittest.makeSuite(multipleFollowTradeSam))
    unittest.TextTestRunner(verbosity=2).run(suite)