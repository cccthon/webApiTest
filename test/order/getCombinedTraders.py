#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getCombinedTraders
# 用例标题: 获取智能组合列表（排行榜）
# 预置条件: 
# 测试步骤:
#   1.不登录的情况下获取智能组合列表（排行榜）
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180309
#=========================================================
import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,FollowManage,Statistic,Order,Follow,Account,RiskControl
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
followData = FMCommon.loadFollowYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()
orderData = FMCommon.loadOrderYML()
riskControlData = FMCommon.loadRiskControlYML()
accountData = FMCommon.loadAccountYML() 

class CombinedTraders(unittest.TestCase):
    def setUp(self):
        #跟随者登陆---------------------
        followDatas = {"account":webAPIData['followAccount'], "password":webAPIData['followPasswd'], "remember":"false"}
        followSignin = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], followDatas)
        #登录成功，返回200 ok
        self.assertEqual(followSignin.status_code, webAPIData['status_code_200'])
        #保存账号的nickName
        self.followNickName = json.loads(followSignin.text)['data']['nickname']
        # #保存登录时的token，待登出使用
        self.followUserToken = json.loads(followSignin.text)['data']['token']
        #规整headers
        self.followHeaders = dict(webAPIData['headers'], **{webAPIData['Authorization'] : webAPIData['Bearer'] + self.followUserToken})
        #获取指定经纪商的accountIndex。当前为：pcio
        self.followPicoAccountIndex = Account.getSpecialAccountIndex(headers = self.followHeaders,brokerID=riskControlData["testBrokerID"])[0]
        print(self.followPicoAccountIndex)
        self.switchFollowAccount = Account.switchAccount(webAPIData['hostName'] + accountData['switchAccount'], self.followHeaders, index=self.followPicoAccountIndex)
        print(self.switchFollowAccount.text)
        #账号切换成功
        self.assertEqual(self.switchFollowAccount.status_code, webAPIData['status_code_200'])
        #获取跟随者交易token
        self.followToken = Account.getToken(self.followHeaders, onlyTokn="true", printLogs=1)

    def test_1_getCombinedTraders_Broker(self):
        self.combinedTraders = Order.getCombinedTraders(webAPIData['hostName'] + orderData['getCombinedTraders_url'],params="",printLogs=0)
        self.assertEqual(self.combinedTraders.status_code, webAPIData['status_code_200'])

        '''断言跟随者是否能够正常跟随组合交易员'''
        combinedTraders_Broker = []
        combinedTraders_AccountCurrentIndex = []
        for item in json.loads(self.combinedTraders.text)["data"]["items"][0]["TraderList"]:
            combinedTraders_Broker.append(item["UserId"])
            combinedTraders_AccountCurrentIndex.append(item["AccountCurrentIndex"])
            print(combinedTraders_Broker)
            print(combinedTraders_AccountCurrentIndex)

        followDatas={"accountIndex": self.followPicoAccountIndex, "list":[{"Trader": str(combinedTraders_Broker[0]) + "_" + str(combinedTraders_AccountCurrentIndex[0]), "StrategyType": 1, "Direction": 1, "FollowSetting": 0.2},
                {"Trader": str(combinedTraders_Broker[1]) + "_" + str(combinedTraders_AccountCurrentIndex[1]), "StrategyType": 1, "Direction": 1, "FollowSetting": 0.3},
                {"Trader": str(combinedTraders_Broker[2]) + "_" + str(combinedTraders_AccountCurrentIndex[2]), "StrategyType": 1, "Direction": 1, "FollowSetting": 0.1},
                {"Trader": str(combinedTraders_Broker[3]) + "_" + str(combinedTraders_AccountCurrentIndex[3]), "StrategyType": 1, "Direction": 1, "FollowSetting": 0.2},
                {"Trader": str(combinedTraders_Broker[4]) + "_" + str(combinedTraders_AccountCurrentIndex[4]), "StrategyType": 1, "Direction": 1, "FollowSetting": 0.6}]}
        self.follows = Follow.follows(webAPIData['hostName'] + followData['follows_url'],headers = self.followHeaders,datas = followDatas,printLogs=0)
        self.assertEqual(self.follows.status_code, webAPIData['status_code_200'])


    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        followSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.followHeaders)
        self.assertEqual(followSignout.status_code, webAPIData['status_code_200'])

if __name__ == '__main__':
    unittest.main()

