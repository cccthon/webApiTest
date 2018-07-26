#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_blogShare
# 用例标题: 分享微博
# 流程：
    #1、登录
    #2、发布微博
    #3、获取微博全部动态
    #4、获取热门推荐
    #5、按推荐位获取热门推荐
    #6、分享微博
    #7、删除微博
# 脚本作者: zhangyanyun
# 写作日期: 2018/06/28
#=========================================================

import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,newSocial,FMCommon,Http
from requests_toolbelt.multipart import MultipartEncoder

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadnewSocialYML()
authData=FMCommon.loadAuthYML()

class Blog(unittest.TestCase):
    def setUp(self):
        #登录账号
        siginParams= {"account": userData['account'], "password": userData['passwd'], "remember": False}
        siginRes=Auth.signin(userData['hostName']+authData['signin_url'],headers = userData['headers'],datas = siginParams)
        #断言返回200登录成功
        self.assertEqual(siginRes.status_code,userData['status_code_200'])
        #获取headers
        self.token=json.loads(siginRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})


    def test_getAllBlog001(self):
        #获取全部微博动态
        '''发纯文字短微博'''
        blogParams={"isLongBlog": False,                     #boolean  true表示长微博，false表示短微博
                    "body": "test short blog test",          #短微博内容
                    "blogType": 0,                           #微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
                    "symbol": "",
                    "postType": 0                            #发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
                   }
        shortBlogRes=newSocial.addBlog(userData['hostName']+socialData['addBlog_url'],headers = self.headers,datas = blogParams)
        #断言返回200，发布微博成功
        self.assertEqual(shortBlogRes.status_code,userData['status_code_200'],"微博发布失败")
        #获取微博id,用于删除微博
        shortBlogId=json.loads(shortBlogRes.text)['data']['ObjectId']

        #休眠2秒后再获取我的微博
        time.sleep(2)
        #微博发布成功，检查微博全部动态
        params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
        getAllBlog=newSocial.getAllBlog(userData['hostName']+socialData['getMyBlogs_url'],headers=self.headers)
        #断言返回200，code=0,获取微博列表成功
        self.assertEqual(getAllBlog.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getAllBlog.text)['code'],0)
        # 获取微博动态第一条微博id
        blogId=json.loads(getAllBlog.text)['data']['Items'][0]['Id']
        #断言，微博动态第一条微博id等于刚发布的短微博id
        self.assertEqual(blogId,shortBlogId)
        #删除微博
        delBlogRes=newSocial.delBlogById(userData['hostName']+socialData['delBlogById_url']+str(shortBlogId),headers = self.headers)
        self.assertEqual(delBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(delBlogRes.text)['code'],0)

    def test_blogShare002(self):
        #分享微博
        '''发纯文字短微博'''
        blogParams={"isLongBlog": False,                     #boolean  true表示长微博，false表示短微博
                    "body": "test short blog test",          #短微博内容
                    "blogType": 0,                           #微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
                    "symbol": "",
                    "postType": 0                            #发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
                   }
        shortBlogRes=newSocial.addBlog(userData['hostName']+socialData['addBlog_url'],headers = self.headers,datas = blogParams)
        #断言返回200，发布微博成功
        self.assertEqual(shortBlogRes.status_code,userData['status_code_200'],"微博发布失败")
        #获取微博id,用于删除微博
        shortBlogId=json.loads(shortBlogRes.text)['data']['ObjectId']

        #休眠2秒后再获取我的微博
        time.sleep(2)
        #微博发布成功，检查微博全部动态
        params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
        getAllBlog=newSocial.getAllBlog(userData['hostName']+socialData['getMyBlogs_url'],headers=self.headers)
        #断言返回200，code=0,获取微博列表成功
        self.assertEqual(getAllBlog.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getAllBlog.text)['code'],0)
        # 获取微博动态第一条微博id
        blogId=json.loads(getAllBlog.text)['data']['Items'][0]['Id']
        #断言，微博动态第一条微博id等于刚发布的短微博id
        self.assertEqual(blogId,shortBlogId)
        #分享微博
        blogShare = newSocial.blogShare(userData['hostName']+socialData['blogShare_url']+str(shortBlogId),headers=self.headers)
        #删除微博
        delBlogRes=newSocial.delBlogById(userData['hostName']+socialData['delBlogById_url']+str(shortBlogId),headers = self.headers)
        self.assertEqual(delBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(delBlogRes.text)['code'],0)

    def test_getHotBlog003(self):
        #检查获取热门微博
        params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
        getAllBlog=newSocial.getHotBlog(userData['hostName']+socialData['getHotBlog_url'],headers=self.headers)
        #断言返回200，code=0,获取热门微博列表成功
        self.assertEqual(getAllBlog.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getAllBlog.text)['code'],0)
        #热门微博排序规则

    def test_getBlogByLocation004(self):
        #按推荐位获取热门推荐 ,现在首页和个人中心都没用到这个接口，只有微博详情页
        params={"pageIndex":1,"pageSize":15,"location":2}  #有默认值可以不用传参,推荐位（location）：1：首页；2：微博详情；3：个人中心；
        getBlogByLocation=newSocial.getBlogByLocation(userData['hostName']+socialData['getBlogByLocation_url'],params=params,headers=self.headers,)
        #断言返回200，code=0,获取热门微博列表成功
        self.assertEqual(getBlogByLocation.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getBlogByLocation.text)['code'],0)


    def tearDown(self):

        #清空测试环境
        #退出登录
        signOutRes=Auth.signout(userData['hostName']+ authData['signout_url'],datas = self.headers)
        self.assertEqual(signOutRes.status_code,userData['status_code_200'])

if __name__=='__main__':
    unittest.main()
