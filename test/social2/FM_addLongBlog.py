#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_addLongBlog
# 用例标题: 发长微博（1、文字+本地图片长微博 2、文字+网络图片长微博 3、文字+内嵌视频长微博）
# 流程：
    #1、登录
    #2、发布微博
    #3、我的微博列表


import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
from requests_toolbelt.multipart import MultipartEncoder
import Auth,newSocial,FMCommon,Http,time

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadnewSocialYML()
authData=FMCommon.loadAuthYML()

class AddLongBlog(unittest.TestCase):
    def setUp(self):
        #登录账号
        siginParams= {"account": userData['account'], "password": userData['passwd'], "remember": False}
        siginRes=Auth.signin(userData['hostName']+authData['signin_url'],headers = userData['headers'],datas = siginParams)
        #断言返回200登录成功
        self.assertEqual(siginRes.status_code,userData['status_code_200'])
        #获取headers
        self.token=json.loads(siginRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})
        print("self.headers",self.headers)

    # def test_addLongBlog001(self):
    #     '''发布长微博：文字+本地图片'''
    #     #先上传图片
    #     # m={'pic': ('image.gif', open("../../file/image.gif", 'rb'), 'image/gif')}    #这样上传文件post中用files，但是文件太大，选择用数据流传送MultipartEncoder
    #     m = MultipartEncoder(fields = { "pic": ("image.jpg", open("../../file/image.jpg", "rb"), "image/jpeg")})
    #     print("m",m)
    #     print("m.content")
    #     self.headers['Content-Type'] = m.content_type
    #     print("self.headers",self.headers)
    #     # self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})
    #     print("self.headers",self.headers)
    #     #上传图片
    #     imageRes=requests.post(userData['hostName']+socialData['singleFileUpload_url'],data = m,headers = self.headers)
    #     print(userData['hostName']+socialData['singleFileUpload_url'])
    #     # headers = dict(('content-type' : m.content),**{userData['Authorization'] : userData['Bearer']+self.token})
    #     print("headers",self.headers)
    #     print("imageRes",imageRes.text)
    #     #断言返回200，上传图片成功，返回code=0,上传图片成功
    #     self.assertEqual(imageRes.status_code,userData['status_code_200'])
    #     self.assertEqual(json.loads(imageRes.text)['code'],0)
    #     #获取上传图片的url,用于发微博
    #     imageUrl=json.loads(imageRes.text)['data']
    #     imageUrl['ContentType']='jpg'
    #     listImage=[]
    #     listImage.append(imageUrl)
    #     print("imageUrl",imageUrl)
    
    #     blogParams={"isLongBlog": True,                     #boolean  true表示长微博，false表示短微博
    #                 "longBody": "test longBlog test longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
    #                             "longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest"
    #                             " longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
    #                             "longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
    #                             "longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
    #                             "longBlogtest longBlog </p><p><img src="+imageUrl['url']+" /> </p>",     #长微博内容
    #                 "longTitle": "longBlog Title",          #长微博标题
    #                 "longIntro": "longBlog Intro",          #长微博导语
    #                 "blogType": 0,                          #微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
    #                 #"files": listImage,
    #                 "symbol": "",
    #                 "postType": 0                           #发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
    #                }

    #     self.headers['Content-Type'] = "application/json; charset=utf-8"
    #     longBlogRes=newSocial.addBlog(userData['hostName']+socialData['addBlog_url'],datas = blogParams, headers = self.headers)
    #     #断言返回200，code=0，发布微博成功
    #     self.assertEqual(longBlogRes.status_code,userData['status_code_200'])
    #     self.assertEqual(json.loads(longBlogRes.text)['code'],0)
    #     #获取微博id，用于删除微博
    #     longBlogId=json.loads(longBlogRes.text)['data']['ObjectId']
    
    #     #检查我的微博列表
    #     time.sleep(2)
    #     # params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
    #     getMyBlogsRes=newSocial.getMyBlogs(userData['hostName']+socialData['getMyBlogs_url'],headers = self.headers)
    #     print(userData['hostName']+socialData['getMyBlogs_url'])
    #     #断言返回200，code=0,获取我的微博列表成功
    #     self.assertEqual(getMyBlogsRes.status_code,userData['status_code_200'])
    #     self.assertEqual(json.loads(getMyBlogsRes.text)['code'],0)
    
    #     #断言，我的微博列表第一条微博为刚发布的微博
    #     blogId=json.loads(getMyBlogsRes.text)['data']['Items'][0]['Id']
    #     self.assertEqual(longBlogId,blogId)
    
    #     #删除微博
    #     delBlogRes=newSocial.delBlogById(userData['hostName']+socialData['delBlogById_url']+str(longBlogId),headers = self.headers)
    #     self.assertEqual(delBlogRes.status_code,userData['status_code_200'])
    #     self.assertEqual(json.loads(delBlogRes.text)['code'],0)


    # def test_addLongBlog002(self):
    #     '''发布长微博：文字+网络图片'''
    #     imageUrl="https://www.baidu.com/img/bd_logo1.png"
    #     blogParams = {"isLongBlog": True,  # boolean  true表示长微博，false表示短微博
    #                   "longBody": "<p> test longBlog test longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
    #                               "longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest"
    #                               " longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
    #                               "longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
    #                               "longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
    #                               "longBlogtest longBlog </p><p><img src="+imageUrl+" /> </p>",  # 长微博内容
    #                   "longTitle": "longBlog Title",  # 长微博标题
    #                   "longIntro": "longBlog Intro",  # 长微博导语
    #                   "blogType": 0,  # 微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
    #                   "symbol": "",
    #                   "postType": 0   # 发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
    #                   }
    #     longBlogRes=newSocial.addBlog(userData['hostName']+socialData['addBlog_url'],datas = blogParams, headers = self.headers)
    #     #断言返回200，code=0，发布微博成功
    #     self.assertEqual(longBlogRes.status_code,userData['status_code_200'])
    #     self.assertEqual(json.loads(longBlogRes.text)['code'],0)
    #     #获取微博id,用于删除微博
    #     longBlogId=json.loads(longBlogRes.text)['data']['ObjectId']

    #     #检查我的微博列表
    #     time.sleep(2)
    #     # params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
    #     getMyBlogsRes=newSocial.getMyBlogs(userData['hostName']+socialData['getMyBlogs_url'],headers = self.headers)
    #     #断言返回200，code=0,获取我的微博列表成功
    #     self.assertEqual(getMyBlogsRes.status_code,userData['status_code_200'])
    #     self.assertEqual(json.loads(getMyBlogsRes.text)['code'],0)

    #     #断言，我的微博列表第一条微博为刚发布的微博
    #     blogId=json.loads(getMyBlogsRes.text)['data']['Items'][0]['Id']
    #     self.assertEqual(longBlogId,blogId)

    #     #删除微博
    #     delBlogRes=newSocial.delBlogById(userData['hostName']+socialData['delBlogById_url']+str(longBlogId),headers = self.headers)
    #     self.assertEqual(delBlogRes.status_code,userData['status_code_200'])
    #     self.assertEqual(json.loads(delBlogRes.text)['code'],0)


    # def test_addLongBlog003(self):
    #     '''发布长微博：文字+内嵌视频'''
    #     tvUrl="<iframe height=498 width=510 src='https://player.youku.com/embed/XMzI1MjQxMjQxMg==' frameborder=0 'allowfullscreen'></iframe>"
    #     blogParams = {"isLongBlog": True,  # boolean  true表示长微博，false表示短微博
    #                   "longBody": "<p> test longBlog test longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
    #                               "longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest"
    #                               " longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
    #                               "longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
    #                               "longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
    #                               "longBlogtest longBlog </p><p>"+tvUrl+"  </p>",  # 长微博内容
    #                   "longTitle": "longBlog Title",  # 长微博标题
    #                   "longIntro": "longBlog Intro",  # 长微博导语
    #                   "blogType": 0,  # 微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
    #                   "symbol": "",
    #                   "postType": 0   # 发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
    #                   }
    #     longBlogRes=newSocial.addBlog(userData['hostName']+socialData['addBlog_url'],datas = blogParams, headers = self.headers)
    #     #断言返回200，code=0，发布微博成功
    #     self.assertEqual(longBlogRes.status_code,userData['status_code_200'])
    #     self.assertEqual(json.loads(longBlogRes.text)['code'],0)
    #     #获取微博id,用于删除微博
    #     longBlogId=json.loads(longBlogRes.text)['data']['ObjectId']

    #     #检查我的微博列表
    #     time.sleep(2)
    #     # params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
    #     getMyBlogsRes=newSocial.getMyBlogs(userData['hostName']+socialData['getMyBlogs_url'],headers = self.headers)
    #     #断言返回200，code=0,获取我的微博列表成功
    #     self.assertEqual(getMyBlogsRes.status_code,userData['status_code_200'])
    #     self.assertEqual(json.loads(getMyBlogsRes.text)['code'],0)

    #     #断言，我的微博列表第一条微博为刚发布的微博
    #     blogId=json.loads(getMyBlogsRes.text)['data']['Items'][0]['Id']
    #     self.assertEqual(longBlogId,blogId)

    #     #删除微博
    #     delBlogRes=newSocial.delBlogById(userData['hostName']+socialData['delBlogById_url']+str(longBlogId),headers = self.headers)
    #     self.assertEqual(delBlogRes.status_code,userData['status_code_200'])
    #     self.assertEqual(json.loads(delBlogRes.text)['code'],0)

    def test_addLongBlog005(self):
        '''发布长微博：纯文字'''
        #先上传图片
        # m={'pic': ('image.gif', open("../../file/image.gif", 'rb'), 'image/gif')}    #这样上传文件post中用files，但是文件太大，选择用数据流传送MultipartEncoder
        # m = MultipartEncoder(fields = { "pic": ("image.jpg", open("../../file/image.jpg", "rb"), "image/jpeg")})
        # print("m",m)
        # print("m.content")
        # self.headers['Content-Type'] = m.content_type
        # print("self.headers",self.headers)
        # # self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})
        # print("self.headers",self.headers)
        # #上传图片
        # imageRes=requests.post(userData['hostName']+socialData['singleFileUpload_url'],data = m,headers = self.headers)
        # print(userData['hostName']+socialData['singleFileUpload_url'])
        # # headers = dict(('content-type' : m.content),**{userData['Authorization'] : userData['Bearer']+self.token})
        # print("headers",self.headers)
        # print("imageRes",imageRes.text)
        # #断言返回200，上传图片成功，返回code=0,上传图片成功
        # self.assertEqual(imageRes.status_code,userData['status_code_200'])
        # self.assertEqual(json.loads(imageRes.text)['code'],0)
        # #获取上传图片的url,用于发微博
        # imageUrl=json.loads(imageRes.text)['data']
        # imageUrl['ContentType']='jpg'
        # listImage=[]
        # listImage.append(imageUrl)
        # print("imageUrl",imageUrl)
    
        blogParams={"isLongBlog": True,                     #boolean  true表示长微博，false表示短微博
                    "longBody": "test longBlog test longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
                                "longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest"
                                " longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
                                "longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
                                "longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest longBlogtest "
                                "longBlogtest longBlog",     #长微博内容
                    "longTitle": "longBlog",          #长微博标题
                    "longIntro": "longBlog",          #长微博导语
                    "blogType": 0,                          #微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
                    #"files": listImage,
                    "symbol": "",
                    "postType": 0                           #发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
                   }

        self.headers['Content-Type'] = "application/json; charset=utf-8"
        longBlogRes=newSocial.addBlog(userData['hostName']+socialData['addBlog_url'],datas = blogParams, headers = self.headers)
        #断言返回200，code=0，发布微博成功
        self.assertEqual(longBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(longBlogRes.text)['code'],0)
        #获取微博id，用于删除微博
        longBlogId=json.loads(longBlogRes.text)['data']['ObjectId']
    
        #检查我的微博列表
        time.sleep(2)
        # params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
        getMyBlogsRes=newSocial.getMyBlogs(userData['hostName']+socialData['getMyBlogs_url'],headers = self.headers)
        print(userData['hostName']+socialData['getMyBlogs_url'])
        #断言返回200，code=0,获取我的微博列表成功
        self.assertEqual(getMyBlogsRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getMyBlogsRes.text)['code'],0)
    
        #断言，我的微博列表第一条微博为刚发布的微博
        blogId=json.loads(getMyBlogsRes.text)['data']['Items'][0]['Id']
        self.assertEqual(longBlogId,blogId)
    
        #删除微博
        delBlogRes=newSocial.delBlogById(userData['hostName']+socialData['delBlogById_url']+str(longBlogId),headers = self.headers)
        self.assertEqual(delBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(delBlogRes.text)['code'],0)

    def tearDown(self):
        # 清空测试环境
        # 退出登录
        signOutRes = Auth.signout(userData['hostName'] + authData['signout_url'], datas=self.headers)
        self.assertEqual(signOutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()
