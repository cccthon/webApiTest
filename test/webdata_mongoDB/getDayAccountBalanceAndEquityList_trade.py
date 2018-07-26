#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getDayAccountBalanceAndEquityList

# 用例标题: 获取交易员净值余额图表数据对比MongoDB数据
# 预置条件: 
# 测试步骤:
#   1.获取交易员净值余额图表数据对比MongoDB数据
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180516
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

class DayAccountBalanceAndEquityList(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #入参
        self.userID = '132316'
        self.AccountIndex = 4

        mongoUrl = "mongodb://%s:%s@%s" % (statisticData["mongo_userName"], statisticData["mongo_passwd"], statisticData["mongo_host"])
        mongoDB = FMCommon.mongoDB_operater_data(host=mongoUrl, port = statisticData["mongo_port"])

        #获取MT4账号
        self.mt4Account = Statistic.getMt4Account(userID=str(self.userID),accountIndex=str(self.AccountIndex))
        '''获取个人展示页的净值余额图表数据'''
        balanceAndEquity = Datastatistic.getDayAccountBalanceAndEquityList(webAPIData['hostName'] + datastatisticData['getDayAccountBalanceAndEquityList_url'] + str(self.userID) + "_"+ str(self.AccountIndex) + datastatisticData["getDayAccountBalanceAndEquityList_url2"],printLogs=1)
        
        # self.assertEqual(balanceAndEquity.status_code, webAPIData['status_code_200'])

        self.monthList = []
        self.buyStandardLotsList = []
        self.sellStandardLotsList = []
        self.pipsList = []
        for self.item in json.loads(balanceAndEquity.text)["data"]["MonthDataList"]:
            self.monthList.append(self.item["Month"])
            self.buyStandardLotsList.append(self.item["BuyStandardLots"])
            self.sellStandardLotsList.append(self.item["SellStandardLots"])
            self.pipsList.append(self.item["Pips"])
            monthStamp = int(self.item["Month"])
            monthArray = time.localtime(monthStamp)
            otherStyleMonth = time.strftime("%Y-%m", monthArray)

            for i in mongoDB.datastatistic.mg_result_month.find({"login":str(self.mt4Account),"close_month":str(otherStyleMonth)}):
                self.mongoList_month = {}
                for key in statisticData["mongoKeyListAll"]:
                    try:
                        value = i[key]
                    except KeyError:
                        value = statisticData["keyErr"]
                    self.mongoList_month[key]=value

            table = PrettyTable(["预期/实际","UserID","AccountIndex","MT4Account","月份","做多手数","做空手数","盈亏点数"])

            try:
                table.add_row(["预期结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleMonth,self.mongoList_month["standardlots_long_close"],self.mongoList_month["standardlots_short_close"],self.mongoList_month["point_loss_close"]+self.mongoList_month["point_profit_close"]])
                table.add_row(["实际结果",self.userID,self.AccountIndex,self.mt4Account,otherStyleMonth,self.item["BuyStandardLots"],self.item["SellStandardLots"],self.item["Pips"]])
                table.add_row(["","","","","","","",""])
                
            finally:
                table.reversesort = True
                print(table)
         
        
    
    def test_3_BuyStandardLots(self):     
        #做多手数
        self.assertAlmostEqual(self.mongoList_month["standardlots_long_close"],float(self.item["BuyStandardLots"]),delta = 0.01)

    def test_4_SellStandardLots(self):
        #做空手数
        self.assertAlmostEqual(self.mongoList_month["standardlots_short_close"],float(self.item["SellStandardLots"]),delta = 0.01)

    def test_5_Pips(self):
        #盈亏点数
        self.assertAlmostEqual(self.mongoList_month["point_loss_close"] + self.mongoList_month["point_profit_close"],float(self.item["Pips"]),delta = 0.01)
    

    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

