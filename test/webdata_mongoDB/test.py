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
import sys,unittest,json,numpy,datetime,time
from dateutil.parser import parse #pip3 install python-dateutil
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,Account,Statistic,Trade
from Statistic import test_T_mt4trades,T_followorders,TD_followorders,test_T_mt4tradesinfo
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable
from pymongo import MongoClient
from pyhive import presto 
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
accountData = FMCommon.loadAccountYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()
tradeData = FMCommon.loadTradeYML()


class UserInfo(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        #生产 十年一剑1688
        self.login = '210062656'
        self.brokerID = 5
        curr_tiem = datetime.datetime.now() + datetime.timedelta(days=-1)
        self.yesterDay = curr_tiem.strftime('%Y-%m-%d 00:00:00.000')

        mongoDB = FMCommon.mongoDB_operater_data(host=statisticData["mongo_host"], port=statisticData["mongo_port"],)
        for i in mongoDB.fm.mg_test_result_all.find({"login":self.login}):
            self.mongoList = {}
            for key in statisticData["mongoKeyListAll"]:
                try:
                    value = i[key]
                    # print("88888888888888888")
                    # print(i,'>>>>>>>>>>>>>>>>>>',i[key])
                except KeyError:
                    value = statisticData["keyErr"]

                self.mongoList[key]=value
                # print(self.mongoList[key],value)
        params = {"time":7,"pageField":"Score","pageSort":"DESC"}
        self.rankTraders = Trade.getRankTraders(webAPIData['hostName_dev'] + tradeData['getRankTraders_url'],params=params,printLogs=1)
        self.assertEqual(self.rankTraders.status_code, webAPIData['status_code_200']) 
        # key = []
        #遍历items里面所有的数据
        for i in json.loads(self.rankTraders.text)["data"]["items"]:
            # 遍历items里面所有的key，value
            if i["NickName"] =="萬丈豪情":