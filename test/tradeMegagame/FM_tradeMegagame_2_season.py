#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getHomeHotTrader
# 用例标题: 获取首页的热门交易员信息
# 预置条件: 
# 测试步骤:
#   1.不登录的情况下获取首页热门交易员信息
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: shencanhui
# 写作日期: 20171211
#=========================================================
import sys,unittest,json,datetime
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeMegagame")
import Auth,FMCommon,Common,TradeMegagame
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
commonData = FMCommon.loadCommonYML()
tradeMegagameData = FMCommon.loadTradeMegagameYML()

class TradeMegagame(unittest.TestCase):
    def setUp(self):
        ##### 统计数据入参
        self.login = '2100000007'
        self.brokerID = 1
        ####统计粒度，天：t_ltl_daily，周：t_ltl_week，月：t_ltl_month，季度：t_ltl_season
        self.statistic_period = 't_ltl_daily'
        self.startTime = '2018-04-15 05:00:00.000'
        self.endTime = datetime.datetime.strptime(self.startTime,'%Y-%m-%d %H:00:00.000') + datetime.timedelta(days=1)
        self.statisticDate = self.startTime.split(' ')[0]
        # print("test info:  Account:",self.login,"brokerID:",self.brokerID,"startTime:",self.startTime,"self.endTime:",self.endTime)
        #sqlserver预期指标值
        quotas = [tradeMegagameData["profit_close"],tradeMegagameData["standard_lots"],
        tradeMegagameData["orders"],tradeMegagameData["follower_count"],tradeMegagameData["follow_actual_money"],
        tradeMegagameData["follow_service_charge"],tradeMegagameData["follow_money"],tradeMegagameData["follow_standard_lots"],
        tradeMegagameData["profit"],tradeMegagameData["aroi"]]
        # print(quotas)
        #计算指标
        self.quotaDict = {}
        for quota in quotas:
            # print(quota % (self.login,self.brokerID, self.startTime, self.endTime))
            profit_close = FMCommon.mssql_operaters(host=tradeMegagameData["mssql_host"],port=tradeMegagameData["mssql_port"],
                database=tradeMegagameData["mssql_V3_DB"],uid=tradeMegagameData["mssql_user"],
                pwd=tradeMegagameData["mssql_passwd"],sql=quota % (self.login, self.brokerID, self.startTime, self.endTime))
            for key in profit_close:
                # print(key,profit_close[key])
                self.quotaDict[key] = profit_close[key]
        # print(self.quotaDict)

        #获取mysql交易大赛账号表数据
        sql="""SELECT IFNULL(profit_close,0) AS profit_close,IFNULL(standard_lots,0) AS standard_lots,IFNULL(orders,0) AS orders,
            IFNULL(follower_count,0) AS follower_count,IFNULL(follow_service_charge,0) AS follow_service_charge,IFNULL(follow_actual_money,0) AS follow_actual_money,
            IFNULL(follow_money,0) AS follow_money,IFNULL(follow_standard_lots,0) AS follow_standard_lots,IFNULL(profit,0) AS profit,
            IFNULL(aroi,0) AS aroi from %s where account=%s and broker_id=%d and day = '%s'""" % (self.statistic_period,self.login, self.brokerID, self.statisticDate+' 00:00:00.000')
        self.mysqlMegagameDay = FMCommon.mysql_operaters(host=tradeMegagameData["mysql_host"], port=tradeMegagameData["mysql_port"], 
            user=tradeMegagameData["mysql_user"], passwd=tradeMegagameData["mysql_passwd"], db=tradeMegagameData["mysql_statistic_DB"],
            sql=sql)

    def test_1_TradeMegagame_profit_close(self):
        '''交易大赛天统计数据:盈亏金额(平仓总收益)'''
        # print(mysqlMegagameDay)
        # print(self.quotaDict["profit_close"], self.mysqlMegagameDay["profit_close"])
        self.assertEqual(self.quotaDict["profit_close"], self.mysqlMegagameDay["profit_close"])

    def test_2_TradeMegagame_standard_lots(self):
        '''交易大赛天统计数据:交易手数'''
        self.assertEqual(self.quotaDict["standard_lots"], self.mysqlMegagameDay["standard_lots"])

    def test_3_TradeMegagame_orders(self):
        '''交易大赛天统计数据:交易笔数'''
        self.assertEqual(self.quotaDict["orders"], self.mysqlMegagameDay["orders"])

    def test_4_TradeMegagame_follower_count(self):
        '''交易大赛天统计数据:实盘跟随人数'''
        self.assertEqual(self.quotaDict["follower_count"], self.mysqlMegagameDay["follower_count"])  #此记录会实施查询最新跟随者

    def test_5_TradeMegagame_follow_service_charge(self):
        '''交易大赛天统计数据:跟随服务费'''
        self.assertEqual(float(self.quotaDict["follow_service_charge"]), self.mysqlMegagameDay["follow_service_charge"])

    def test_6_TradeMegagame_follow_actual_money(self):
        '''交易大赛天统计数据:实盘跟随总收益'''
        self.assertAlmostEqual(self.quotaDict["follow_actual_money"], self.mysqlMegagameDay["follow_actual_money"],delta=0.1)

    def test_7_TradeMegagame_follow_money(self):
        '''交易大赛天统计数据:跟随总收益'''
        self.assertAlmostEqual(self.quotaDict["follow_money"], self.mysqlMegagameDay["follow_money"],delta=0.1)

    def test_8_TradeMegagame_follow_standard_lots(self):
        '''交易大赛天统计数据:跟随总手数'''
        self.assertAlmostEqual(self.quotaDict["follow_standard_lots"], self.mysqlMegagameDay["follow_standard_lots"],delta=0.002)

    def test_9_TradeMegagame_profit(self):
        '''交易大赛天统计数据:平，持仓盈亏金额'''
        self.assertEqual(self.quotaDict["profit"], self.mysqlMegagameDay["profit"])

    def test_10_TradeMegagame_aroi(self):
        '''交易大赛天统计数据:平，持仓累计资金收益率'''
        self.assertEqual(self.quotaDict["aroi"], self.mysqlMegagameDay["aroi"])

    def test_11_TradeMegagame_accountData(self):
        '''交易大赛帐号数据验证'''
        #获取sqlserver数据库数据
        mssqlMegagameAccount = FMCommon.mssql_operaters(host=tradeMegagameData["mssql_host"],port=tradeMegagameData["mssql_port"],
                database=tradeMegagameData["mssql_V3_DB"],uid=tradeMegagameData["mssql_user"],
                pwd=tradeMegagameData["mssql_passwd"],sql=tradeMegagameData["megagameAccount"] % (self.login, self.brokerID))
        # print(mssqlMegagameAccount)

        #获取mysql交易大赛账号表数据
        mysqlMegagameAccount = FMCommon.mysql_operaters(host=tradeMegagameData["mysql_host"], port=tradeMegagameData["mysql_port"], 
            user=tradeMegagameData["mysql_user"], passwd=tradeMegagameData["mysql_passwd"], db=tradeMegagameData["mysql_statistic_DB"],
            sql='SELECT * from t_ltl_account where account=%s and broker_id=%d' % (self.login, self.brokerID))
        # print(mysqlMegagameAccount)
        self.assertEqual(mssqlMegagameAccount["userid"], mysqlMegagameAccount["user_id"])
        self.assertEqual(mssqlMegagameAccount["nickName"], mysqlMegagameAccount["nickname"])
        self.assertEqual(mssqlMegagameAccount["realName"], mysqlMegagameAccount["real_name"])
        self.assertEqual(mssqlMegagameAccount["accountMobile"], mysqlMegagameAccount["mobile"])
        self.assertEqual(mssqlMegagameAccount["accountIndex"], mysqlMegagameAccount["account_index"])
        # self.assertEqual(mssqlMegagameAccount["equity"], mysqlMegagameAccount["equity"])

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

