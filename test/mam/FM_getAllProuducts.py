#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getAllProuducts
# 用例标题: 获取所有产品列表（状态、收益分配、最大风险、操作周期范围、最低参与资金、收益范围）
# 流程：
    #1、产品状态 全部、发布中、交易中、已结束、进行中
    #2、收益分配 全部、2：8、5：5
    #3、最大风险 <1%、<5%、<7.5%、<10%、<12.5%、<15%
    #4、操作周期 全部、15天内、15-30天、30-60天、60-90天
    #5、最低参与资金 全部、5千-1万、1万-3万、3万-5万、5万-10万、10万-20万、20万以上
    #6、获取发布中 2：8 产品
    #7、获取进行中 2：8 产品
    #8、获取进行中 2：8 产品，最大风险<1%,操作周期15天内，最低参与资金5千-1w的产品
    #9、获取已结束的产品
    #10、获取已结束产品筛选最终收益10%以内
import sys,requests,unittest,yaml,json,time

sys.path.append("../../lib/MAM")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
sys.path.append("../../lib/common")

import FMCommon,MAM

userData = FMCommon.loadWebAPIYML()
userDataMAMUrl=FMCommon.loadMamYML()
webAPIData = FMCommon.loadWebAPIYML()

class GetAllProuducts(unittest.TestCase):
    def setUp(self):
            print('Start！')

    '''获取全部产品列表'''
    def test_getAllProuducts_001(self):

        getAllProductsRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'])
        self.assertEqual(getAllProductsRes.status_code,webAPIData['status_code_200'],'获取全部产品列表失败！')

    '''获取发布中产品列表'''
    def test_getAllProuductsOfStatus_002(self):
        datas={"status": userData['status_Pending']}
        getAllProuductsOfStatusRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProuductsOfStatusRes.status_code,webAPIData['status_code_200'],'获取发布中产品失败！')

        getAllProuductsOfStatusList=json.loads(getAllProuductsOfStatusRes.text)['data']['items']
        if len(getAllProuductsOfStatusList):
            for i in range(len(getAllProuductsOfStatusList)):
                self.assertEqual(getAllProuductsOfStatusList[i]['Status'],userData['status_Pending'],'获取发布中的产品数据状态非Pending状态！')


    '''获取收益分配比例2:8'''
    def test_getAllProductsOfProfitRatio_003(self):
        datas={"profitRatio": userData['profitRatio1']}
        getAllProductsOfProfitRatioRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProductsOfProfitRatioRes.status_code,webAPIData['status_code_200'],'获取产品收益分配比例为2:8失败！')

        getAllProductsOfProfitRatioList=json.loads(getAllProductsOfProfitRatioRes.text)['data']['items']
        if len(getAllProductsOfProfitRatioList):
            for i in  range(len(getAllProductsOfProfitRatioList)):
                print(i+getAllProductsOfProfitRatioList[i]['ProfitMode']['TakeProfitRatio'])
                self.assertEqual(getAllProductsOfProfitRatioList[i]['ProfitMode']['TakeProfitRatio'],0.8,'获取产品收益分配比例数据非2:8产品！')
                self.assertEqual(getAllProductsOfProfitRatioList[i]['ProfitMode']['StopLossRatio'],1,'获取产品收益分配比例数据非2:8产品！')

    '''获取收益分配比例5:5'''
    def test_getAllProductsOfProfitRatio_004(self):
        datas={"profitRatio": userData['profitRatio2']}
        getAllProductsOfProfitRatioRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProductsOfProfitRatioRes.status_code,webAPIData['status_code_200'],'获取产品收益分配比例为5:5失败！')

        getAllProductsOfProfitRatioList=json.loads(getAllProductsOfProfitRatioRes.text)['data']['items']
        if len(getAllProductsOfProfitRatioList):
            for i in  range(len(getAllProductsOfProfitRatioList)):
                self.assertEqual(getAllProductsOfProfitRatioList[i]['ProfitMode']['TakeProfitRatio'],userData['takeProfitRatio2'],'获取产品收益分配比例数据非5:5产品！')
                self.assertEqual(getAllProductsOfProfitRatioList[i]['ProfitMode']['StopLossRatio'],userData['stopLossRatio2'],'获取产品收益分配比例数据非5:5产品！')

    '''获取最大风险<1%'''
    def test_getAllProductsOfFollowerMaxRisk_005(self):
        datas={"followerMaxRisk": userData['followerMaxRisk1']}
        getAllProductsOfFollowerMaxRiskRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProductsOfFollowerMaxRiskRes.status_code,webAPIData['status_code_200'],'获取最大风险产品失败！')

        getAllProductsOfFollowerMaxRiskList=json.loads(getAllProductsOfFollowerMaxRiskRes.text)['data']['items']
        if len(getAllProductsOfFollowerMaxRiskList):
            for i in range(len(getAllProductsOfFollowerMaxRiskList)):
                self.assertEqual(getAllProductsOfFollowerMaxRiskList[i]['FollowerMaxRisk'],0.01,'获取最大风险<1%的数据错误！')

    '''获取最大风险<5%'''
    def test_getAllProductsOfFollowerMaxRisk_006(self):
        datas={"followerMaxRisk": userData['followerMaxRisk2']}
        getAllProductsOfFollowerMaxRiskRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProductsOfFollowerMaxRiskRes.status_code,webAPIData['status_code_200'],'获取最大风险产品失败！')

        getAllProductsOfFollowerMaxRiskList=json.loads(getAllProductsOfFollowerMaxRiskRes.text)['data']['items']
        if len(getAllProductsOfFollowerMaxRiskList):
            for i in range(len(getAllProductsOfFollowerMaxRiskList)):
                self.assertEqual(getAllProductsOfFollowerMaxRiskList[i]['FollowerMaxRisk'],0.05,'获取最大风险<5%的数据错误！')

    '''获取最大风险<7.5%'''
    def test_getAllProductsOfFollowerMaxRisk_007(self):
        datas={"followerMaxRisk": userData['followerMaxRisk3']}
        getAllProductsOfFollowerMaxRiskRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProductsOfFollowerMaxRiskRes.status_code,webAPIData['status_code_200'],'获取最大风险产品失败！')

        getAllProductsOfFollowerMaxRiskList=json.loads(getAllProductsOfFollowerMaxRiskRes.text)['data']['items']
        if len(getAllProductsOfFollowerMaxRiskList):
            for i in range(len(getAllProductsOfFollowerMaxRiskList)):
                self.assertEqual(getAllProductsOfFollowerMaxRiskList[i]['FollowerMaxRisk'],0.075,'获取最大风险<7.5%的数据错误！')

    '''获取最大风险<10%'''
    def test_getAllProductsOfFollowerMaxRisk_008(self):
        datas={"followerMaxRisk": userData['followerMaxRisk4']}
        getAllProductsOfFollowerMaxRiskRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProductsOfFollowerMaxRiskRes.status_code,webAPIData['status_code_200'],'获取最大风险产品失败！')

        getAllProductsOfFollowerMaxRiskList=json.loads(getAllProductsOfFollowerMaxRiskRes.text)['data']['items']
        if len(getAllProductsOfFollowerMaxRiskList):
            for i in range(len(getAllProductsOfFollowerMaxRiskList)):
                self.assertEqual(getAllProductsOfFollowerMaxRiskList[i]['FollowerMaxRisk'],0.1,'获取最大风险<10%的数据错误！')

    '''获取最大风险<12.5%'''
    def test_getAllProductsOfFollowerMaxRisk_009(self):
        datas={"followerMaxRisk": userData['followerMaxRisk5']}
        getAllProductsOfFollowerMaxRiskRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProductsOfFollowerMaxRiskRes.status_code,webAPIData['status_code_200'],'获取最大风险产品失败！')

        getAllProductsOfFollowerMaxRiskList=json.loads(getAllProductsOfFollowerMaxRiskRes.text)['data']['items']
        if len(getAllProductsOfFollowerMaxRiskList):
            for i in range(len(getAllProductsOfFollowerMaxRiskList)):
                self.assertEqual(getAllProductsOfFollowerMaxRiskList[i]['FollowerMaxRisk'],0.125,'获取最大风险<12.5%的数据错误！')

    '''获取最大风险<15%'''
    def test_getAllProductsOfFollowerMaxRisk_010(self):
        datas={"followerMaxRisk": userData['followerMaxRisk6']}
        getAllProductsOfFollowerMaxRiskRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProductsOfFollowerMaxRiskRes.status_code,webAPIData['status_code_200'],'获取最大风险产品失败！')

        getAllProductsOfFollowerMaxRiskList=json.loads(getAllProductsOfFollowerMaxRiskRes.text)['data']['items']
        if len(getAllProductsOfFollowerMaxRiskList):
            for i in range(len(getAllProductsOfFollowerMaxRiskList)):
                self.assertEqual(getAllProductsOfFollowerMaxRiskList[i]['FollowerMaxRisk'],0.15,'获取最大风险<15%的数据错误！')

    '''操作周期15天内'''
    def test_getAllProductsOfExpectDays_011(self):
        datas={"expectDays": userData['expectDays1']}
        getAllProductsOfExpectDaysRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProductsOfExpectDaysRes.status_code,webAPIData['status_code_200'],'获取操作周期15天内的产品失败！')

        getAllProductsOfExpectDaysList=json.loads(getAllProductsOfExpectDaysRes.text)['data']['items']
        if len(getAllProductsOfExpectDaysList):
            for i in range(len(getAllProductsOfExpectDaysList)):
                self.assertTrue(getAllProductsOfExpectDaysList[i]['ExpectDays'] < 15,'获取操作周期15天内的产品的数据错误！')

    '''操作周期15-30天内'''
    def test_getAllProductsOfExpectDays_012(self):

        datas={"expectDays": userData['expectDays2']}
        getAllProductsOfExpectDaysRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProductsOfExpectDaysRes.status_code,webAPIData['status_code_200'],'获取操作周期15-30天内的产品失败！')

        getAllProductsOfExpectDaysList=json.loads(getAllProductsOfExpectDaysRes.text)['data']['items']
        if len(getAllProductsOfExpectDaysList):
            for i in range(len(getAllProductsOfExpectDaysList)):
                self.assertTrue(15 <= getAllProductsOfExpectDaysList[i]['ExpectDays'] and getAllProductsOfExpectDaysList[i]['ExpectDays'] < 30 ,'获取操作周期15-30天内的产品的数据错误！')

    '''操作周期30-60天内'''
    def test_getAllProductsOfExpectDays_013(self):

        datas={"expectDays": userData['expectDays3']}
        getAllProductsOfExpectDaysRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProductsOfExpectDaysRes.status_code,webAPIData['status_code_200'],'获取操作周期30-60天内的产品失败！')

        getAllProductsOfExpectDaysList=json.loads(getAllProductsOfExpectDaysRes.text)['data']['items']
        if len(getAllProductsOfExpectDaysList):
            for i in range(len(getAllProductsOfExpectDaysList)):
                self.assertTrue(30 <= getAllProductsOfExpectDaysList[i]['ExpectDays'] and getAllProductsOfExpectDaysList[i]['ExpectDays'] < 60 ,'获取操作周期15-30天内的产品的数据错误！')

    '''操作周期60-90天内'''
    def test_getAllProductsOfExpectDays_014(self):
        datas = {"expectDays": userData['expectDays4']}
        getAllProductsOfExpectDaysRes = MAM.getAllProducts(userData['hostName'] + userDataMAMUrl['getAllProducts_url'],
                                                           headers=webAPIData['headers'], params=datas)
        self.assertEqual(getAllProductsOfExpectDaysRes.status_code, webAPIData['status_code_200'],
                         '获取操作周期60-90天内的产品失败！')

        getAllProductsOfExpectDaysList = json.loads(getAllProductsOfExpectDaysRes.text)['data']['items']
        if len(getAllProductsOfExpectDaysList):
            for i in range(len(getAllProductsOfExpectDaysList)):
                self.assertTrue(
                    60 <= getAllProductsOfExpectDaysList[i]['ExpectDays'] and getAllProductsOfExpectDaysList[i][
                        'ExpectDays'] < 90, '获取操作周期60-90天内的产品的数据错误！')

    '''最低参与资金5k-1w'''
    def test_getAllProductsOfMinFollowBalance_015(self):
        datas = {"minFollowBalance": userData['minFollowBalance1']}
        getAllProductsOfMinFollowBalanceRes = MAM.getAllProducts(userData['hostName'] + userDataMAMUrl['getAllProducts_url'],
                                                           headers=webAPIData['headers'], params=datas)
        self.assertEqual(getAllProductsOfMinFollowBalanceRes.status_code, webAPIData['status_code_200'],
                         '获取最低参与资金5k-1w的产品失败！')
        getAllProductsOfMinFollowBalanceList = json.loads(getAllProductsOfMinFollowBalanceRes.text)['data']['items']
        if len(getAllProductsOfMinFollowBalanceList):
            for i in range(len(getAllProductsOfMinFollowBalanceList)):
                self.assertTrue(
                    5000 <= getAllProductsOfMinFollowBalanceList[i]['MinFollowBalance'] and getAllProductsOfMinFollowBalanceList[i][
                        'MinFollowBalance'] < 10000, '获取最低参与资金5k-1w的产品的数据错误！')

    '''最低参与资金1w-3w'''
    def test_getAllProductsOfMinFollowBalance_016(self):
        datas = {"minFollowBalance": userData['minFollowBalance2']}
        getAllProductsOfMinFollowBalanceRes = MAM.getAllProducts(
            userData['hostName'] + userDataMAMUrl['getAllProducts_url'],
            headers=webAPIData['headers'], params=datas)
        self.assertEqual(getAllProductsOfMinFollowBalanceRes.status_code, webAPIData['status_code_200'],
                         '获取最低参与资金1w-3w的产品失败！')
        getAllProductsOfMinFollowBalanceList = json.loads(getAllProductsOfMinFollowBalanceRes.text)['data']['items']
        if len(getAllProductsOfMinFollowBalanceList):
            for i in range(len(getAllProductsOfMinFollowBalanceList)):
                self.assertTrue(
                    10000 <= getAllProductsOfMinFollowBalanceList[i]['MinFollowBalance'] and
                    getAllProductsOfMinFollowBalanceList[i][
                        'MinFollowBalance'] < 30000, '获取最低参与资金1w-3w的产品的数据错误！')

    '''最低参与资金3w-5w'''
    def test_getAllProductsOfMinFollowBalance_017(self):
        datas = {"minFollowBalance": userData['minFollowBalance3']}
        getAllProductsOfMinFollowBalanceRes = MAM.getAllProducts(
            userData['hostName'] + userDataMAMUrl['getAllProducts_url'],
            headers=webAPIData['headers'], params=datas)
        self.assertEqual(getAllProductsOfMinFollowBalanceRes.status_code, webAPIData['status_code_200'],
                         '获取最低参与资金3w-5w的产品失败！')
        getAllProductsOfMinFollowBalanceList = json.loads(getAllProductsOfMinFollowBalanceRes.text)['data']['items']
        if len(getAllProductsOfMinFollowBalanceList):
            for i in range(len(getAllProductsOfMinFollowBalanceList)):
                self.assertTrue(
                    30000 <= getAllProductsOfMinFollowBalanceList[i]['MinFollowBalance'] and
                    getAllProductsOfMinFollowBalanceList[i][
                        'MinFollowBalance'] < 50000, '获取最低参与资金3w-5w的产品的数据错误！')

    '''最低参与资金5w-10w'''
    def test_getAllProductsOfMinFollowBalance_018(self):
        datas = {"minFollowBalance": userData['minFollowBalance4']}
        getAllProductsOfMinFollowBalanceRes = MAM.getAllProducts(
            userData['hostName'] + userDataMAMUrl['getAllProducts_url'],
            headers=webAPIData['headers'], params=datas)
        self.assertEqual(getAllProductsOfMinFollowBalanceRes.status_code, webAPIData['status_code_200'],
                         '获取最低参与资金5w-10w的产品失败！')
        getAllProductsOfMinFollowBalanceList = json.loads(getAllProductsOfMinFollowBalanceRes.text)['data']['items']
        if len(getAllProductsOfMinFollowBalanceList):
            for i in range(len(getAllProductsOfMinFollowBalanceList)):
                self.assertTrue(
                    50000 <= getAllProductsOfMinFollowBalanceList[i]['MinFollowBalance'] and
                    getAllProductsOfMinFollowBalanceList[i][
                        'MinFollowBalance'] < 100000, '获取最低参与资金5w-10w的产品的数据错误！')

    '''最低参与资金10w-20w'''
    def test_getAllProductsOfMinFollowBalance_019(self):
        datas = {"minFollowBalance": userData['minFollowBalance5']}
        getAllProductsOfMinFollowBalanceRes = MAM.getAllProducts(
            userData['hostName'] + userDataMAMUrl['getAllProducts_url'],
            headers=webAPIData['headers'], params=datas)
        self.assertEqual(getAllProductsOfMinFollowBalanceRes.status_code, webAPIData['status_code_200'],
                         '获取最低参与资金10w-20w的产品失败！')
        getAllProductsOfMinFollowBalanceList = json.loads(getAllProductsOfMinFollowBalanceRes.text)['data']['items']
        if len(getAllProductsOfMinFollowBalanceList):
            for i in range(len(getAllProductsOfMinFollowBalanceList)):
                self.assertTrue(
                    100000 <= getAllProductsOfMinFollowBalanceList[i]['MinFollowBalance'] and
                    getAllProductsOfMinFollowBalanceList[i][
                        'MinFollowBalance'] < 200000, '获取最低参与资金10w-20w的产品的数据错误！')

    '''最低参与资金20w以上'''
    def test_getAllProductsOfMinFollowBalance_020(self):
        datas = {"minFollowBalance": userData['minFollowBalance6']}
        getAllProductsOfMinFollowBalanceRes = MAM.getAllProducts(
            userData['hostName'] + userDataMAMUrl['getAllProducts_url'],
            headers=webAPIData['headers'], params=datas)
        self.assertEqual(getAllProductsOfMinFollowBalanceRes.status_code, webAPIData['status_code_200'],
                         '获取最低参与资金20w以上的产品失败！')
        getAllProductsOfMinFollowBalanceList = json.loads(getAllProductsOfMinFollowBalanceRes.text)['data']['items']
        if len(getAllProductsOfMinFollowBalanceList):
            for i in range(len(getAllProductsOfMinFollowBalanceList)):
                self.assertTrue(
                    200000 <= getAllProductsOfMinFollowBalanceList[i]['MinFollowBalance'],
                    '获取最低参与资金20w以上的产品的数据错误！')

    '''获取发布中产品的收益分配比例2:8'''
    def test_getAllProductsOfProfitRatio_021(self):
        datas={"status": userData['status_Pending'],"profitRatio": userData['profitRatio1']}
        getAllProductsOfProfitRatioRes=MAM.getAllProducts(userData['hostName']+userDataMAMUrl['getAllProducts_url'],headers=webAPIData['headers'],params=datas)
        self.assertEqual(getAllProductsOfProfitRatioRes.status_code,webAPIData['status_code_200'],'获取产品收益分配比例为2:8失败！')
        getAllProductsOfProfitRatioList=json.loads(getAllProductsOfProfitRatioRes.text)['data']['items']
        if len(getAllProductsOfProfitRatioList):
            for i in range(len(getAllProductsOfProfitRatioList)):
                self.assertEqual(getAllProductsOfProfitRatioList[i]['Status'],userData['status_Pending'],'获取发布中的产品数据状态非Pending状态')
                self.assertEqual(getAllProductsOfProfitRatioList[i]['ProfitMode']['TakeProfitRatio'],userData['takeProfitRatio1'],'获取产品收益分配比例数据非2:8产品！')
                self.assertEqual(getAllProductsOfProfitRatioList[i]['ProfitMode']['StopLossRatio'],userData['stopLossRatio1'],'获取产品收益分配比例数据非2:8产品！')

    '''获取进行中产品，验证排序功能'''
    def test_getAllProductsOfFilter_022(self):
        datas = {"pageIndex": userData['getAllProuductPageIndex'],"pageSize": userData['getAllProuductPageSize'],"status": userData['status_InProcess']}
        productStatus = ''
        roi=0
        dt=''
        getAllProductsOfFilterRes = MAM.getAllProducts(userData['hostName'] + userDataMAMUrl['getAllProducts_url'],
                                                            headers=webAPIData['headers'], params=datas)
        self.assertEqual(getAllProductsOfFilterRes.status_code, webAPIData['status_code_200'], '获取产品收益分配比例为2:8失败！')
        getAllProductsOfFilterList = json.loads(getAllProductsOfFilterRes.text)['data']['items']
        if len(getAllProductsOfFilterList):
            for i in range(len(getAllProductsOfFilterList)):
                self.assertIn(getAllProductsOfFilterList[i]['Status'],userData['status_Pending'] + ',' + userData['status_Trading'],
                              '获取进行中的产品数据非InProcess状态')
                if productStatus == userData['status_Trading']:
                    self.assertEqual(getAllProductsOfFilterList[i]['Status'], userData['status_Trading'],
                                     '获取进行中的产品状态排序错误！')
                    self.assertTrue(getAllProductsOfFilterList[i]['ROI'] <= roi,'获取进行中正在交易中的产品排序错误！')
                productStatus = getAllProductsOfFilterList[i]['Status']
                roi = getAllProductsOfFilterList[i]['ROI']

    '''获取进行中 2：8 产品，最大风险<1%,操作周期15天内，最低参与资金5千-1w的产品'''
    def test_getAllProductsOfFilter_023(self):
        datas = {"status": userData['status_InProcess'], "profitRatio": userData['profitRatio1'],"followerMaxRisk":userData['followerMaxRisk1'],"expectDays":userData['expectDays1'],
                 "minFollowBalance":userData['minFollowBalance1']}
        getAllProductsOfFilterRes = MAM.getAllProducts(userData['hostName'] + userDataMAMUrl['getAllProducts_url'],
                                                            headers=webAPIData['headers'], params=datas)
        self.assertEqual( getAllProductsOfFilterRes.status_code, webAPIData['status_code_200'], '获取产品收益分配比例为2:8失败！')
        getAllProductsOfFilterList = json.loads( getAllProductsOfFilterRes.text)['data']['items']
        if len(getAllProductsOfFilterList):
            for i in range(len(getAllProductsOfFilterList)):
                self.assertIn(getAllProductsOfFilterList[i]['Status'],userData['status_Pending']+','+userData['status_Trading'],
                                 '获取进行中的产品数据非InProcess状态')
                self.assertEqual(getAllProductsOfFilterList[i]['ProfitMode']['TakeProfitRatio'],
                                 userData['takeProfitRatio1'], '获取产品收益分配比例数据非2:8产品！')
                self.assertEqual(getAllProductsOfFilterList[i]['ProfitMode']['StopLossRatio'],
                                 userData['stopLossRatio1'], '获取产品收益分配比例数据非2:8产品！')
                self.assertEqual(getAllProductsOfFilterList[i]['FollowerMaxRisk'], 0.01, '获取最大风险<1%的数据错误！')
                self.assertTrue(getAllProductsOfFilterList[i]['ExpectDays'] < 15, '获取操作周期15天内的产品的数据错误！')
                self.assertTrue(5000 <= getAllProductsOfFilterList[i]['MinFollowBalance'] and
                                getAllProductsOfFilterList[i]['MinFollowBalance'] < 10000, '获取最低参与资金5k-1w的产品的数据错误！')

    '''获取已结束的产品'''
    def test_getAllProductsOfSettled_024(self):
        datas = {"status": userData['status_Settled']}
        getAllProductsOfSettledRes = MAM.getAllProducts(userData['hostName'] + userDataMAMUrl['getAllProducts_url'],
                                                       headers=webAPIData['headers'], params=datas)
        self.assertEqual(getAllProductsOfSettledRes.status_code, webAPIData['status_code_200'], '获取已结束的产品失败！')
        getAllProductsOfSettledList = json.loads(getAllProductsOfSettledRes.text)['data']['items']
        if len(getAllProductsOfSettledList):
            for i in range(len(getAllProductsOfSettledList)):
                self.assertEqual(getAllProductsOfSettledList[i]['Status'], userData['status_Settled'],
                                 '获取发布中的产品数据状态非Settled状态')

    '''获取已结束产品筛选最终收益10%以内'''
    def test_getAllProductsOfSettled_025(self):
        datas = {"status": userData['status_Settled'],"roi": userData['roi1']}
        getAllProductsOfSettledRes = MAM.getAllProducts(userData['hostName'] + userDataMAMUrl['getAllProducts_url'],
                                                        headers=webAPIData['headers'], params=datas)
        self.assertEqual(getAllProductsOfSettledRes.status_code, webAPIData['status_code_200'], '获取已结束的产品失败！')
        getAllProductsOfSettledList = json.loads(getAllProductsOfSettledRes.text)['data']['items']
        if len(getAllProductsOfSettledList):
            for i in range(len(getAllProductsOfSettledList)):
                self.assertEqual(getAllProductsOfSettledList[i]['Status'], userData['status_Settled'],
                                 '获取发布中的产品数据状态非Settled状态')
                self.assertTrue(getAllProductsOfSettledList[i]['ROI'] < 0.1,'获取结束中最终收益率10%以内数据错误！')

    def tearDown(self):
            print('End！')

if __name__ == '__main__':
    unittest.main()