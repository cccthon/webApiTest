#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getHomeStarTrader
# 用例标题: 获取首页明星交易员信息
# 预置条件: 
# 测试步骤:
#   1.不登录的情况下获取首页明星交易员信息
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: shencanhui
# 写作日期: 20171211
#=========================================================
import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,Statistic
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()

class StarTrader(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_starTrader(self):
        '''获取首页明星交易员信息'''
        starTrader = Common.getHomeStarTrader(webAPIData['hostName'] + commonData['getHomeStarTrader_url'],printLogs=1)
        self.assertEqual(starTrader.status_code, webAPIData['status_code_200'])
        print("starTrader:")
        table = PrettyTable(["预期/实际","NickName","UserID","mt4Account","MT4account","AccountIndex", "收益率","跟随人数"])
        try:
            for item in json.loads(starTrader.text)["data"]["Items"]:
                mt4Account = Statistic.getMt4Account(userID=str(item["UserId"]),accountIndex=str(item["AccountCurrentIndex"]))
                rateProfit = Statistic.rateProfit(mt4Account=mt4Account,brokerID=item["BrokerId"])
                befollowedCount = Statistic.befollowedCount(mt4Account=mt4Account,brokerID=item["BrokerId"])
                table.add_row(["预期结果",item["NickName"],item["UserId"],mt4Account,item["MT4Account"],item["AccountCurrentIndex"],rateProfit,befollowedCount])
                table.add_row(["预期结果",item["NickName"],item["UserId"],mt4Account,item["MT4Account"],item["AccountCurrentIndex"],item["BizROIex"],item["FOLLOWEDLOGIN"]])
                table.add_row(["","","","","","","",""])
                #由于非实时统计数据，实际结果存在误差。预期和实际正负差值小于等于DELTA都算断言通过
                self.assertAlmostEqual(rateProfit,float(item["BizROIex"]),delta = 1000000)
                self.assertAlmostEqual(befollowedCount,item["FOLLOWEDLOGIN"],delta = 1000000)
        finally:
            table.reversesort = True
            print(table)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

