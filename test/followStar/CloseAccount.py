import sys,unittest,json,requests,gc,redis,re,time

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import FMCommon,Account,Auth,Trade
from lib.tradeOnline import TradeOnline
from RegisterByMobile import RegisterByMobile
from BindPico import BindPico

userData = FMCommon.loadWebAPIYML()
userDataAccountUrl=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()
userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()

class UpgradeStar(unittest.TestCase):
    def setUp(self):
        pass

    def test_registerAndLogin(self):
        #oa单点登录获取token
        clientId = "oa"
        userName = "mqwtkn69074@chacuo.net"
        password = "123456"
        getUserTokenRES = Auth.getUserToken(
            userData['hostNameSwagger'] +userDataAuth['getUserToken_url']+clientId+"&userName="+userName+"&password="+password,
            userData['headersOA'],interfaceName="getUserToken")
        self.assertEqual(getUserTokenRES.status_code, userData['status_code_200'])
        self.tokenOA = json.loads(getUserTokenRES.text)['accessToken']

        self.headerOA = {'content-type': 'application/json', 'Accept': 'application/json',
                         'Authorization': 'Bearer ' + str(self.tokenOA)}
        #批量注销新注册的账户
        userId = [169580, 169581, 169582, 169583, 169584, 169585, 169586]
        # userId = [169282]
        for i in userId:
            closeAccountRES = Auth.closeAccount(userData['hostNameOA']+userDataAuth['getCloseAccount_url']+str(i),
                                                headers=self.headerOA,interfaceName="closeAccount",printLogs=1)
            self.assertEqual(closeAccountRES.status_code, userData['status_code_200'])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()