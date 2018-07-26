import sys,unittest,json,requests,gc,redis,re,time

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import FMCommon,FollowStar

userData = FMCommon.loadWebAPIYML()
userDataFollowStar = FMCommon.loadFollowStarYML()

class BankCard(unittest.TestCase):
    def setUp(self):
        # 1.登录followstar13444444401
        datas = {"account": '18088888802', "password": '123456'}
        followstarloginRES = FollowStar.loginFStar(userData['hostPyramid']+userDataFollowStar['followStarLogin_url'],
                                                   userData['headers'],datas,interfaceName='followStarLogin')
        self.assertEqual(followstarloginRES.status_code, userData['status_code_200'])
        self.userId = json.loads(followstarloginRES.text)['data']['userId']
        self.FollowStarToken = json.loads(followstarloginRES.text)['data']['token']
        userData['headers'][userData['Authorization']] = userData['Bearer'] + self.FollowStarToken

    def test_BankCard(self):
        '''1.我的服务费-获取银行卡信息'''
        getPaymentRES = FollowStar.getPayment(userData['hostPyramid']+userDataFollowStar['getPayment_url'],
                                                   userData['headers'],interfaceName='getPayment')
        self.assertEqual(getPaymentRES.status_code, userData['status_code_200'])
        self.isBindCard = json.loads(getPaymentRES.text)['data']['isBindCard']

        '''2.绑定银行卡时获取验证码,短信验证码'''

        '''3.检查图形验证码是否正确 '''

        '''4.获取验证码 '''

        '''5.我的服务费-绑定/更新银行卡 '''
        # datas = {"CardSignName": '测试零零二二', "CardBank":'中国工商银行', "CardNumber":'61267452201807121038', "CardBankAddress":'广东省深圳市南山支行'}
        # CreateNewOrUpdatePaymentRES = FollowStar.CreateNewOrUpdatePayment(userData['hostPyramid']+userDataFollowStar['CreateNewOrUpdatePayment_url'],
        #                                            userData['headers'], datas, interfaceName='CreateNewOrUpdatePayment')
        # self.assertEqual(CreateNewOrUpdatePaymentRES.status_code, userData['status_code_200'])
        # # self.isBindCard = json.loads(CreateNewOrUpdatePaymentRES.text)['data']['isBindCard']

    def tearDown(self):
        # 登出
        FollowStarLogoutRES = FollowStar.FollowStarLogout(userData['hostPyramid'] + userDataFollowStar['FollowStarLogout_url'],
                                                                  userData['headers'], interfaceName='FollowStarLogout')
        self.assertEqual(FollowStarLogoutRES.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()
