#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_addShortBlog
# 用例标题: 发短微博(1、发纯文字微博 2、发文字+图片微博 3、发品种微博 4、发@用户的微博)
# 流程：
    #1、登录
    #2、发布微博
    #3、我的微博列表

import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,newSocial,FMCommon,Http
from requests_toolbelt.multipart import MultipartEncoder

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadnewSocialYML()
authData=FMCommon.loadAuthYML()

class AddShortBlog(unittest.TestCase):
    def setUp(self):
        #登录账号
        siginParams= {"account": userData['account'], "password": userData['passwd'], "remember": False}
        siginRes=Auth.signin(userData['hostName']+authData['signin_url'],headers = userData['headers'],datas = siginParams)
        #断言返回200登录成功
        self.assertEqual(siginRes.status_code,userData['status_code_200'])
        #获取headers
        self.token=json.loads(siginRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})


    def test_addShortBlog001(self):
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

        #休眠3秒后再获取我的微博
        time.sleep(2)
        #微博发布成功，检查我的微博列表
        # params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
        getMyBlogsRes=newSocial.getMyBlogs(userData['hostName']+socialData['getMyBlogs_url'],headers=self.headers)
        #断言返回200，code=0,获取微博列表成功
        self.assertEqual(getMyBlogsRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getMyBlogsRes.text)['code'],0)
        #获取我的微博列表第一条微博id
        blogId=json.loads(getMyBlogsRes.text)['data']['Items'][0]['Id']
        #断言，我的微博列表第一条微博id等于刚发布的短微博id
        self.assertEqual(blogId,shortBlogId)

        #删除微博
        delBlogRes=newSocial.delBlogById(userData['hostName']+socialData['delBlogById_url']+str(shortBlogId),headers = self.headers)
        self.assertEqual(delBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(delBlogRes.text)['code'],0)

    def test_addShortBlog002(self):
        '''发布单张图片+文字的短微博'''
        #先上传图片
        # m={'pic': ('image.gif', open("../../file/image.gif", 'rb'), 'image/gif')}    #这样上传文件post中用files，但是文件太大，选择用数据流传送MultipartEncoder
        m = MultipartEncoder(fields = { "pic": ("image.jpg", open("../../file/image.jpg", "rb"), "image/jpeg")})
        self.headers['Content-Type'] = m.content_type
        imageRes=requests.post(userData['hostName']+socialData['singleFileUpload_url'],data = m,headers = self.headers)
        # imageRes=newSocial.singleFileUpload(userData['hostName']+socialData['singleFileUpload_url'],datas = m,headers = self.headers)
        print(imageRes.text)
        #断言返回200，上传图片成功，返回code=0,上传图片成功
        self.assertEqual(imageRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(imageRes.text)['code'],0)
        #获取上传图片的url,用于发短微博
        imageUrl=json.loads(imageRes.text)['data']
        # print("",)
        imageUrl['Url']=imageUrl['url']
        print("imageUrl",imageUrl)
        del imageUrl['url']
        imageUrl['ContentType']='jpg'
        listImage=[]
        listImage.append(imageUrl)
        print("imageUrl",imageUrl)
        print("listImage",listImage)
    
        blogParams = {"isLongBlog": False,  # boolean  true表示长微博，false表示短微博
                      "body": "test",       # 短微博内容
                      "files":listImage,    #files图片文件为数组
                      "blogType": 0,        # 微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
                      "symbol": "",
                      "postType": 0         # 发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
                      }

        
        self.headers['Content-Type'] = "application/json; charset=utf-8"
        addShortBlogRes=newSocial.addBlog(userData['hostName']+socialData['addBlog_url'],headers = self.headers, datas = blogParams)
        #断言返回200，发微博成功，code=0发微博成功
        self.assertEqual(addShortBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(addShortBlogRes.text)['code'],0)
        #获取微博id,用于删除微博
        blogId=json.loads(addShortBlogRes.text)['data']['ObjectId']
    
        #检查我的微博列表
    
        #删除微博
        delBlogRes=newSocial.delBlogById(userData['hostName']+socialData['delBlogById_url']+str(blogId),headers = self.headers)
        self.assertEqual(delBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(delBlogRes.text)['code'],0)

    def test_addShortBlog003(self):
        '''发带品种标签的短微博'''
        blogParams = {"isLongBlog": False,  # boolean  true表示长微博，false表示短微博
                      "body": "$AUD/JPY$ test",       # 短微博内容
                      "blogType": 0,        # 微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
                      "symbol": "",
                      "postType": 0         # 发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
                      }
        addShortBlogRes=newSocial.addBlog(userData['hostName']+socialData['addBlog_url'],headers = self.headers, datas = blogParams)
        #断言返回200，发微博成功，code=0发微博成功
        self.assertEqual(addShortBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(addShortBlogRes.text)['code'],0)
        #获取微博id,用于删除微博
        blogId=json.loads(addShortBlogRes.text)['data']['ObjectId']

        #获取品种资讯列表
        #userData['type']博客类型：0-普通微博，1-公告，2-品种资讯，3-交易动态
        time.sleep(2)
        symbolBlogRes=newSocial.getBlogByType(userData['hostName']+socialData['getBlogByType_url']+str(userData['type']), headers = self.headers)
        #断言返回200，code=0,获取品种列表成功
        self.assertEqual(symbolBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(symbolBlogRes.text)['code'],0)
        #获取品种资讯列表所有微博,断言，刚发布的品种微博存在于品种资讯列表中
        listBlog=json.loads(symbolBlogRes.text)['data']['Items']
        listBlogId=[]
        for i in listBlog:
            listBlogId.append(i['Id'])
        self.assertIn(blogId,listBlogId)

        #删除微博
        delBlogRes=newSocial.delBlogById(userData['hostName']+socialData['delBlogById_url']+str(blogId),headers = self.headers)
        self.assertEqual(delBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(delBlogRes.text)['code'],0)

    def test_addShortBlog004(self):
        '''发布@用户的微博'''

        # 登录账号
        signinPrams = {"account": userData['followAccount'], "password": userData['followPasswd'], "remember": False}
        signinRes = Auth.signin(userData['hostName'] + authData['signin_url'], headers=userData['headers'],datas=signinPrams)
        # 断言返回200，登录成功
        self.assertEqual(signinRes.status_code, userData['status_code_200'])
        # 获取headers
        token = json.loads(signinRes.text)['data']['token']
        headers = dict(userData['headers'], **{userData['Authorization']: userData['Bearer'] + token})
        nickName = json.loads(signinRes.text)['data']['nickname']

        #发布微博
        blogParams = {"isLongBlog": False,  # boolean  true表示长微博，false表示短微博
                      "body": "test short blog at user @"+nickName,       # 短微博内容
                      "blogType": 0,        # 微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
                      "symbol": "",
                      "postType": 0         # 发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
                      }
        addShortBlogRes=newSocial.addBlog(userData['hostName']+socialData['addBlog_url'],headers = self.headers, datas = blogParams)
        #断言返回200，发微博成功，code=0发微博成功
        self.assertEqual(addShortBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(addShortBlogRes.text)['code'],0)
        #获取微博id,用于删除微博
        blogId=json.loads(addShortBlogRes.text)['data']['ObjectId']

        #获取@我的微博
        getAtMeBlogRes=newSocial.getAtMeBlogAndComment(userData['hostName']+socialData['getAtMeBlogAndComment_url']+str(userData['atmeType_blog']),headers = headers)
        #断言200，code=0,获取@我的微博成功
        self.assertEqual(getAtMeBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getAtMeBlogRes.text)['code'],0)

        #刚发布的微博id=@我的微博列表第一条微博
        atMeBlogList=json.loads(getAtMeBlogRes.text)['data']['Items']
        atMeBlogInfoList=[]
        for i in atMeBlogList:
            atMeBlogInfoList.append(i['BlogInfo'])
        self.assertEqual(blogId,atMeBlogInfoList[0]['Id'])

        # 删除微博
        delBlogRes = newSocial.delBlogById(userData['hostName'] + socialData['delBlogById_url'] + str(blogId),headers = self.headers)
        self.assertEqual(delBlogRes.status_code, userData['status_code_200'])
        self.assertEqual(json.loads(delBlogRes.text)['code'], 0)

    def test_addShortBlog005(self):
        '''发文字+表情短微博'''
        blogParams={"isLongBlog": False,                     #boolean  true表示长微博，false表示短微博
                    "body": "test short blog test[花心][花心][花心][花心][花心][花心]",          #短微博内容
                    "blogType": 0,                           #微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
                    "symbol": "",
                    "postType": 0                            #发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
                   }
        shortBlogRes=newSocial.addBlog(userData['hostName']+socialData['addBlog_url'],headers = self.headers,datas = blogParams)
        #断言返回200，发布微博成功
        self.assertEqual(shortBlogRes.status_code,userData['status_code_200'],"微博发布失败")
        #获取微博id,用于删除微博
        shortBlogId=json.loads(shortBlogRes.text)['data']['ObjectId']

        #休眠3秒后再获取我的微博
        time.sleep(2)
        #微博发布成功，检查我的微博列表
        # params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
        getMyBlogsRes=newSocial.getMyBlogs(userData['hostName']+socialData['getMyBlogs_url'],headers=self.headers)
        #断言返回200，code=0,获取微博列表成功
        self.assertEqual(getMyBlogsRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getMyBlogsRes.text)['code'],0)
        #获取我的微博列表第一条微博id
        blogId=json.loads(getMyBlogsRes.text)['data']['Items'][0]['Id']
        #断言，我的微博列表第一条微博id等于刚发布的短微博id
        self.assertEqual(blogId,shortBlogId)

        #删除微博
        delBlogRes=newSocial.delBlogById(userData['hostName']+socialData['delBlogById_url']+str(shortBlogId),headers = self.headers)
        self.assertEqual(delBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(delBlogRes.text)['code'],0)
        


    def tearDown(self):

        #清空测试环境
        #退出登录
        signOutRes=Auth.signout(userData['hostName']+ authData['signout_url'],datas = self.headers)
        self.assertEqual(signOutRes.status_code,userData['status_code_200'])

if __name__=='__main__':
    unittest.main()
