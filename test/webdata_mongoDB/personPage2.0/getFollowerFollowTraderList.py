#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getFollowerFollowTraderList
# 用例标题: 获取跟随者的跟随收益图表数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
#   1.获取跟随者的跟随收益图表数据对比MongoDB数据
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180517
#=========================================================
import sys,unittest,json
import time,os
import datetime
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,Statistic,Follow,Datastatistic
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable
from pymongo import MongoClient

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()
followData = FMCommon.loadFollowYML()
datastatisticData = FMCommon.loadDatastatisticYML()

class FollowerFollowTraderList(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # 入参
        self.userID = '18907'
        self.AccountIndex = 2
        #获取MT4账号
        self.mt4Account = Statistic.getMt4Account(userID=str(self.userID),accountIndex=str(self.AccountIndex))

        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        self.mongoDB = FMCommon.mongoDB_operater_data(host=mongoUrl, port = statisticData["mongo_port"])

        followerFollowTrader = Datastatistic.getFollowerFollowTraderList(webAPIData['hostName'] + datastatisticData['getFollowerFollowTraderList_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + datastatisticData["getFollowerFollowTraderList_url2"],printLogs=0)
        # self.assertEqual(followerFollowTrader.status_code, webAPIData['status_code_200'])
        
        for self.item in json.loads(followerFollowTrader.text)["data"]["List"]:

            for i in self.mongoDB.datastatistic.mg_result_follall.find({"login":str(self.mt4Account),"masteraccount":str(self.item["Account"])}):
                self.mongoList = {}
                for key in statisticData["mongoKeyListAll"]:
                    try:
                        value = i[key]
                    except KeyError:
                        value = statisticData["keyErr"]
                    self.mongoList[key]=value

            table= PrettyTable(["预期/实际","NickName","mt4Account","BrokerID","跟随收益","跟随手数"])
            
            try:
                table.add_row(["预期结果",self.item["NickName"],self.item["Account"],self.item["BrokerID"],self.mongoList["money_close"],self.mongoList["standardlots_close"]])
                table.add_row(["实际结果",self.item["NickName"],self.item["Account"],self.item["BrokerID"],self.item["FollowMoney"],self.item["FollowStandardLots"]])
                table.add_row(["","","","","",""])
                       
            finally:
                table.reversesort = True
                print(table)
    

    def test_1_FollowMoney(self):           
        #跟随收益
        self.assertAlmostEqual(self.mongoList["money_close"],float(self.item["FollowMoney"]),delta = 0.01)

    def test_2_FollowStandardLots(self): 
        #跟随手数
        self.assertAlmostEqual(self.mongoList["standardlots_close"],float(self.item["FollowStandardLots"]),delta = 0.01)
    
    
    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

