#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID:
# 用例标题: Sam
# 预置条件:
# 测试步骤:
# 预期结果:
# 脚本作者: wangmingli
# 写作日期: 20180705
# -*- coding:utf-8 -*
import sys,unittest,json,grpc,time,threading
sys.path.append("../../lib/proto")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeSAM")
sys.path.append("../../test/follow")
import FMCommon,TradeSAM,Account,Follow,Auth,Trade
import FollowOperation
from mt4api import mt4api_pb2
from mt4api import mt4api_pb2_grpc
from tradesignal import tradesignal_pb2
from tradesignal import tradesignal_pb2_grpc

webAPIData = FMCommon.loadWebAPIYML()
commonConf = FMCommon.loadPublicYML()
userDataFollow=FMCommon.loadFollowYML()
userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()
userDataTrade=FMCommon.loadTradeYML()

class SamFollowSam(unittest.TestCase):
    def setUp(self):
        '''测试Sam经纪商开仓,平仓,历史订单'''
        # 连接测试服务器
        host = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],server='followme.srv.mt4api.3', key='ServiceAddress')
        port = FMCommon.consul_operater(host=commonConf['consulHost'], port=commonConf['consulPort'],server='followme.srv.mt4api.3', key='ServicePort')
        channel = grpc.insecure_channel(host + ':' + str(port))
        print(channel)
        self.stub = mt4api_pb2_grpc.MT4APISrvStub(channel)

        # 跟随者登录
        datas = {"account": webAPIData['wfollowAccount'], "password": webAPIData['wfollowpasswd'], "remember": "false"}
        loginRes = Auth.signin(webAPIData['hostName'] + userDataAuth['signin_url'], webAPIData['headers'], datas)
        self.assertEqual(loginRes.status_code, webAPIData['status_code_200'])
        self.token = json.loads(loginRes.text)['data']['token']

        # 交易员登录
        datas = {"account": webAPIData['waccount'], "password": webAPIData['wpasswd'], "remember": "false"}
        traderLoginRes = Auth.signin(webAPIData['hostName'] + userDataAuth['signin_url'], webAPIData['headers'], datas)
        self.assertEqual(traderLoginRes.status_code, webAPIData['status_code_200'])
        self.traderToken = json.loads(traderLoginRes.text)['data']['token']
        self.traderUserId = json.loads(traderLoginRes.text)['data']['id']

    def test_SamFollowSam(self):
        brokerID = 106
        symbol = 'AUDCAD'
        cmd = 0
        lots = 0.1

        webAPIData['headers'] = dict(webAPIData['headers'], **{'Authorization': webAPIData['Bearer'] + self.token})
        self.traderHeaders = dict(webAPIData['headers'], **{'Authorization': webAPIData['Bearer'] + self.traderToken})

        # 获取交易员的accountindex
        self.tradeAccountIndex = Account.getSpecialAccountIndex(headers=self.traderHeaders, accountType=2, brokerID=brokerID)
        print("self.tradeAccountIndex:", self.tradeAccountIndex[0])

        # 获取跟随者的accountindex
        self.followerAccountIndex = Account.getSpecialAccountIndex(headers=webAPIData['headers'], accountType=2, brokerID=brokerID)
        print("self.followerAccountIndex:", self.followerAccountIndex[0])

        # 新建一个跟随,固定手数跟随
        params = {"accountIndex": int(self.followerAccountIndex[0]), "strategy": "fixed", "setting": 0.5, "direction": "positive"}
        getFollowsRes = Follow.createFollow(webAPIData['hostName'] + userDataFollow["Follow_Url"] + str(self.traderUserId) + "_" + self.tradeAccountIndex[0],
                                            headers=webAPIData['headers'], datas=params)
        FMCommon.printLog('getFollowsRes: ' + getFollowsRes.text)
        self.assertEqual(getFollowsRes.status_code, webAPIData['status_code_200'])

        # 交易员切换账户
        switchAccountRes = Account.switchAccount(webAPIData['hostName'] + userDataAccount['switchAccount'], self.traderHeaders, self.tradeAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, webAPIData['status_code_200'])

        # 获取交易员MT4Account
        traderTokenRes = Trade.getToken(webAPIData['hostName'] + userDataAccount["getToken_url"], self.traderHeaders)
        self.assertEqual(traderTokenRes.status_code, webAPIData['status_code_200'])
        MT4Account = str(json.loads(traderTokenRes.content)["data"]["MT4Account"])

        # 循环开仓
        length = 1
        TradeIDList = []
        for i in range(0, length):
            openRes = TradeSAM.TradeSAMStream.OpenPosition(stub=self.stub, account=MT4Account, brokerID=brokerID, symbol=symbol, cmd=cmd, lots=lots)
            print(openRes)
            self.assertEqual(openRes.Signal.Symbol, symbol)
            tradeID = openRes.Signal.TradeID
            self.assertIsNotNone(tradeID, "交易员订单ID为空！")
            TradeIDList.append(tradeID)
        print(TradeIDList)

        # 循环平仓
        for i in TradeIDList:
            closeRes = TradeSAM.TradeSAMStream.ClosePosition(stub=self.stub, account=MT4Account, brokerID=brokerID, tradeID=i, lots=lots)
            print(closeRes)
            self.assertEqual(closeRes.Signal.TradeID, i)
            self.assertEqual(closeRes.Signal.Symbol, symbol)

        # 跟随者切换账户
        switchAccountRes = Account.switchAccount(webAPIData['hostName'] + userDataAccount['switchAccount'], webAPIData['headers'], self.followerAccountIndex[0])
        self.assertEqual(switchAccountRes.status_code, webAPIData['status_code_200'])

        # 获取跟随者MT4Account
        followertokenRES = Trade.getToken(webAPIData['hostName'] + userDataAccount["getToken_url"], webAPIData['headers'])
        self.assertEqual(followertokenRES.status_code, webAPIData['status_code_200'])
        MT4Account = str(json.loads(followertokenRES.content)["data"]["MT4Account"])

        # 验证跟随者跟单成功
        followTraderid=[]
        for i in TradeIDList:
            sql = "SELECT TradeID from t_followorder where Account=" + MT4Account + " and TraderTradeID=" + str(i)
            row = FollowOperation.Operation.operationCopytradingDB(sql)
            self.assertIsNotNone(row['TradeID'], '跟随者订单号为空')
            followTraderid.append(str(row['TradeID']))
            self.assertTrue(len(followTraderid) >= length)

    def tearDown(self):
        # 退出登录
        pass

if __name__ == '__main__':
    unittest.main()