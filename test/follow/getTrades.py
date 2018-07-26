#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: Follow - getTraders
# 用例标题: 获取交易员列表
# 预置条件: 
# 测试步骤:
#   1.获取交易员列表
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180307
#=========================================================
import sys,unittest,json
# sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")
import Auth,FMCommon,Common,FollowManage,Statistic
from socketIO_client import SocketIO
from base64 import b64encode
from prettytable import PrettyTable
import io 
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码 

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
followData = FMCommon.loadFollowYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()

class ChoiceTrades(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        params = {"time":0,"pageField":"Score","pageSort":"DESC"}
        self.trades = FollowManage.getRankTraders(webAPIData['hostName'] + followData['getRankTraders_url'],params=params,printLogs=0)
        self.assertEqual(self.trades.status_code, webAPIData['status_code_200']) 
               
    def test_1_getChoiceTrades_checkscore(self):
        '''判断新增字段score是否存在'''
        key = []
        #遍历items里面所有的数据
        for i in json.loads(self.trades.text)["data"]["items"]:
            # 遍历items里面所有的key，value
            for k,v in i.items():
                #往key空列表里面增加key值
                key.append(k)
        #判断Score是否在KEY值里面
        self.assertIn("Score",key)
    
    def test_2_getChoiceTrades_checkscore(self):
        '''判断净利润因子是否都大于1.2'''
        #遍历items里面所有的数据 
        for i in json.loads(self.trades.text)["data"]["items"]:
            print(i["FactorProfitEquity"])

            self.assertGreater(i["FactorProfitEquity"], 1.2)

    def test_3_getChoiceTrades_checkscore(self):
        '''判断新增字段score是否倒序排序'''
        scoreList = []
        #遍历items里面所有的数据
        for i in json.loads(self.trades.text)["data"]["items"]:
            scoreList.append(i["Score"])

        j=0
        for scoreList[j] in scoreList:
            self.assertGreaterEqual(scoreList[j],scoreList[j+1])
            j=j+1
            if j == (len(scoreList))-1:
                break

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

