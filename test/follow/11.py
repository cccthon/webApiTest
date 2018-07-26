# -*-coding:utf-8-*- 
#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_followMulti_pcio
# 用例标题: 交易大赛（需要登录） 
# 预置条件: 
# 测试步骤:
#   1.
# 预期结果:
#   1.风控设置返回成功
#   2.检查响应码为：200
# 脚本作者: zhangyanyun
# 写作日期: 20171213
#=========================================================
import sys,unittest,json,requests,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/tradeOnline")
import FMCommon,Auth,RiskControl,Follow,FollowManage,TradeOnline,Account,Order,Social
from socketIO_client import SocketIO
from base64 import b64encode

tradeOnlineData = FMCommon.loadTradeOnlineYML()
webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
riskControlData = FMCommon.loadRiskControlYML()
followData = FMCommon.loadFollowYML()
orderData = FMCommon.loadOrderYML()
accountData = FMCommon.loadAccountYML()

class FollowMulti_pcio(unittest.TestCase):
    def setUp(self):
        #交易员FMS004 晋峰登陆---------------------
        tradeDatas = {"account":webAPIData['account_1'], "password":webAPIData['passwd_1'], "remember":"false"}
        tradeSignin = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], tradeDatas)
        # 登录成功，返回200 ok
        self.assertEqual(tradeSignin.status_code, webAPIData['status_code_200'])
        #保存账号的nickName,待获取userID使用
        self.tradeNickName = json.loads(tradeSignin.text)['data']['nickname']
        # #保存登录时的token，待登出使用
        self.tradeUserToken = json.loads(tradeSignin.text)['data']['token']
        #保存userID
        self.tradeUserID = json.loads(tradeSignin.text)['data']['id']
        #规整headers
        self.tradeHeaders = dict(webAPIData['headers'], **{webAPIData['Authorization'] : webAPIData['Bearer'] + self.tradeUserToken})
        #获取所有账户信息
        self.getAccount = Account.getAccounts(webAPIData['hostName'] + accountData['getAccounts_url'] + accountData['getAccounts_url2'],headers = self.tradeHeaders,interfaceName='getAccount')
        #获取指定经纪商的accountIndex。当前为：pcio
        self.tradeAccountIndex_Pico = Account.getSpecialAccountIndex(headers = self.tradeHeaders, brokerID=1)
        self.switchTradeAccount_Pico = Account.switchAccount(webAPIData['hostName'] + accountData['switchAccount'], self.tradeHeaders, index=self.tradeAccountIndex_Pico)
        # 账号切换成功
        self.assertEqual(self.switchTradeAccount_Pico.status_code, webAPIData['status_code_200'])
        # 获取交易员交易token
        self.tradeToken_Pico = Account.getToken(self.tradeHeaders, onlyTokn="true", printLogs=1)


        #交易员FMSOO4 福汇登陆---------------------
        tradeDatas = {"account":webAPIData['account'], "password":webAPIData['passwd'], "remember":"false"}
        tradeSignin = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], tradeDatas)
        print(tradeSignin)
        #登录成功，返回200 ok
        self.assertEqual(tradeSignin.status_code, webAPIData['status_code_200'])
        #保存账号的nickName,待获取userID使用
        self.tradeNickName = json.loads(tradeSignin.text)['data']['nickname']
        # #保存登录时的token，待登出使用
        self.tradeUserToken = json.loads(tradeSignin.text)['data']['token']
        #保存userID
        self.tradeUserID = json.loads(tradeSignin.text)['data']['id']
        #规整headers
        self.tradeHeaders = dict(webAPIData['headers'], **{webAPIData['Authorization'] : webAPIData['Bearer'] + self.tradeUserToken})
        #获取指定经纪商的accountIndex。当前为：FXCM
        self.tradeccountIndex_FXCM = Account.getSpecialAccountIndex(headers = self.tradeHeaders, brokerID=4)
        self.getAccountindex_FXCM = Account.getAccount(webAPIData['hostName'] + accountData['getAccounts_url'],headers = self.tradeHeaders)
        self.switchTradeAccount_FXCM = Account.switchAccount(webAPIData['hostName'] + accountData['switchAccount'], self.tradeHeaders, index= self.tradeAccountIndex_FXCM)
        # 账号切换成功
        self.assertEqual(self.switchTradeAccount_FXCM.status_code, webAPIData['status_code_200'])
        # 获取交易员交易token
        self.tradeToken_FXCM = Account.getToken(self.tradeHeaders, onlyTokn="true", printLogs=1)
        print(self.tradeToken_FXCM)
        self.tradeIndex_FXCM = str(self.tradeUserID) + '_' + self.tradeAccountIndex_FXCM


    #交易员FMSOO4 KVB登陆---------------------
        tradeDatas = {"account":webAPIData['account'], "password":webAPIData['passwd'], "remember":"false"}
        tradeSignin = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], tradeDatas)
        print(tradeSignin)
        #登录成功，返回200 ok
        self.assertEqual(tradeSignin.status_code, webAPIData['status_code_200'])
        #保存账号的nickName,待获取userID使用
        self.tradeNickName = json.loads(tradeSignin.text)['data']['nickname']
        # #保存登录时的token，待登出使用
        self.tradeUserToken = json.loads(tradeSignin.text)['data']['token']
        #保存userID
        self.tradeUserID = json.loads(tradeSignin.text)['data']['id']
        #规整headers
        self.tradeHeaders = dict(webAPIData['headers'], **{webAPIData['Authorization'] : webAPIData['Bearer'] + self.tradeUserToken})
        #获取指定经纪商的accountIndex。当前为：FXCM
        self.tradeccountIndex_KVB = Account.getSpecialAccountIndex(headers = self.tradeHeaders, brokerID=5)
        self.getAccountindex_KVB = Account.getAccount(webAPIData['hostName'] + accountData['getAccounts_url'],headers = self.tradeHeaders)
        self.switchTradeAccount_KVB = Account.switchAccount(webAPIData['hostName'] + accountData['switchAccount'], self.tradeHeaders, index= self.tradeAccountIndex_FXCM)
        # 账号切换成功
        self.assertEqual(self.switchTradeAccount_KVB.status_code, webAPIData['status_code_200'])
        # 获取交易员交易token
        self.tradeToken_KVB = Account.getToken(self.tradeHeaders, onlyTokn="true", printLogs=1)
        print(self.tradeToken_KVB)
        self.tradeIndex_KVB = str(self.tradeUserID) + '_' + self.tradeAccountIndex_KVB

    def test_1_getChoiceTrades_checkscore(self):
        #展示账号所有的交易员
        target=[]
        data = json.loads(self.getAccount.text)["data"]["accounts"]
        print('输出源数据：')
        for  i in data:          
            if i['UserType'] == 1:
                temp = {'UserType':i['UserType'],'MT4Account':i['MT4Account'] , 'BrokerName':i['BrokerName'] }
                print(temp)
                target.append(temp)
                # target.extend(temp)
        print('下面是输出结果：')                                      
        print(target)

        MT4AccountList=[]
        BrokerNameList=[]
        for item in target:
            MT4AccountList.append(item["MT4Account"])
            BrokerNameList.append(item["BrokerName"])
        MT4AccountList.sort()
        BrokerNameList.sort()

        MT4Account = ['2100000004', '79904', '9907813','996394','']
        BrokerName = [ 'RH晋峰环球国际','KVB昆仑国际','KVB昆仑国际','FXCM福汇英国','KVB昆仑国际']
        MT4Account.sort()
        BrokerName.sort()
        self.assertListEqual(MT4AccountList,MT4Account)
        self.assertListEqual(BrokerNameList,BrokerName)

    def test_2_getChoiceTrades_checkscore(self):
        #同个账号的第一个账户参加交易大赛，可以参加
        params = {"category ":"all","time":0}
        self.trades = FollowManage.getTraders(webAPIData['hostName'] + followData['getTraders_url'],params=params,printLogs=1)
        self.assertEqual(self.trades.status_code, webAPIData['status_code_200'])

    def test_2_getChoiceTrades_checkscore(self):
        #同个账号的第二个账户参加交易大赛，可以参加
        params = {"category ":"all","time":0}
        self.trades = FollowManage.getTraders(webAPIData['hostName'] + followData['getTraders_url'],params=params,printLogs=1)
        self.assertEqual(self.trades.status_code, webAPIData['status_code_200'])

    def test_2_getChoiceTrades_checkscore(self):
        #同个账号的第三个账户参加交易大赛，不可以参加
        params = {"category ":"all","time":0}
        self.trades = FollowManage.getTraders(webAPIData['hostName'] + followData['getTraders_url'],params=params,printLogs=1)
        self.assertEqual(self.trades.status_code, webAPIData['status_code_200'])





    def test_1_getChoiceTrades_checkscore(self):
        #展示账号所有的交易员
        target=[]
        data = json.loads(self.getAccount.text)["data"]["accounts"]
        print('输出源数据：')
        for  i in data:          
            if i['UserType'] == 1:
                temp = {'UserType':i['UserType'],'MT4Account':i['MT4Account'] , 'BrokerName':i['BrokerName'] }
                print(temp)
                target.append(temp)
                # target.extend(temp)
        print('下面是输出结果：')                                      
        print(target)

        MT4AccountList=[]
        BrokerNameList=[]
        for item in target:
            MT4AccountList.append(item["MT4Account"])
            BrokerNameList.append(item["BrokerName"])
        MT4AccountList.sort()
        BrokerNameList.sort()

        MT4Account = ['2100000004', '79904', '9907813','996394','']
        BrokerName = [ 'RH晋峰环球国际','KVB昆仑国际','KVB昆仑国际','FXCM福汇英国','KVB昆仑国际']
        MT4Account.sort()
        BrokerName.sort()
        self.assertListEqual(MT4AccountList,MT4Account)
        self.assertListEqual(BrokerNameList,BrokerName)

    def test_2_getChoiceTrades_checkscore(self):
        #同个账号的晋峰
        target=[]
        data = json.loads(self.getAccount.text)["data"]["accounts"]
        print('输出源数据：')
        for  i in data:          
            if i['UserType'] == 1:
                temp = {'UserType':i['UserType'],'MT4Account':i['MT4Account'] , 'BrokerName':i['BrokerName'] }
                print(temp)
                target.append(temp)
                # target.extend(temp)
        print('下面是输出结果：')                                      
        print(target)

        MT4AccountList=[]
        BrokerNameList=[]
        for item in target:
            MT4AccountList.append(item["MT4Account"])
            BrokerNameList.append(item["BrokerName"])
        MT4AccountList.sort()
        BrokerNameList.sort()

        MT4Account = ['2100000004', '79904', '9907813','996394','']
        BrokerName = [ 'RH晋峰环球国际','KVB昆仑国际','KVB昆仑国际','FXCM福汇英国','KVB昆仑国际']
        MT4Account.sort()
        BrokerName.sort()
        self.assertListEqual(MT4AccountList,MT4Account)
        self.assertListEqual(BrokerNameList,BrokerName)




    #     #大赛排行
    #     #总榜：只显示前10名，排序默认以收益率从高到低为准，只显示十个，字段：排名，昵称，账户，收益率，收益
        
    # def test_1_getGeneralList_field(self):
    #     '''判断新增字段排名，昵称，账户，收益率，收益是否存在'''
    #     generalList = []
    #     #遍历i里面所有的数据
    #     for i in json.loads(self.榜单接口返回内容.text)["data"]["items"]:
    #         #遍历items里面所有的key，value
    #         for k,v in i.items():
    #             #往key空列表里面增加key值
    #             generalList.append(k)
    #     generalList.sort()
    #     table = ['排名', '昵称', '账户','收益率','收益']
    #     table.sort()
    #     self.assertListEqual(generalList,table)

    # def test_2_getGenerallist_number(self):
    #     generallist_number = []
    #     for i in json.loads(self.榜单接口返回内容.text)["data"]["items"]:
    #         generallist_number.append(i["排名"])
    #     self.assertGreater(len(i["排名"]), 10)

    # def test_3_getGenerallist_Roisort(self):
    #     generallist_Roisort = []
    #     for i in json.loads(self.榜单接口返回内容.text)["data"]["items"]:
    #         generallist_Roisort.append(i["Roi"])
    #     j=10
    #     for j in generallist_Roisort:
    #         self.assertLessEqual(generallist_Roisort[j], generallist_Roisort[j-1])
    #         j=j-1


    # # 月榜：只显示当月前10名，排序默认以收益率从高到低为准，只显示十个，字段：排名，昵称，账户，收益率，收益
        
    # def test_4_getMonthlyList_field(self):
    #     '''判断新增字段排名，昵称，账户，收益率，收益是否存在'''
    #     generalList = []
    #     #遍历i里面所有的数据
    #     for i in json.loads(self.榜单接口返回内容.text)["data"]["items"]:
    #         #遍历items里面所有的key，value
    #         for k,v in i.items():
    #             #往key空列表里面增加key值
    #             generalList.append(k)
    #     generalList.sort()
    #     table = ['排名', '昵称', '账户','收益率','收益']
    #     table.sort()
    #     self.assertListEqual(generalList,table)

    # def test_5_getMonthlyList_number(self):
    #     generallist_number = []
    #     for i in json.loads(self.榜单接口返回内容.text)["data"]["items"]:
    #         generallist_number.append(i["排名"])
    #     self.assertGreater(len(i["排名"]), 10)

    # def test_6_getMonthlyList_Roisort(self):
    #     generallist_Roisort = []
    #     for i in json.loads(self.榜单接口返回内容.text)["data"]["items"]:
    #         generallist_Roisort.append(i["Roi"])
    #     j=10
    #     for j in generallist_Roisort:
    #         self.assertLessEqual(generallist_Roisort[j], generallist_Roisort[j-1])
    #         j=j-1

    # # 周榜：只显示当周前10名，排序默认以收益率从高到低为准，只显示十个，字段：排名，昵称，账户，收益率，收益
    # def test_7_getMonthlyList_field(self):
    #     '''判断新增字段排名，昵称，账户，收益率，收益是否存在'''
    #     generalList = []
    #     #遍历i里面所有的数据
    #     for i in json.loads(self.榜单接口返回内容.text)["data"]["items"]:
    #         #遍历items里面所有的key，value
    #         for k,v in i.items():
    #             #往key空列表里面增加key值
    #             generalList.append(k)
    #     generalList.sort()
    #     table = ['排名', '昵称', '账户','收益率','收益']
    #     table.sort()
    #     self.assertListEqual(generalList,table)

    # def test_8_getweeklyList_number(self):
    #     generallist_number = []
    #     for i in json.loads(self.榜单接口返回内容.text)["data"]["items"]:
    #         generallist_number.append(i["排名"])
    #     self.assertGreater(len(i["排名"]), 10)

    # def test_9_getMonthlyList_Roisort(self):
    #     generallist_Roisort = []
    #     for i in json.loads(self.榜单接口返回内容.text)["data"]["items"]:
    #         generallist_Roisort.append(i["Roi"])
    #     j=10
    #     for j in generallist_Roisort:
    #         self.assertLessEqual(generallist_Roisort[j], generallist_Roisort[j-1])
    #         j=j-1

    # #赞助经纪商榜单：点击某个经纪商，只展示该经纪商的数据，以收益率从高到低排序 2、显示TOP5 3、参赛者人数低于5位显示全部
    # def test_10_getBrokersList_field(self):
    #     '''判断新增字段排名，昵称，账户，收益率，收益是否存在'''
    #     brokersList = []
    #     #遍历i里面所有的数据
    #     for i in json.loads(self.榜单接口返回内容.text)["data"]["items"]:
    #         #遍历items里面所有的key，value
    #         for k,v in i.items():
    #             #往key空列表里面增加key值
    #             generalList.append(k)
    #     generalList.sort()
    #     table = ['排名', '昵称', '账户','收益率','收益']
    #     table.sort()
    #     self.assertListEqual(generalList,table)

    # def test_11_getBrokersList_number(self):
    #     generallist_number = []
    #     for i in json.loads(self.榜单接口返回内容.text)["data"]["items"]:
    #         generallist_number.append(i["排名"])
    #     self.assertGreater(len(i["排名"]), 10)

    # def test_12_getBrokersList_Roisort(self):
    #     generallist_Roisort = []
    #     for i in json.loads(self.榜单接口返回内容.text)["data"]["items"]:
    #         generallist_Roisort.append(i["Roi"])
    #     j=10
    #     for j in generallist_Roisort:
    #         self.assertLessEqual(generallist_Roisort[j], generallist_Roisort[j-1])
    #         j=j-1


    # #查看我的战绩
    
    def tearDown(self):
        #清空测试环境，还原测试数据
        #清除所有测试订单，如果有
        '''获取交易员的所有交易订单，并平掉'''
        # tradeOrderParams = {webAPIData['orderStatus']:webAPIData['orderStatus_open']}
        # getTradeOrders = Order.getOrders(webAPIData['hostName'] + orderData['getOrders_url'], self.tradeHeaders, params=tradeOrderParams)
        # #获取订单成功，返回200 ok
        # self.assertEqual(getTradeOrders.status_code, webAPIData['status_code_200'])
        # tradeOrdersIDList = Order.getOrdersID(getTradeOrders)
        # #平掉当前用户所有订单,如果有
        # # #web sockets批量平仓
        # closeParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_219'], tradeOnlineData['orderParam_tickets']: tradeOrdersIDList }
        # closePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.tradeToken}, closeParam)
        # #校验code等于0，为及时单平仓成功
        # self.assertEqual(closePositionRes["code"], tradeOnlineData['ws_code_0'])

        # '''获取跟随者的所有交易订单，并平掉'''
        # followOrderParams = {webAPIData['orderStatus']:webAPIData['orderStatus_open']}
        # getFollowOrders = Order.getOrders(webAPIData['hostName'] + orderData['getOrders_url'], self.followHeaders, params=followOrderParams)
        # #获取订单成功，返回200 ok
        # self.assertEqual(getFollowOrders.status_code, webAPIData['status_code_200'])
        # followOrdersIDList = Order.getOrdersID(getFollowOrders)
        # #平掉当前用户所有订单,如果有
        # # #web sockets批量平仓
        # closeParam = { tradeOnlineData['orderParam_code']: tradeOnlineData['ws_code_219'], tradeOnlineData['orderParam_tickets']: followOrdersIDList }
        # closePositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self, tradeOnlineData['ws_host'], tradeOnlineData['ws_port'], {'token': self.followToken}, closeParam)
        # #校验code等于0，为及时单平仓成功
        # self.assertEqual(closePositionRes["code"], tradeOnlineData['ws_code_0'])

        # # 取消跟随关系
        # deleteFollow = FollowManage.deleteFollow(webAPIData['hostName'] + followData['deleteFollow_url'] + self.tradeIndex, headers = self.followHeaders, accountIndex=self.tradePicoAccountIndex)
        # self.assertEqual(deleteFollow.status_code, webAPIData['status_code_200'])

        #登出followme系统
        tradeSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.tradeHeaders,printLogs=0)
        self.assertEqual(tradeSignout.status_code, webAPIData['status_code_200'])
        # followSignout = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas = self.followHeaders)
        # self.assertEqual(followSignout.status_code, webAPIData['status_code_200'])

if __name__ == '__main__':
    unittest.main()

