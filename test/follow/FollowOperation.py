import grpc,sys,unittest,yaml,uuid,json
import FMCommon,Follow,pymssql
sys.path.append("../../lib/proto")
sys.path.append("../../lib/common")

userData = FMCommon.loadWebAPIYML()
userDataFollow=FMCommon.loadFollowYML()

class Operation(object):
    @staticmethod
    def createFollow(traderUserId,tradeAccountIndex,headers,followAccountIndex):
        params = {"accountIndex": followAccountIndex, "strategy": "fixed", "setting": 1.5, "direction": "positive"}
        Follow.createFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(traderUserId) + "_" + tradeAccountIndex,
            headers, datas=params)
        follower = str(followAccountIndex)
        return follower

    @staticmethod
    def deleteFollow(traderUserId, tradeAccountIndex,headers,followAccountIndex):
        Follow.DeleteFollow(
            userData['hostName'] + userDataFollow["Follow_Url"] + str(traderUserId) + "_" +
            tradeAccountIndex +"?accountIndex="+str(followAccountIndex),
            headers)
        follower = str(followAccountIndex)
        return follower

    @staticmethod
    def operationCopytradingDB(mysql):
        row = FMCommon.mysql_operaters(userData['beta_mysql_host'],
                                       userData['beta_mysql_port'],
                                       'copytrading',
                                       userData['beta_mysql_user'],
                                       userData['beta_mysql_passwd'],
                                       mysql)
        return row

    @staticmethod
    def operationV3DB(mysql):
        row = FMCommon.mssql_operater(host='119.23.168.162',
                                      port=52436,
                                      database='FM_OS_V3',
                                      uid='chenyangyang',
                                      pwd='fmW3gxCDATWF',
                                      sql=mysql)
        return row

