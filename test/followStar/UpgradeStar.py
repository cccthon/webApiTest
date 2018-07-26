import sys,unittest,json,requests,gc,redis,re,time

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import FMCommon,Account,Auth,Trade
from lib.tradeOnline import TradeOnline
from RegisterByMobile import RegisterByMobile
from BindPico import BindPico
from TradeForStar import TradeForStar
from MysqlDBOperation import OperationMysqlDB
from CloseAccounts import CloseAccounts

userData = FMCommon.loadWebAPIYML()
userDataAccountUrl=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()
userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()

class UpgradeStar(unittest.TestCase):
    def setUp(self):
        pass

    def test_UpgradeStar(self):
        '''注册新账号，建立层级关系，从1星->升级2星->升级3星->升级4星->升级5星'''
        # 注册所需手机号码
        self.telephone = ['13444444400','13444444401', '13444444402', '13444444403', '13444444404', '13444444405',
                          '13444444406','13444444407', '13444444408', '13444444409', '13444444410', '13444444411',
                          '13444444412','13444444413', '13444444414', '13444444415', '13444444416', '13444444417',
                          '13444444418','13444444419', '13444444420', '13444444421', '13444444422', '13444444423',
                          '13444444424','13444444425', '13444444426', '13444444427', '13444444128', '13444444129',
                          '13444444130','13444444131', '13444444132', '13444444133', '13444444134', '13444444135']
        # 注册密码
        self.mypassword = "123456"
        # 星级会员测试总账号vcode
        self.rootvode = '220429'
        self.thirtyVolume = 30000
        self.sixVolume = 600
        # 存用户id
        self.userID = []
        # 查询星级
        selectLevelIdSql = 'SELECT LEVELId from `user` WHERE UserId='
        # 查询vcode
        selectVcodeSql = 'SELECT VCode from `user` WHERE UserId='
        # 1.注册账号A
        userIDA = RegisterByMobile.registerByMobile(self.telephone[0], self.mypassword, self.rootvode)
        self.userID.append(userIDA)

        # 2.给A绑定晋峰账户
        BindPico.bindPico(userIDA,'ct_pico',1,1)

        # 3.验证A会员升级为2星
        time.sleep(5)
        selectLevelA2 = selectLevelIdSql+str(userIDA)
        selectLevelA2row = OperationMysqlDB.operationPyramidDB(selectLevelA2)
        # self.assertEqual(2,selectLevelA2row['LEVELId'],'A账号没有升级为2星')

        #4.查A的vcode
        selectVocdeA = selectVcodeSql+str(userIDA)
        selectVocdeArow = OperationMysqlDB.operationPyramidDB(selectVocdeA)

        #5.在A会员下注册一个下级会员AB
        userIDAB = RegisterByMobile.registerByMobile(self.telephone[1], self.mypassword, str(selectVocdeArow['VCode']))
        self.userID.append(userIDAB)

        #6.AB绑定一个晋峰账户
        BindPico.bindPico(userIDAB, 'ct_pico', 1, 1)

        # 7.AB会员交易30手，A交易6手
        TradeForStar.tradeForStar(self, self.telephone[1], self.mypassword, self.thirtyVolume)
        # 7.2A登录，获取交易token，开仓6，平仓6
        TradeForStar.tradeForStar(self, self.telephone[0], self.mypassword, self.sixVolume)
        time.sleep(5)

        # 8.验证A升级为3星
        selectLevelA3 = selectLevelIdSql + str(userIDA)
        selectLevelA3row=OperationMysqlDB.operationPyramidDB(selectLevelA3)
        # self.assertEqual(3,selectLevelA3row['LEVELId'],'A账号没有升级为3星')

        # 9.在AB的vcode
        selectVocdeAB = selectVcodeSql+str(userIDAB)
        selectVocdeABrow = OperationMysqlDB.operationPyramidDB(selectVocdeAB)

        # 10.在AB会员下注册一个下级会员B1
        userIDB1 = RegisterByMobile.registerByMobile(self.telephone[2], self.mypassword, str(selectVocdeABrow['VCode']))
        self.userID.append(userIDB1)

        #11.给B1绑定晋峰账户
        BindPico.bindPico(userIDB1,'ct_pico',1,1)
        #12.B1会员交易30手
        TradeForStar.tradeForStar(self, self.telephone[2], self.mypassword, self.thirtyVolume)

        # 13.验证AB会员升为3星
        time.sleep(5)
        selectLevelAB3 = selectLevelIdSql+str(userIDAB)
        selectLevelAB3row = OperationMysqlDB.operationPyramidDB(selectLevelAB3)
        # self.assertEqual(3, selectLevelAB3row['LEVELId'], 'AB账号没有升级为3星')

        # 14.在A会员下注册一个下级会员AC
        userIDAC = RegisterByMobile.registerByMobile(self.telephone[3], self.mypassword, str(selectVocdeArow['VCode']))
        self.userID.append(userIDAC)

        # 15.给AC绑定账户
        BindPico.bindPico(userIDAC, 'ct_pico', 1, 1)

        # 16.在AC会员下注册一个下级会员C1
        selectVocdeAC = selectVcodeSql+str(userIDAC)
        selectVocdeACrow = OperationMysqlDB.operationPyramidDB(selectVocdeAC)

        userIDC1 = RegisterByMobile.registerByMobile(self.telephone[4], self.mypassword, str(selectVocdeACrow['VCode']))
        self.userID.append(userIDC1)

        #17.C1会员开真实账户
        BindPico.bindPico(userIDC1, 'ct_pico', 1, 1)

        # 18.C1会员交易30手，AC会员交易6手
        TradeForStar.tradeForStar(self, self.telephone[4], self.mypassword, self.thirtyVolume)
        # AC会员交易6手
        TradeForStar.tradeForStar(self, self.telephone[3], self.mypassword, self.sixVolume)

        # 19.验证AC会员升为3星
        time.sleep(5)
        selectLevelAC3 = selectLevelIdSql+str(userIDAC)
        selectLevelAC3row = OperationMysqlDB.operationPyramidDB(selectLevelAC3)
        # self.assertEqual(3, selectLevelAC3row['LEVELId'], 'AC账号没有升级为3星')

        # 20.在A会员下注册一个下级会员AD
        userIDAD = RegisterByMobile.registerByMobile(self.telephone[5], self.mypassword, str(selectVocdeArow['VCode']))
        self.userID.append(userIDAD)

        # 21.AD会员开真实账户
        BindPico.bindPico(userIDAD, 'ct_pico', 1, 1)

        # 22.在AD会员下注册一个下级会员D1
        selectVocdeAD = selectVcodeSql+str(userIDAD)
        selectVocdeADrow = OperationMysqlDB.operationPyramidDB(selectVocdeAD)

        userIDD1 = RegisterByMobile.registerByMobile(self.telephone[6], self.mypassword, str(selectVocdeADrow['VCode']))
        self.userID.append(userIDD1)
        #23.D1会员开真实账户
        BindPico.bindPico(userIDD1, 'ct_pico', 1, 1)

        # 24.D1会员交易30手，AD会员交易6手
        TradeForStar.tradeForStar(self, self.telephone[6], self.mypassword, self.sixVolume)
        TradeForStar.tradeForStar(self, self.telephone[5], self.mypassword, self.thirtyVolume)

        # 25.A会员自己再交易100手，赚取服务费达到1500
        TradeForStar.tradeForStar(self, self.telephone[0], self.mypassword, 10000)
        time.sleep(5)
        # 26.验证A升级为4星
        selectLevelA4 = selectLevelIdSql+str(userIDA)
        selectLevelA4row = OperationMysqlDB.operationPyramidDB(selectLevelA4)
        # self.assertEqual(4, selectLevelA4row['LEVELId'], 'A账号没有升级为4星')

        # 27.在A会员下注册一个下级会员AE
        userIDAE = RegisterByMobile.registerByMobile(self.telephone[7], self.mypassword, str(selectVocdeArow['VCode']))
        self.userID.append(userIDAE)
        # 28.AE会员开真实账户
        BindPico.bindPico(userIDAE, 'ct_pico', 1, 1)

        # 29.在AE会员下注册一个下级会员E1
        selectVocdeAE = selectVcodeSql + str(userIDAE)
        selectVocdeAErow = OperationMysqlDB.operationPyramidDB(selectVocdeAE)
        userIDE1 = RegisterByMobile.registerByMobile(self.telephone[8], self.mypassword, str(selectVocdeAErow['VCode']))
        self.userID.append(userIDE1)

        # 30.E1会员开真实账户
        BindPico.bindPico(userIDE1, 'ct_pico', 1, 1)

        # 31.E1会员交易30手，AE会员交易6手
        TradeForStar.tradeForStar(self, self.telephone[8], self.mypassword, self.thirtyVolume)
        TradeForStar.tradeForStar(self, self.telephone[7], self.mypassword, self.sixVolume)

        # 32.验证AE会员升为3星
        time.sleep(5)
        selectLevelAE3 = selectLevelIdSql + str(userIDAE)
        selectLevelAE3row = OperationMysqlDB.operationPyramidDB(selectLevelAE3)
        # self.assertEqual(3, selectLevelAE3row['LEVELId'], 'AE账号没有升级为3星')

        # 33.在A会员下注册一个下级会员AF，开真实账户
        userIDAF = RegisterByMobile.registerByMobile(self.telephone[9], self.mypassword, str(selectVocdeArow['VCode']))
        self.userID.append(userIDAF)
        BindPico.bindPico(userIDAF, 'ct_pico', 1, 1)

        # 34.在AF会员下注册一个下级会员F1
        selectVocdeAF = selectVcodeSql + str(userIDAF)
        selectVocdeAFrow = OperationMysqlDB.operationPyramidDB(selectVocdeAF)

        userIDF1 = RegisterByMobile.registerByMobile(self.telephone[10], self.mypassword, str(selectVocdeAFrow['VCode']))
        self.userID.append(userIDF1)
        # F1会员开真实账户
        BindPico.bindPico(userIDF1, 'ct_pico', 1, 1)

        # 35.F1会员交易30手，AF会员交易6手
        TradeForStar.tradeForStar(self, self.telephone[10], self.mypassword, self.thirtyVolume)
        TradeForStar.tradeForStar(self, self.telephone[9], self.mypassword, self.sixVolume)
        time.sleep(5)
        # 36.验证AF会员升为3星
        selectLevelAF3 = selectLevelIdSql + str(userIDAF)
        selectLevelAF3row = OperationMysqlDB.operationPyramidDB(selectLevelAF3)
        # self.assertEqual(3, selectLevelAF3row['LEVELId'], 'AF账号没有升级为3星')

        # 37.在B1会员下注册一个下级会员B11
        selectVocdeB1 = selectVcodeSql + str(userIDB1)
        selectVocdeB1row = OperationMysqlDB.operationPyramidDB(selectVocdeB1)

        userIDB11 = RegisterByMobile.registerByMobile(self.telephone[11], self.mypassword, str(selectVocdeB1row['VCode']))
        self.userID.append(userIDB11)
        BindPico.bindPico(userIDB11, 'ct_pico', 1, 1)

        # 38.B11会员交易30手
        TradeForStar.tradeForStar(self, self.telephone[11], self.mypassword, self.thirtyVolume)
        time.sleep(5)
        # 验证B1会员升为3星
        selectLevelB13 = selectLevelIdSql + str(userIDB1)
        selectLevelB13row = OperationMysqlDB.operationPyramidDB(selectLevelB13)
        # self.assertEqual(3, selectLevelB13row['LEVELId'], 'B1账号没有升级为3星')

        # 39.在AB会员下注册一个下级会员B2,开真实账户
        userIDB2 = RegisterByMobile.registerByMobile(self.telephone[12], self.mypassword, str(selectVocdeABrow['VCode']))
        self.userID.append(userIDB2)
        BindPico.bindPico(userIDB2, 'ct_pico', 1, 1)

        # 40.B2会员交易6手
        TradeForStar.tradeForStar(self, self.telephone[12], self.mypassword, self.sixVolume)

        # 41.在B2会员下注册一个下级会员B22,开真实账户
        selectVocdeB2= selectVcodeSql + str(userIDB2)
        selectVocdeB2row = OperationMysqlDB.operationPyramidDB(selectVocdeB2)

        userIDB22 = RegisterByMobile.registerByMobile(self.telephone[13], self.mypassword, str(selectVocdeB2row['VCode']))
        self.userID.append(userIDB22)
        # 42.B22会员交易30手
        BindPico.bindPico(userIDB22, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[13], self.mypassword, self.sixVolume)

        # 43.验证B2会员升为3星
        time.sleep(5)
        selectLevelB23 = selectLevelIdSql + str(userIDB2)
        selectLevelB23row = OperationMysqlDB.operationPyramidDB(selectLevelB23)
        # self.assertEqual(3, selectLevelB23row['LEVELId'], 'B2账号没有升级为3星')

        # 44.在AB会员下注册一个下级会员B3,开真实账户,交易6手
        userIDB3 = RegisterByMobile.registerByMobile(self.telephone[14], self.mypassword, str(selectVocdeABrow['VCode']))
        self.userID.append(userIDB3)
        BindPico.bindPico(userIDB3, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[14], self.mypassword, self.sixVolume)

        # 45.在B3会员下注册一个下级会员B33,B33会员交易30手
        selectVocdeB3 = selectVcodeSql + str(userIDB3)
        selectVocdeB3row = OperationMysqlDB.operationPyramidDB(selectVocdeB3)

        userIDB33 = RegisterByMobile.registerByMobile(self.telephone[15], self.mypassword, str(selectVocdeB3row['VCode']))
        self.userID.append(userIDB33)
        BindPico.bindPico(userIDB33, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[15], self.mypassword, self.thirtyVolume)

        time.sleep(5)
        #46.验证B3会员升为3星
        selectLevelB33 = selectLevelIdSql + str(userIDB3)
        selectLevelB33row = OperationMysqlDB.operationPyramidDB(selectLevelB33)
        # self.assertEqual(3, selectLevelB33row['LEVELId'], 'B3账号没有升级为3星')
        TradeForStar.tradeForStar(self, self.telephone[1], self.mypassword, 10000)
        time.sleep(5)

        #47.验证AB为四星
        selectLevelAB4 = selectLevelIdSql + str(userIDAB)
        selectLevelAB4row = OperationMysqlDB.operationPyramidDB(selectLevelAB4)
        # self.assertEqual(4, selectLevelAB4row['LEVELId'], 'AB账号没有升级为4星')

        # 48.在C1会员下注册一个下级会员C11,开真实账户,C11会员交易30手,验证C1会员升为3星
        selectVocdeC1 = selectVcodeSql + str(userIDC1)
        selectVocdeC1row = OperationMysqlDB.operationPyramidDB(selectVocdeC1)

        userIDC11 = RegisterByMobile.registerByMobile(self.telephone[16], self.mypassword, str(selectVocdeC1row['VCode']))
        self.userID.append(userIDC11)
        BindPico.bindPico(userIDC11, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[16], self.mypassword, self.thirtyVolume)
        time.sleep(5)

        selectLevelC13 = selectLevelIdSql + str(userIDC1)
        selectLevelC13row = OperationMysqlDB.operationPyramidDB(selectLevelC13)
        # self.assertEqual(3, selectLevelC13row['LEVELId'], 'C1账号没有升级为3星')
        # 49.在AC会员下注册一个下级会员C2,开真实账户,C2会员交易6手
        userIDC2 = RegisterByMobile.registerByMobile(self.telephone[17], self.mypassword, str(selectVocdeACrow['VCode']))
        self.userID.append(userIDC2)
        BindPico.bindPico(userIDC2, 'ct_pico', 1, 1)

        TradeForStar.tradeForStar(self, self.telephone[17], self.mypassword, self.sixVolume)

        # 50.在C2会员下注册一个下级会员C22,开真实账户,C22会员交易30手,验证C2会员升为3星
        selectVocdeC2 = selectVcodeSql + str(userIDC2)
        selectVocdeC2row = OperationMysqlDB.operationPyramidDB(selectVocdeC2)
        userIDC22 = RegisterByMobile.registerByMobile(self.telephone[18], self.mypassword, str(selectVocdeC2row['VCode']))
        self.userID.append(userIDC22)

        BindPico.bindPico(userIDC22, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[18], self.mypassword, self.thirtyVolume)
        time.sleep(5)
        selectLevelC23 = selectLevelIdSql + str(userIDC2)
        selectLevelC23row = OperationMysqlDB.operationPyramidDB(selectLevelC23)
        # self.assertEqual(3, selectLevelC23row['LEVELId'], 'C2账号没有升级为3星')

        # 51.在AC会员下注册一个下级会员C3，开真实账户，C3会员交易6手
        userIDC3= RegisterByMobile.registerByMobile(self.telephone[19], self.mypassword, str(selectVocdeACrow['VCode']))
        self.userID.append(userIDC3)
        BindPico.bindPico(userIDC3, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[19], self.mypassword, self.sixVolume)

        # 52.在C3会员下注册一个下级会员C33,开真实账户,C33会员交易30手
        selectVocdeC3 = selectVcodeSql + str(userIDC3)
        selectVocdeC3row = OperationMysqlDB.operationPyramidDB(selectVocdeC3)
        userIDC33 = RegisterByMobile.registerByMobile(self.telephone[20], self.mypassword, str(selectVocdeC3row['VCode']))
        self.userID.append(userIDC33)

        BindPico.bindPico(userIDC33, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[20], self.mypassword, self.thirtyVolume)
        time.sleep(5)

        # 53.验证C3会员升为3星, AC为4星
        selectLevelC33 = selectLevelIdSql + str(userIDC3)
        selectLevelC23row = OperationMysqlDB.operationPyramidDB(selectLevelC33)
        # self.assertEqual(3, selectLevelC23row['LEVELId'], 'C3账号没有升级为3星')

        TradeForStar.tradeForStar(self, self.telephone[3], self.mypassword, 10000)
        time.sleep(5)

        selectLevelAC4 = selectLevelIdSql + str(userIDAC)
        selectLevelAC4row = OperationMysqlDB.operationPyramidDB(selectLevelAC4)
        # self.assertEqual(4, selectLevelAC4row['LEVELId'], 'AC账号没有升级为4星')

        # 54.在D1会员下注册一个下级会员D11,开真实账户
        selectVocdeD1 = selectVcodeSql + str(userIDD1)
        selectVocdeD1row = OperationMysqlDB.operationPyramidDB(selectVocdeD1)
        userIDD11 = RegisterByMobile.registerByMobile(self.telephone[21], self.mypassword, str(selectVocdeD1row['VCode']))
        self.userID.append(userIDD11)

        BindPico.bindPico(userIDD11, 'ct_pico', 1, 1)

        # 55.D11会员交易30手, D1会员升为3星
        TradeForStar.tradeForStar(self, self.telephone[21], self.mypassword, self.thirtyVolume)

        selectLevelD13 = selectLevelIdSql + str(userIDD1)
        selectLevelD13row = OperationMysqlDB.operationPyramidDB(selectLevelD13)
        # self.assertEqual(3, selectLevelD13row['LEVELId'], 'D1账号没有升级为3星')

        # 56.在AD会员下注册一个下级会员D2,开真实账户,D2会员交易6手
        userIDD2 = RegisterByMobile.registerByMobile(self.telephone[22], self.mypassword, str(selectVocdeADrow['VCode']))
        self.userID.append(userIDD2)

        BindPico.bindPico(userIDD2, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[22], self.mypassword, self.sixVolume)

        # 57.在D2会员下注册一个下级会员D22,开真实账户
        selectVocdeD2 = selectVcodeSql + str(userIDD2)
        selectVocdeD2row = OperationMysqlDB.operationPyramidDB(selectVocdeD2)
        userIDD22 = RegisterByMobile.registerByMobile(self.telephone[23], self.mypassword, str(selectVocdeD2row['VCode']))
        self.userID.append(userIDD22)

        BindPico.bindPico(userIDD22, 'ct_pico', 1, 1)

        # 58. D22会员交易30手, D2会员升为3星
        TradeForStar.tradeForStar(self, self.telephone[23], self.mypassword, self.thirtyVolume)
        time.sleep(5)
        selectLevelD23 = selectLevelIdSql + str(userIDD2)
        selectLevelD23row = OperationMysqlDB.operationPyramidDB(selectLevelD23)
        # self.assertEqual(3, selectLevelD23row['LEVELId'], 'D2账号没有升级为3星')

        # 59.在AD会员下注册一个下级会员D3,开真实账户,D3会员交易6手
        userIDD3 = RegisterByMobile.registerByMobile(self.telephone[24], self.mypassword, str(selectVocdeADrow['VCode']))
        self.userID.append(userIDD3)

        BindPico.bindPico(userIDD3, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[24], self.mypassword, self.sixVolume)

        # 60.在D3会员下注册一个下级会员D33,开真实账户
        selectVocdeD3 = selectVcodeSql + str(userIDD3)
        selectVocdeD3row = OperationMysqlDB.operationPyramidDB(selectVocdeD3)
        userIDD33 = RegisterByMobile.registerByMobile(self.telephone[25], self.mypassword, str(selectVocdeD3row['VCode']))
        self.userID.append(userIDD33)

        BindPico.bindPico(userIDD33, 'ct_pico', 1, 1)

        # 61.D33会员交易30手, D3会员升为3星, AD为4星
        TradeForStar.tradeForStar(self, self.telephone[25], self.mypassword, self.thirtyVolume)
        time.sleep(5)
        selectLevelD33 = selectLevelIdSql + str(userIDD3)
        selectLevelD33row = OperationMysqlDB.operationPyramidDB(selectLevelD33)
        # self.assertEqual(3, selectLevelD33row['LEVELId'], 'D3账号没有升级为3星')

        TradeForStar.tradeForStar(self, self.telephone[5], self.mypassword, 10000)
        time.sleep(5)

        selectLevelAD4 = selectLevelIdSql + str(userIDAD)
        selectLevelAD4row = OperationMysqlDB.operationPyramidDB(selectLevelAD4)
        # self.assertEqual(4, selectLevelAD4row['LEVELId'], 'AD账号没有升级为4星')

        # 62.在E1会员下注册一个下级会员E11,开真实账户,E11会员交易30手,验证E1会员升为3星
        selectVocdeE1 = selectVcodeSql + str(userIDE1)
        selectVocdeE1row = OperationMysqlDB.operationPyramidDB(selectVocdeE1)
        userIDE11 = RegisterByMobile.registerByMobile(self.telephone[26], self.mypassword, str(selectVocdeE1row['VCode']))
        self.userID.append(userIDE11)
        BindPico.bindPico(userIDE11, 'ct_pico', 1, 1)

        TradeForStar.tradeForStar(self, self.telephone[26], self.mypassword, self.thirtyVolume)
        time.sleep(5)
        selectLevelE13 = selectLevelIdSql + str(userIDE1)
        selectLevelE13row = OperationMysqlDB.operationPyramidDB(selectLevelE13)
        # self.assertEqual(3, selectLevelE13row['LEVELId'], 'E1账号没有升级为3星')

        # 63.在AE会员下注册一个下级会员E2,开真实账户,E2会员交易6手
        userIDE2 = RegisterByMobile.registerByMobile(self.telephone[27], self.mypassword, str(selectVocdeAErow['VCode']))
        self.userID.append(userIDE2)

        BindPico.bindPico(userIDE2, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[27], self.mypassword, self.sixVolume)

        # 64.在E2会员下注册一个下级会员E22,开真实账户,E22会员交易30手,验证E2会员升为3星
        selectVocdeE2 = selectVcodeSql + str(userIDE2)
        selectVocdeE2row = OperationMysqlDB.operationPyramidDB(selectVocdeE2)
        userIDE22 = RegisterByMobile.registerByMobile(self.telephone[28], self.mypassword, str(selectVocdeE2row['VCode']))
        self.userID.append(userIDE22)

        BindPico.bindPico(userIDE22, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[28], self.mypassword, self.thirtyVolume)
        time.sleep(5)

        selectLevelE23 = selectLevelIdSql + str(userIDE2)
        selectLevelE23row = OperationMysqlDB.operationPyramidDB(selectLevelE23)
        # self.assertEqual(3, selectLevelE23row['LEVELId'], 'E2账号没有升级为3星')

        # 65.在AE会员下注册一个下级会员E3,开真实账户,E3会员交易6手
        userIDE3 = RegisterByMobile.registerByMobile(self.telephone[29], self.mypassword, str(selectVocdeAErow['VCode']))
        self.userID.append(userIDE3)

        BindPico.bindPico(userIDE3, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[29], self.mypassword, self.sixVolume)

        # 66.在E3会员下注册一个下级会员E33,开真实账户
        selectVocdeE3 = selectVcodeSql + str(userIDE3)
        selectVocdeE3row = OperationMysqlDB.operationPyramidDB(selectVocdeE3)
        userIDE33 = RegisterByMobile.registerByMobile(self.telephone[30], self.mypassword, str(selectVocdeE3row['VCode']))
        self.userID.append(userIDE33)

        BindPico.bindPico(userIDE33, 'ct_pico', 1, 1)

        # 67.E33会员交易30手, 验证E3会员升为3星, AE为4星
        TradeForStar.tradeForStar(self, self.telephone[30], self.mypassword, self.thirtyVolume)
        time.sleep(5)

        selectLevelE33 = selectLevelIdSql + str(userIDE3)
        selectLevelE33row = OperationMysqlDB.operationPyramidDB(selectLevelE33)
        # self.assertEqual(3, selectLevelE33row['LEVELId'], 'E3账号没有升级为3星')

        TradeForStar.tradeForStar(self, self.telephone[7], self.mypassword, 10000)
        time.sleep(5)

        selectLevelAE4 = selectLevelIdSql + str(userIDAE)
        selectLevelAE4row = OperationMysqlDB.operationPyramidDB(selectLevelAE4)
        # self.assertEqual(4, selectLevelAE4row['LEVELId'], 'AE账号没有升级为4星')

        # 68.在F1会员下注册一个下级会员F11，开真实账户，F11会员交易30手，验证F1会员升为3星
        selectVocdeF1 = selectVcodeSql + str(userIDF1)
        selectVocdeF1row = OperationMysqlDB.operationPyramidDB(selectVocdeF1)

        userIDF11 = RegisterByMobile.registerByMobile(self.telephone[31], self.mypassword, str(selectVocdeF1row['VCode']))
        self.userID.append(userIDF11)

        BindPico.bindPico(userIDF11, 'ct_pico', 1, 1)

        TradeForStar.tradeForStar(self, self.telephone[31], self.mypassword, self.thirtyVolume)
        time.sleep(5)

        selectLevelF13 = selectLevelIdSql + str(userIDF1)
        selectLevelF13row = OperationMysqlDB.operationPyramidDB(selectLevelF13)
        # self.assertEqual(3, selectLevelF13row['LEVELId'], 'F1账号没有升级为3星')

        # 69.在AF会员下注册一个下级会员F2，开真实账户，F2会员交易6手
        userIDF2 = RegisterByMobile.registerByMobile(self.telephone[32], self.mypassword, str(selectVocdeAFrow['VCode']))
        self.userID.append(userIDF2)

        BindPico.bindPico(userIDF2, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[32], self.mypassword, self.sixVolume)
        # 70.在F2会员下注册一个下级会员F22，开真实账户，F22会员交易30手，验证F2会员升为3星
        selectVocdeF2 = selectVcodeSql + str(userIDF2)
        selectVocdeF2row = OperationMysqlDB.operationPyramidDB(selectVocdeF2)

        userIDF22 = RegisterByMobile.registerByMobile(self.telephone[33], self.mypassword, str(selectVocdeF2row['VCode']))
        self.userID.append(userIDF22)

        BindPico.bindPico(userIDF22, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[33], self.mypassword, self.thirtyVolume)
        time.sleep(5)

        selectLevelF23 = selectLevelIdSql + str(userIDF2)
        selectLevelF23row = OperationMysqlDB.operationPyramidDB(selectLevelF23)
        # self.assertEqual(3, selectLevelF23row['LEVELId'], 'F2账号没有升级为3星')

        # 71.在AF会员下注册一个下级会员F3，开真实账户，F3会员交易6手
        userIDF3 = RegisterByMobile.registerByMobile(self.telephone[34], self.mypassword, str(selectVocdeAFrow['VCode']))
        self.userID.append(userIDF3)

        BindPico.bindPico(userIDF3, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[34], self.mypassword, self.sixVolume)

        # 72.在F3会员下注册一个下级会员F33，开真实账户，F33会员交易30手，验证F3会员升为3星
        # userIDF3 = 169419
        selectVocdeF3 = selectVcodeSql + str(userIDF3)
        selectVocdeF3row = OperationMysqlDB.operationPyramidDB(selectVocdeF3)

        userIDF33 = RegisterByMobile.registerByMobile(self.telephone[35], self.mypassword, str(selectVocdeF3row['VCode']))
        self.userID.append(userIDF33)

        BindPico.bindPico(userIDF33, 'ct_pico', 1, 1)
        TradeForStar.tradeForStar(self, self.telephone[35], self.mypassword, self.thirtyVolume)
        time.sleep(5)

        #给所有账号做单30手，创建服务费
        for i in self.telephone:
            TradeForStar.tradeForStar(self, i, self.mypassword, self.thirtyVolume)

        selectLevelF33 = selectLevelIdSql + str(userIDF3)
        selectLevelF33row = OperationMysqlDB.operationPyramidDB(selectLevelF33)
        # self.assertEqual(3, selectLevelF33row['LEVELId'], 'F3账号没有升级为3星')

        # 验证AF为4星
        selectLevelAF4 = selectLevelIdSql + str(userIDAF)
        selectLevelAF4row = OperationMysqlDB.operationPyramidDB(selectLevelAF4)
        # self.assertEqual(4, selectLevelAF4row['LEVELId'], 'AF账号没有升级为4星')

        # 验证A为5星
        time.sleep(5)
        selectLevelA5 = selectLevelIdSql + str(userIDA)
        selectLevelA5row = OperationMysqlDB.operationPyramidDB(selectLevelA5)
        self.assertEqual(5, selectLevelA5row['LEVELId'], 'A账号没有升级为5星')

    def tearDown(self):
        print("userID:",self.userID)
        #注销所有新注册的星级会员账号
        # CloseAccounts.closeAccounts(self.userID)

if __name__ == '__main__':
    unittest.main()
