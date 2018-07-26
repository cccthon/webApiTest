#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getHomeFollower
# 用例标题: 获取首页的跟随者收益信息
# 预置条件: 
# 测试步骤:
#   1.不登录的情况下获取首页的跟随者收益信息
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: shencanhui
# 写作日期: 20171211
#=========================================================
import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,Account,Statistic
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
accountData = FMCommon.loadAccountYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()

class UserInfo(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_1_userInfo(self):
        '''鼠标停在头像上的悬浮窗数据'''
        userID = "148174_2"
        userData = Account.getUserInfo(webAPIData['hostName'] + accountData['getUserInfo_url'] + userID,printLogs=0)
        self.assertEqual(userData.status_code, webAPIData['status_code_200'])
        self.assertNotEqual(json.loads(userData.text)["data"]["user"],{},"不存在用户信息数据")
        print("userInfo:")
        table = PrettyTable(["预期/实际","NickName","UserID","mt4Account","AccountIndex","BrokerId","跟随获利","收益率","订单数","交易周期","关注人数","粉丝人数"])
        userInfo = json.loads(userData.text)["data"]["user"]
        mt4Account = Statistic.getMt4Account(userID=str(userInfo["UserId"]),accountIndex=str(userInfo["AccountIndex"]))
        followProfit = Statistic.followProfit(mt4Account=mt4Account,brokerID=userInfo["BrokerId"])
        rateProfit = Statistic.rateProfit(mt4Account=mt4Account,brokerID=userInfo["BrokerId"])
        ordersCount = Statistic.ordersCount(mt4Account=mt4Account,brokerID=userInfo["BrokerId"])
        tradePeriod = Statistic.tradePeriod(mt4Account=mt4Account,brokerID=userInfo["BrokerId"])
        attentionCount = Statistic.attentionCount(mt4Account=mt4Account)
        fansCount = Statistic.fansCount(mt4Account=mt4Account)
        table.add_row(["预期结果",userInfo["NickName"],userInfo["UserId"],mt4Account,userInfo["AccountIndex"],userInfo["BrokerId"],followProfit,rateProfit,ordersCount,tradePeriod,attentionCount,fansCount])
        table.add_row(["实际结果",userInfo["NickName"],userInfo["UserId"],mt4Account,userInfo["AccountIndex"],userInfo["BrokerId"],userInfo["FollowProfit"],str(userInfo["ROI"])+'%',userInfo["Orders"],userInfo["Weeks"],userInfo["AttentionCount"],userInfo["FansCount"]])
        try:
            #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
            self.assertAlmostEqual(followProfit,userInfo["FollowProfit"],delta = 1000000)
            # self.assertAlmostEqual(rateProfit,userInfo["ROI"],delta = 1000000)
            self.assertAlmostEqual(ordersCount,userInfo["Orders"],delta = 1000000)
            self.assertAlmostEqual(tradePeriod,userInfo["Weeks"],delta = 1000000)
            self.assertAlmostEqual(attentionCount,int(userInfo["AttentionCount"]),delta = 1000000)
            self.assertAlmostEqual(fansCount,int(userInfo["FansCount"]),delta = 1000000)
        finally:
            table.reversesort = True
            print(table)

   
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

