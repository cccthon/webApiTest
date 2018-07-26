#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getAccountRoi
# 用例标题: 获取跟随者收益率图表数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
#   1.获取收益率图表数据对比MongoDB数据
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180515
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

class AccountRoi(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #入参
        self.userID = '140130'
        self.AccountIndex = 4

        # mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        mongoUrl = "mongodb://%s:%s@%s" % (statisticData.mongo_userName, statisticData.mongo_passwd, statisticData.mongo_host)
        mongoDB = FMCommon.mongoDB_operater_data(host=mongoUrl, port = statisticData.mongo_port)
        
        #获取MT4账号
        self.mt4Account = Statistic.getMt4Account(userID=str(self.userID),accountIndex=str(self.AccountIndex))
        print(self.mt4Account)
        '''获取个人展示页的收益率图表数据'''
        accountRoi = Datastatistic.getAccountRoi(webAPIData.hostName + datastatisticData.getAccountRoi_url + str(self.userID) + "_"+ str(self.AccountIndex) + datastatisticData.getAccountRoi_url2,printLogs=1)
        
        # self.assertEqual(accountRoi.status_code, webAPIData['status_code_200'])
        '''获取FM的经纪商列表'''
        self.roiList = []
        self.dateList = []
        self.selfRoiList = []
        self.followRoiList = []
        # for self.item in json.loads(accountRoi.text)["data"]["RoiList"]:
        for self.item in json.loads(accountRoi.text)["data"]["RoiList"]:
            self.roiList.append(self.item["Roi"])
            print(self.roiList[0])
            self.dateList.append(self.item["Date"])
            self.selfRoiList.append(self.item["SelfRoi"])
            self.followRoiList.append(self.item["FollowRoi"])
            timeStamp = int(self.item["Date"])
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)

            for i in mongoDB.datastatistic_1_16.mg_result_day.find({"login":str(self.mt4Account),"close_date":str(otherStyleTime)}):
                self.mongoList = {}
                for key in statisticData["mongoKeyListAll"]:
                    try:
                        value = i[key]
                    except KeyError:
                        value = statisticData["keyErr"]
                    self.mongoList[key]=value
            table = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","平仓时间","收益率","自主收益率","跟随收益率"])

            try:
                table.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleTime,self.mongoList["rate_asumasum_profit_balance_close"],self.mongoList["rate_asumasum_profit_balance_close_self"],self.mongoList["rate_asumasum_profit_balance_close_follow"]])
                table.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleTime,self.item["Roi"],self.item["SelfRoi"],self.item["FollowRoi"]])
                table.add_row(["","","","","","","",""])
                
            finally:
                table.reversesort = True
                print(table)

    def test_1_ProfitOrders(self):           
        #收益率
        self.assertAlmostEqual(self.mongoList["rate_asumasum_profit_balance_close"],float(self.item["Roi"]),delta = 0.01)

    def test_2_ProfitOrders(self):           
        #自主收益率
        self.assertAlmostEqual(self.mongoList["rate_asumasum_profit_balance_close_self"],float(self.item["SelfRoi"]),delta = 0.01)

    def test_3_ProfitOrders(self):           
        #跟随收益率
        self.assertAlmostEqual(self.mongoList["rate_asumasum_profit_balance_close_follow"],float(self.item["FollowRoi"]),delta = 0.01)
    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

