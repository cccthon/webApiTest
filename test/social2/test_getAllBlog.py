#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
#  用例名称:FM_WebAPI_newSocial_getAllBlog
#  用例标题:汇友圈获取不同tab列表
#  预置条件:
#  测试步骤:
#    1.获取所有微博动态，2.获取热门微博，3.获取热门推荐，4.获取不同PostType类型微博
# 5.获取微博详情，6.获取公告banner列表
#  预期结果:
#    检查响应码为：200
#  脚本作者:liujifeng
#  写作日期:20180628
#  修改人：
#  修改日期：
#=========================================================

import sys, unittest, json,unittest

sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth, FMCommon, Account,newSocial,Http,time
from socketIO_client import SocketIO
from base64 import b64encode

webAPIData = FMCommon.loadWebAPIYML()
authData = FMCommon.loadAuthYML()
userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadnewSocialYML()


class Signin(unittest.TestCase):
    def setUp(self):
        pass

    def test_signin(self):
        '''登录followme系统'''
        datas = {"account": webAPIData['account'], "password": webAPIData['passwd'], "remember": "false"}
        signinRes = Auth.signin(webAPIData['hostName'] + authData['signin_url'], webAPIData['headers'], datas)
        '''登录成功，返回200 ok'''
        self.assertEqual(signinRes.status_code, webAPIData['status_code_200'])
        # 保存登录时的token，待登出使用
        self.token = json.loads(signinRes.text)['data']['token']
        # 规整headers
        webAPIData['headers'][webAPIData['Authorization']] = webAPIData['Bearer'] + self.token

        #1、获取所有微博动态
        getAllBlogRes=newSocial.getAllBlog(userData['hostName']+socialData['getAllBlog_url'],headers = webAPIData['headers'])
        #断言返回200，code=0,获取所有微博动态成功
        self.assertEqual(getAllBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getAllBlogRes.text)['code'],0)


        #2、获取热门微博
        getHotBlogRes=newSocial.getHotBlog(userData['hostName']+socialData['getHotBlog_url'],headers = webAPIData['headers'])
        #断言返回200，code=0,获取所有微博动态成功
        self.assertEqual(getHotBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getHotBlogRes.text)['code'],0)

        #3、按推荐位获取热门推荐-微博详情页
        # 推荐位  1 - 首页 2 - 微博详情 3 - 个人中心
        location = '2'
        getBlogByLocationRes=newSocial.getBlogByLocation(userData['hostName']+socialData['getBlogByLocation_url']+location,headers = webAPIData['headers'])
        #断言返回200，code=0,获取所有微博动态成功
        self.assertEqual(getBlogByLocationRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getBlogByLocationRes.text)['code'],0)

        #4、根据PostType类型获取相应的微博
        # 发布类型0：用户微博 1：推广 2：认证用户微博 3：名人大咖 4：分析师 5：媒体号 6：经纪商  默认值: 0
        type = '3'
        getBlogByPostTypeRes=newSocial.getBlogByPostType(userData['hostName']+socialData['getBlogByPostType_url']+type, headers = webAPIData['headers'])
        #断言返回200，code=0,根据PostType类型获取相应的微博成功
        self.assertEqual(getBlogByPostTypeRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getBlogByPostTypeRes.text)['code'],0)
        self.LastId = json.loads(getBlogByPostTypeRes.text)['data']['LastId']
        print('LastId:', self.LastId)

        #6、获取公告banner列表
        getNoticeListRes=newSocial.getNoticeList(userData['hostName']+socialData['getNoticeList_url'],headers = webAPIData['headers'])
        #断言返回200，code=0,获取公告banner列表
        self.assertEqual(getNoticeListRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getNoticeListRes.text)['code'],0)

        # #7、获取微博最后ID
        # # 类型：0 - 全部动态，1 - 热门微博，2 - 交易动态，3 - 品种咨询，4 - 大咖秀，5 - 评论分析，6 - 经纪商动态  默认值: 0
        # par = {"type ": 3}
        # getLastIdRes=newSocial.getLastId(userData['hostName']+socialData['getLastId_url'],params = par,headers = webAPIData['headers'])
        # #断言返回200，code=0,获取微博最后ID成功
        # self.assertEqual(getLastIdRes.status_code,userData['status_code_200'])
        # self.assertEqual(json.loads(getLastIdRes.text)['code'],0)

        # 8、获取全局提醒列表[需要登录]
        getGlobalRemindRes = newSocial.getGlobalRemind(userData['hostName'] + socialData['getGlobalRemind_url'],
                                             headers=webAPIData['headers'])
        # 断言返回200，code=0,获取全局提醒列表成功
        self.assertEqual(getGlobalRemindRes.status_code, userData['status_code_200'])
        self.assertEqual(json.loads(getGlobalRemindRes.text)['code'], 0)

        # 9、获取财经要闻
        getFinanceListRes = newSocial.getFinanceList(userData['hostName'] + socialData['getFinanceList_url'],
                                             headers=webAPIData['headers'])
        # 断言返回200，code=0,获取财经要闻成功
        self.assertEqual(getFinanceListRes.status_code, userData['status_code_200'])
        self.assertEqual(json.loads(getFinanceListRes.text)['code'], 0)

        # 10、获取财经要闻页的热门推荐
        getHotRecommendListRes = newSocial.getHotRecommendList(userData['hostName'] + socialData['getHotRecommendList_url'],
                                             headers=webAPIData['headers'])
        # 断言返回200，code=0,获取财经要闻页的热门推荐成功
        self.assertEqual(getHotRecommendListRes.status_code, userData['status_code_200'])
        self.assertEqual(json.loads(getHotRecommendListRes.text)['code'], 0)


    # def test_addShortBlog003(self):
        '''发带品种标签的短微博'''
        blogParams = {"isLongBlog": False,  # boolean  true表示长微博，false表示短微博
                      "body": "$AUD/JPY$ test1",  # 短微博内容
                      "blogType": 0,  # 微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
                      "symbol": "",
                      "postType": 0  # 发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
                      }
        addShortBlogRes = newSocial.addBlog(userData['hostName'] + socialData['addBlog_url'], headers=webAPIData['headers'],
                                            datas=blogParams)
        # 断言返回200，发微博成功，code=0发微博成功
        self.assertEqual(addShortBlogRes.status_code, userData['status_code_200'])
        self.assertEqual(json.loads(addShortBlogRes.text)['code'], 0)
        # 获取微博id,用于删除微博
        blogId = json.loads(addShortBlogRes.text)['data']['ObjectId']

        #5、获取微博详情
        # id = blogId
        getBlogDetailRes=newSocial.getBlogDetail(userData['hostName']+socialData['getBlogDetail_url']+str(blogId)+'/detail',headers = webAPIData['headers'])
        #断言返回200，code=0,获取微博详情成功
        self.assertEqual(getBlogDetailRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getBlogDetailRes.text)['code'],0)

        # BlogDetailId = json.loads(getBlogDetailRes.text)['data']['BlogInfo']['Id']
        # # BlogDetailId = []
        # # for i in BlogDetail:
        # #     BlogDetailId.append(i['Id'])
        # self.assertIn(blogId, BlogDetailId)

        # #11、分享微博
        # blogShareRes=newSocial.blogShare(userData['hostName']+socialData['blogShare_url']+str(blogId),headers = webAPIData['headers'])
        # #断言返回200，code=0,分享成功
        # self.assertEqual(blogShareRes.status_code,userData['status_code_200'])
        # self.assertEqual(json.loads(blogShareRes.text)['code'],0)

        # 获取品种资讯列表
        # userData['type']博客类型：0-普通微博，1-公告，2-品种资讯，3-交易动态
        time.sleep(2)
        symbolBlogRes = newSocial.getBlogByType(
            userData['hostName'] + socialData['getBlogByType_url'] + str(userData['type']), headers=webAPIData['headers'])

        # 断言返回200，code=0,获取品种列表成功
        self.assertEqual(symbolBlogRes.status_code, userData['status_code_200'])
        self.assertEqual(json.loads(symbolBlogRes.text)['code'], 0)
        # 获取品种资讯列表所有微博,断言，刚发布的品种微博存在于品种资讯列表中
        listBlog = json.loads(symbolBlogRes.text)['data']['Items']
        listBlogId = []
        for i in listBlog:
            listBlogId.append(i['Id'])
        self.assertIn(blogId, listBlogId)

        # 删除微博
        delBlogRes = newSocial.delBlogById(userData['hostName'] + socialData['delBlogById_url'] + str(blogId),
                                           headers=webAPIData['headers'])
        self.assertEqual(delBlogRes.status_code, userData['status_code_200'])
        self.assertEqual(json.loads(delBlogRes.text)['code'], 0)

    def tearDown(self):
        # 清空测试环境，还原测试数据
        # 登出followme系统
        signoutRes = Auth.signout(webAPIData['hostName'] + authData['signout_url'], datas=webAPIData['headers'])
        self.assertEqual(signoutRes.status_code, webAPIData['status_code_200'])


if __name__ == '__main__':
    unittest.main()

