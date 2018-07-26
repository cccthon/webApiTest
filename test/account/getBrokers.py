#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: Account - getBrokers
# 用例标题: 获取经纪商列表
# 预置条件: 
# 测试步骤:
#   1.获取经纪商列表
# 预期结果:
#   1.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20180308
#=========================================================
import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/statistic")

import Auth,FMCommon,Common,FollowManage,Statistic,Account
from socketIO_client import SocketIO
from base64 import b64encode


webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
followData = FMCommon.loadFollowYML()
commonData = FMCommon.loadCommonYML()
statisticData = FMCommon.loadStatisticYML()
accountData = FMCommon.loadAccountYML()
userData = FMCommon.loadWebAPIYML()


class getBrokers(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
       
    def test_1_getBrokers_FM(self):
        brokers = Account.getBrokers(webAPIData['hostName'] + accountData['getBrokers_url'],printLogs=0)
        self.assertEqual(brokers.status_code,webAPIData['status_code_200'])
        '''获取FM的经纪商列表'''
        brokerList = []
        #遍历返回来的json的brokers数据
        for item in json.loads(brokers.text)["data"]["brokers"]:
            brokerList.append(item["Broker"])
        brokerList.sort()
        brokerbrokertable = ['KVB', 'FXCM']
        brokerbrokertable.sort()
        self.assertListEqual(brokerList,brokerbrokertable)

    def test_2_getBrokers_all(self):
        '''获取所有的经纪商列表'''
        brokers = Account.getBrokers(webAPIData['hostName'] + accountData['getBrokers_url'],params="category=all",printLogs=0)
        self.assertEqual(brokers.status_code,webAPIData['status_code_200'])
        brokerList = []
        for item in json.loads(brokers.text)["data"]["brokers"]:
            brokerList.append(item["Broker"])
        print(brokerList)
        brokerList.sort()
        brokerbrokertable = ['', '','RH', 'RiseHill', 'Demo', 'FXCM', 'KVB', 'KVBmini', 'FxPro', 
        'FxPro-SAM', 'Axi-SAM', 'ADS-SAM', 'GKFX-SAM', 'STA-SAM', 'Ava-SAM', 'FOREX-SAM', 'GoMarkets-SAM', 'Pepperstone-SAM', 'ThinkForexAU-SAM', 'IFMTrade-SAM', 'ICMarkets-SAM', 'Alpari-SAM', 'ExnessCY-SAM', 'EasyForex-SAM','AETOS-SAM']
        brokerbrokertable.sort()
        self.assertListEqual(brokerList,brokerbrokertable)

    def test_3_getBrokers_available(self):
        '''获取有效的经纪商列表'''
        params = {"category ":"available"}
        brokers = Account.getBrokers(webAPIData['hostName'] + accountData['getBrokers_url'],params="category=available",printLogs=0)
        self.assertEqual(brokers.status_code,webAPIData['status_code_200'])
        brokerList = []
        for item in json.loads(brokers.text)["data"]["brokers"]:
            brokerList.append(item["Broker"])
        print(brokerList)
        brokerList.sort()
        brokertable = ['ADS-SAM','Alpari-SAM','Ava-SAM','Axi-SAM','EasyForex-SAM','ExnessCY-SAM','FOREX-SAM','FXCM','FxPro-SAM',
        'GKFX-SAM','GoMarkets-SAM','ICMarkets-SAM','IFMTrade-SAM','KVB','Pepperstone-SAM','STA-SAM','ThinkForexAU-SAM','AETOS-SAM']
        brokertable.sort()
        self.assertListEqual(brokerList,brokertable)

    def test_4_getBrokers_sam(self):
        '''获取sam经纪商列表'''
        brokers = Account.getBrokers(webAPIData['hostName'] + accountData['getBrokers_url'],params="category=sam",printLogs=0)
        self.assertEqual(brokers.status_code,webAPIData['status_code_200'])
        brokerList = []
        for item in json.loads(brokers.text)["data"]["brokers"]:
            brokerList.append(item["Broker"])
        print(brokerList)
        brokerList.sort()
        brokertable = ['ADS-SAM','Alpari-SAM','Ava-SAM','Axi-SAM','EasyForex-SAM','ExnessCY-SAM','FOREX-SAM','FxPro-SAM', 
        'GKFX-SAM','GoMarkets-SAM','ICMarkets-SAM','IFMTrade-SAM','STA-SAM','Pepperstone-SAM','ThinkForexAU-SAM','AETOS-SAM']
        # ['ADS-SAM','Alpari-SAM','Ava-SAM','Axi-SAM','EasyForex-SAM','ExnessCY-SAM','FOREX-SAM','FXCM','FxPro','FxPro-SAM',
        # 'GKFX-SAM','GoMarkets-SAM','ICMarkets-SAM','IFMTrade-SAM','KVB','Pepperstone-SAM','RH','STA-SAM','ThinkForexAU-SAM']
        brokertable.sort()
        self.assertListEqual(brokerList,brokertable)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

