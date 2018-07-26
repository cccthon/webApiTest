#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_WebAPI_Social_addComment_001
# 流程:
# 1、登录--》获取微博id，发布一条短微博
# 2、删除微博，退出登录
import sys,requests,unittest,yaml,json,time,imghdr
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,Social,FMCommon,Http,time

# from requests_toolbelt.multipart import MultipartEncoder

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadSocialYML()
authData=FMCommon.loadAuthYML()

class PostShortBlog(unittest.TestCase):
    def setUp(self):
        signinParams={"account":userData['account'], "password":userData['passwd'], "remember":False}
        singinRes = Auth.signin(userData['hostName'] + authData['signin_url'],datas=signinParams, headers=userData['headers'])
        self.assertEqual(singinRes.status_code, userData['status_code_200'])
        self.token = json.loads(singinRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})
        self.nickName=json.loads(singinRes.text)['data']['nickname']

    # 获取发布微博的id
        getBlogIdRes=Social.getBlogId(userData['hostName']+socialData['getNewBlogid_url'],headers=self.headers)
        self.assertEqual(getBlogIdRes.status_code, userData['status_code_200'])
        self.blogId=json.loads(getBlogIdRes.text)['data']['Imsg']



    def test_postShortBlog_001(self):
        '''发布纯文字短微博，检查我的微博列表'''
        #发短微博
        params={'blogBody':'测试发短微博',
                'blogid':self.blogId,
                'haspicture':False,     # 是否有图片 有为 true 没有为false
                'whetherremind':False,  # 是否需要后台额外提醒 需要提醒为 true 否为false 默认为false
                'blogType':0,           # blogType微博类型：0：普通微博；1：公告；2：品种；3：交易动态
                'symbol':""
                }
        postShortBlogRes=Social.postShortBlog(userData['hostName']+socialData['postShortBlog_url'],headers=self.headers,datas=params)
        self.assertEqual(postShortBlogRes.status_code, userData['status_code_200'])

        #检查我的微博列表存在该微博
        blogListParams={'pageIndex':1,'pageSize':10}
        myblogListRes=Social.getMyBlogList(userData['hostName']+socialData['getMyBlogList_url'],headers=self.headers,datas=blogListParams)
        self.assertEqual(myblogListRes.status_code, userData['status_code_200'])
        MyBlogList=json.loads(myblogListRes.text)['data']['List']
        self.assertEqual(self.blogId,MyBlogList[0]['MBlog']['id'])

        #删除微博
        delBlogRes = Social.deleteBlog(userData['hostName'] + socialData['deleteBlog_url'] + str(self.blogId),headers=self.headers)
        self.assertEqual(delBlogRes.status_code, userData['status_code_200'])

    def test_postShortBlog_002(self):
        '''发布@用户的微博，检查@我的微博列表'''
        # 登录被@用户的账号
        signinParams = {"account": userData['followAccount'], "password": userData['followPasswd'], "remember": False}
        singinRes = Auth.signin(userData['hostName'] + authData['signin_url'], datas=signinParams,
                                headers=userData['headers'])
        self.assertEqual(singinRes.status_code, userData['status_code_200'])
        atToken = json.loads(singinRes.text)['data']['token']
        atHeaders = dict(userData['headers'], **{userData['Authorization']: userData['Bearer'] + atToken})
        self.nickName = json.loads(singinRes.text)['data']['nickname']
        # self.userId=json.loads(singinRes.text)['data']['id']


        '''发布@用户的微博'''
        params={'blogBody':'@'+self.nickName+' 测试微博@用户的微博',
                'blogid':self.blogId,
                'haspicture':False,     # 是否有图片 有为 true 没有为false
                'whetherremind':True,  # 发布@用的微博，此项必须为true.是否需要后台额外提醒 需要提醒为 true 否为false 默认为false,
                'blogType':0,           # blogType微博类型：0：普通微博；1：公告；2：品种；3：交易动态
                'symbol':""
                }
        postShortBlogRes = Social.postShortBlog(userData['hostName'] + socialData['postShortBlog_url'],headers=self.headers, datas=params)
        self.assertEqual(postShortBlogRes.status_code, userData['status_code_200'])

        time.sleep(3)
        #检查@我的微博列表
        blogListParams = {'pageIndex': 1, 'pageSize': 10}
        atMeblogListRes = Http.get(userData['hostName'] + socialData['getAtMeBlogList_url'], headers=atHeaders,params=blogListParams)
        self.assertEqual(atMeblogListRes.status_code, userData['status_code_200'])
        atMeBlogId = json.loads(atMeblogListRes.text)['data']['List'][0]['MBlog']['id']
        self.assertEqual(self.blogId,atMeBlogId)

        # 删除微博
        delBlogRes = Social.deleteBlog(userData['hostName'] + socialData['deleteBlog_url'] + str(self.blogId),headers=self.headers)
        self.assertEqual(delBlogRes.status_code, userData['status_code_200'])

        signout = Auth.signout(userData['hostName']+ authData['signout_url'],datas=atHeaders)
        self.assertEqual(signout.status_code, userData['status_code_200'])

    def test_postShortBlog_003(self):
        '''发纯图片短微博，检查我的微博列表'''

        # 传单张图片
        # m = MultipartEncoder(fields = {"blogid":str(self.blogId), "pic": ("image.jpg", open("../../file/image.jpg", "rb"), "image/jpeg")})

        # 传多张图片
        # m = MultipartEncoder(fields= [
        #                               ("blogid", (None, "20317510")),
        #                               ("pic", ("image.jpg", open("../../file/image.jpg", "rb"), "image/jpeg")),
        #                               ("pic",("image.png", open("../../file/image.png", "rb"), "image/png"))
        #                               ] )
        #
        # # 请求头必须包含一个特殊的头信息，类似于Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryreya4yqqgkvHSCjW
        # self.headers['Content-Type']=m.content_type
        # multiFileUploadRes = Social.multiFileUpload(userData['hostName'] + socialData['multiFileUpload_url'], datas=m,headers=self.headers)

        # params={"blogid": self.blogId, "blogBody": "", "haspicture":True, "whetherremind": False}
        # postShortBlogRes=Social.postShortBlog(userData['hostName']+userData['postShortBlog_url'],headers=self.headers,datas=params)
        # self.assertEqual(postShortBlogRes.status_code, userData['status_code_200'])
        #
        # # 删除微博
        # delBlogRes = Social.deleteBlog(userData['hostName'] + userData['deleteBlog_url'] + str(self.blogId),headers=self.headers)
        # self.assertEqual(delBlogRes.status_code, userData['status_code_200'])

    def tearDown(self):
        # 清空测试环境,退出登录
        signout = Auth.signout(userData['hostName']+ authData['signout_url'],datas=self.headers)
        self.assertEqual(signout.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()