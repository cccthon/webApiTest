#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_WebAPI_RiskControl_getRiskControl_001_001
# 用例标题: 获取跟随者风控全局设置
# 预置条件: 
# 测试步骤:
#   1.调用接口：getRiskControl,请求url，header发起get请求
# 预期结果:
#   1.风控设置返回成功
#   2.检查响应码为：200
# 脚本作者: shencanhui
# 写作日期: 20171113
#=========================================================
import sys,unittest,json,requests,pymysql
sys.path.append("../../lib/common")
import FMCommon
tradeMegagameData = FMCommon.loadTradeMegagameYML()


class testmysql(unittest.TestCase):
    def setUp(self):
        pass

    # def test_1_mysql(self):
    #     """test mysql"""
    #     sql = 'select * from T_Users limit 1'
    #     # sql = "update T_Users set CreateTime='2017-11-21 21:21:59.000' where UserID=148174 and BrokerID=5"
    #     mysql = FMCommon.mysql_operaters(host='119.23.168.162', port=53326, user='betareader', passwd='V6Wq8Z4mxihz', db='CopyTrading',sql=sql)
    #     #返回sql语句查询结果
    #     print(mysql)
    #     print(">>>>>>>>>>>>>>>>>>>>>")
    #     #通过key查询指定字段的值
    #     print(mysql['ID'])

    # def test_2_mssql(self):
    #     """test mssql"""
    #     print("test mssql >>>>>>>>>>>>>>>>>>")
    #     sql = "select * from t_useraccount where mt4account='2100000007'"
    #     mssql = FMCommon.mssql_operater(host='119.23.168.162',port=52436,
    #         database='FM_OS_V3', uid='chenyangyang',
    #         pwd='fmW3gxCDATWF',sql=sql)
    #     print(mssql)

    def test_des_ecrypt(self):
        ecryptText = '13794829675:Mozilla/5.0 (Windows NT 10.0; Win64; x64; ServiceUI 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'  # 待加密文本
        desKey = "12345678" # Key
        ecrypt = FMCommon.des_ecrypt(ecryptText=ecryptText,desKey=desKey)
        print(ecrypt)


    def tearDown(self):
        #清空测试环境，还原测试数据
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()

