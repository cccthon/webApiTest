#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getStatisticsOfAccount
# 用例标题: 获取交易员个人展示页2.1顶部数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
#   1.获取个人展示页2.1顶部数据对比MongoDB数据
# 1.1 交易能力值（score） 1.2 收益率  1.3 跟随获利总额  1.4 正在跟随总额
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180719
#=========================================================
import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,Statistic,Follow
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable
from pymongo import MongoClient

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()
followData = FMCommon.loadFollowYML()

class StatisticsOfAccount(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #入参
        self.userID = '132316'
        self.AccountIndex = 4
        #获取MT4账号
        self.mt4Account = Statistic.getMt4Account(userID=str(self.userID),accountIndex=str(self.AccountIndex))
        print(self.mt4Account)
        '''获取个人展示页的交易概览数据'''
        statisticsOfAccount = Follow.getStatisticsOfAccount(webAPIData['hostName'] + followData['getStatisticsOfAccount_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + followData["getStatisticsOfAccount_url1"],printLogs=1)
        # self.assertEqual(statisticsOfAccount.status_code, webAPIData['status_code_200'])
        self.item = json.loads(statisticsOfAccount.text)["data"]
        

        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        mongoDB = FMCommon.mongoDB_operater_data(host=mongoUrl, port = statisticData["mongo_port"])
        for i in mongoDB.datastatistic.mg_result_all.find({"login":str(self.mt4Account)}):
            self.mongoList = {}
            for key in statisticData["mongoKeyListAll"]:
                try:
                    value = i[key]
                except KeyError:
                    value = statisticData["keyErr"]
                self.mongoList[key]=value

        
        table_1 = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","交易能力值（score）","收益率","跟随获利总额","正在跟随总额"])
                
        try:
            
            table_1.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,self.mongoList["score"],self.mongoList["rate_ss_profit_balance_close"],self.mongoList["money_followed_close"],self.mongoList["report_followersbalance_demo_following"]+self.mongoList["report_followersbalance_actual_following"]])
            table_1.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,self.item["Score"],self.item["Roi"],self.item["FollowProfitMoney"],self.item["FollowTotalMoney"]])
            table_1.add_row(["","","","","","","",""])
                
        finally:
            table_1.reversesort = True
            print(table_1)


    def setUp(self):
        pass

    def test_1_ProfitOrders(self):         
        #交易能力值（score）
        self.assertAlmostEqual(self.mongoList["score"],float(self.item["Score"]),delta = 0.01)

    def test_2_AvgProfitMoney(self): 
        #收益率
        self.assertAlmostEqual(self.mongoList["rate_ss_profit_balance_close"],self.item["Roi"],delta = 0.01)
    
    def test_3_MaxLossPips(self):     
        #跟随获利总额
        self.assertAlmostEqual(self.mongoList["money_followed_close"],float(self.item["FollowProfitMoney"]),delta = 0.01)

    def test_4_Pips(self):
        #正在跟随总额
        self.assertAlmostEqual(self.mongoList["report_followersbalance_demo_following"]+self.mongoList["report_followersbalance_actual_following"],float(self.item["FollowTotalMoney"]),delta = 0.01)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

