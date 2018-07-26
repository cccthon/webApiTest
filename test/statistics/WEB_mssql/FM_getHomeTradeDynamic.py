#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getHomeTradeDynamic
# 用例标题: 获取首页交易动态信息
# 预置条件: 
# 测试步骤:
#   1.不登录的情况下获取首页交易动态信息
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

class TradeDynamic(unittest.TestCase):
    def setUp(self):
        '''登录followme系统'''
        pass

    def test_tradeDynamic(self):
        '''获取首页交易动态信息'''
        tradeDynamic = Common.getHomeTradeDynamic(webAPIData['hostName'] + commonData['getHomeTradeDynamic_url'],printLogs=1)
        self.assertEqual(tradeDynamic.status_code, webAPIData['status_code_200'])
        print("tradeDynamic:")
        table = PrettyTable(["NickName","UserID","MT4account","AccountIndex","SYMBOL","cmd","StandardLots","OpenPrice","ClosePrice","Profit"])
        for item in json.loads(tradeDynamic.text)["data"]["Items"]:
            table.add_row([item["NickName"],item["id"],item["LOGIN"],item["AccountCurrentIndex"],item["SYMBOL"],item["CMD"],item["StandardLots"],item["BizShowPRICE"],item["CLOSE_PRICE"],item["Profit"]])
        table.reversesort = True
        print(table)

    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

