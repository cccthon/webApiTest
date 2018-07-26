import sys,unittest,json,requests,gc,redis,re,time

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import Auth,FMCommon
from MysqlDBOperation import OperationMysqlDB

userData = FMCommon.loadWebAPIYML()
userDataAuth=FMCommon.loadAuthYML()

class CloseAccounts():
    @staticmethod
    def closeAccounts(userId):
        #oa单点登录获取token
        clientId = "oa"
        userName = "mqwtkn69074@chacuo.net"
        password = "123456"
        getUserTokenRES = Auth.getUserToken(userData['hostNameSwagger']+userDataAuth['getUserToken_url']+clientId+"&userName="+userName+"&password="+password,
                                            userData['headersOA'],interfaceName="getUserToken")
        tokenOA = json.loads(getUserTokenRES.text)['accessToken']

        headerOA = {'content-type': 'application/json', 'Accept': 'application/json','Authorization': 'Bearer ' + str(tokenOA)}


        #批量注销新注册的账户
        for i in userId:
             Auth.closeAccount(userData['hostNameOA']+userDataAuth['getCloseAccount_url']+str(i),
                               headers=headerOA,interfaceName="closeAccount",printLogs=1)
             print("已经注销账号",userId)
