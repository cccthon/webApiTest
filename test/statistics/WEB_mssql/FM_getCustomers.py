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
import Auth,FMCommon,Common,Trade,Statistic
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
tradeData = FMCommon.loadTradeYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()

class Customers(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_1_getCustomers(self):
        '''获取近一周有交易的跟随大师信息'''
        params = {"time":7,"pageField":"FollowProfit"}
        customers = Trade.getCustomers(webAPIData['hostName'] + tradeData['getCustomers_url'],params=params,printLogs=1)
        self.assertEqual(customers.status_code, webAPIData['status_code_200'])
        print("Customers_oneWeek:")
        table = PrettyTable(["预期/实际","NickName","UserID","mt4Account","AccountIndex","近一日跟随获利","近一日盈亏点数","收益率","平均获利点数","交易笔数","交易周期"])
        try:
            for item in json.loads(customers.text)["data"]["items"]:
                mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                moneyFollowCloseDay = Statistic.moneyFollowCloseDay(mt4Account=mt4Account,brokerID=item["BrokerId"])
                pointCloseDay = Statistic.pointCloseDay(mt4Account=mt4Account,brokerID=item["BrokerId"])
                rateProfit = Statistic.rateProfit(mt4Account=mt4Account,brokerID=item["BrokerId"])
                pointProfitCloseMean = Statistic.pointProfitCloseMean(mt4Account=mt4Account,brokerID=item["BrokerId"])
                ordersCount = Statistic.ordersCount(mt4Account=mt4Account,brokerID=item["BrokerId"])
                tradePeriod = Statistic.tradePeriod(mt4Account=mt4Account,brokerID=item["BrokerId"])
                table.add_row(["预期结果",item["NickName"],item["UserId"],mt4Account,item["AccountCurrentIndex"],moneyFollowCloseDay,pointCloseDay,rateProfit,pointProfitCloseMean,ordersCount,tradePeriod])
                table.add_row(["实际结果",item["NickName"],item["UserId"],mt4Account,item["AccountCurrentIndex"],item["BizFollowProfit"],item["BizPoint"],item["BizROIex"],item["BizAVGPoint"],item["Orders"],item["Weeks"]])
                table.add_row(["","","","","","","","","","",""])
                #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
                self.assertAlmostEqual(moneyFollowCloseDay,float(item["BizFollowProfit"]),delta = 1000000)
                self.assertAlmostEqual(pointCloseDay,float(item["BizPoint"]),delta = 1000000)
                self.assertAlmostEqual(rateProfit,float(item["BizROIex"]),delta = 1000000)
                self.assertAlmostEqual(pointProfitCloseMean,float(item["BizAVGPoint"]),delta = 1000000)
                self.assertAlmostEqual(ordersCount,item["Orders"],delta = 1000000)
                self.assertAlmostEqual(tradePeriod,item["Weeks"],delta = 1000000)
        finally:
            table.reversesort = True
            print(table)

   
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

