#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PraiseBlog
# 流程:
    # 1、账号A登录,发布一条短微博
    # 2、账号B登录，点赞该条微博
    # 3、账号A检查收到的赞列表，并获取微博点赞列表检查数据
    # 4、账号B取消点赞，检查A的点赞列表和微博点赞列表
    # 5、账号A删除微博


import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
import Auth,Social,FMCommon

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadSocialYML()
authData=FMCommon.loadAuthYML()

class PraiseBlog(unittest.TestCase):
    def setUp(self):
        # 登录账号A获取headers
        signinParams = {"account": userData['followAccount'], "password": userData['followPasswd'], "remember": False}
        signinRes = Auth.signin(userData['hostName'] + authData['signin_url'], datas=signinParams, headers=userData['headers'])
        self.assertEqual(signinRes.status_code, userData['status_code_200'])
        self.token = json.loads(signinRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})
        self.userId=json.loads(signinRes.text)['data']['id']


        # 获取要发布的微博ID
        getBlogIdRes = Social.getBlogId(userData['hostName'] + socialData['getNewBlogid_url'], headers=self.headers)
        self.assertEqual(getBlogIdRes.status_code, userData['status_code_200'])
        self.blogId = json.loads(getBlogIdRes.text)['data']['Imsg']

        # 账号A发布微博
        params = {'blogBody': '测试点赞微博',
                  'blogid': self.blogId,
                  'haspicture': False,  # 是否有图片 有为 true 没有为false
                  'whetherremind': False,  # 是否需要后台额外提醒 需要提醒为 true 否为false 默认为false
                  'blogType': 0,  # blogType微博类型：0：普通微博；1：公告；2：品种；3：交易动态
                  'symbol': ""
                  }
        postShortBlogRes = Social.postShortBlog(userData['hostName'] + socialData['postShortBlog_url'],headers=self.headers, datas=params)
        self.assertEqual(postShortBlogRes.status_code, userData['status_code_200'])


    def test_praiseBlogAndDelPraistBlog(self):
        '''点赞微博-》检查微博的赞用户列表，检查收到的赞列表，检查新增的微博点赞数-》取消点赞-》检查收到的赞列表，检查微博的赞用户列表-》删除微博，退出账号'''

        #登录账号B点赞该条微博
        signinParams = {"account": userData['account'], "password": userData['passwd'], "remember": False}
        signinRes = Auth.signin(userData['hostName'] + authData['signin_url'], datas=signinParams, headers=userData['headers'])
        self.assertEqual(signinRes.status_code, userData['status_code_200'])
        praiseToken = json.loads(signinRes.text)['data']['token']
        praiseHeaders=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+praiseToken})
        praiseUserId=json.loads(signinRes.text)['data']['id']


        #账号B点赞该条微博
        praiseBlogRes= Social.praiseBlog(userData['hostName'] + socialData['praiseBlog_url1'] + str(self.blogId) + socialData['praiseBlog_url2'],headers=praiseHeaders)
        self.assertEqual(praiseBlogRes.status_code, userData['status_code_200'])


        #检查该条微博的点赞用户列表，
        userPraiseBlogsUrl=userData['hostName']+socialData['getUserPraiseMicroBlogs_url']+str(self.blogId)+socialData['getUserPraiseMicroBlogs_url2']
        userPraiseParams={'id':self.blogId,
                          'top':1,               #获取点赞用户数量
                          'authorId':self.userId  #微博作者Id
                          }
        getUserPraiseMicroBlogsRes=Social.getUserPraiseMicroBlogs(userPraiseBlogsUrl,datas=userPraiseParams)
        self.assertEqual(getUserPraiseMicroBlogsRes.status_code,userData['status_code_200'])
        userPraiseList=json.loads(getUserPraiseMicroBlogsRes.text)['data']['Items']
        #断言：点赞成功后，账户Buserid存在于该条微博的点赞用户userid中
        userPraiseListUserId=userPraiseList[0]
        self.assertEqual(praiseUserId,userPraiseListUserId)


        #账号A,检查微博新增的点赞数
        newPraiseBlogRes=Social.getNewPraiseMicroBlogs(userData['hostName']+socialData['getNewPraiseMicroBlogs_url']+str(self.blogId),headers = self.headers)
        self.assertEqual(newPraiseBlogRes.status_code,userData['status_code_200'])
        #断言，微博的新增的点赞数量=1
        newPraise=json.loads(newPraiseBlogRes.text)['data'][str(self.blogId)]
        self.assertEqual(newPraise,1)


        #账号A检查收到的赞列表,第一条数据为该微博的赞
        praiseListParams={'pageIndex':1,'pageSize':10}
        PraiseListRes=Social.getPraiseList(userData['hostName']+socialData['getPraiseList_url'],datas=praiseListParams,headers=self.headers)
        self.assertEqual(PraiseListRes.status_code,userData['status_code_200'])
        PraiseUserListBlogId=json.loads(PraiseListRes.text)['data']['List'][0]['MicroBlog']['MBlog']['id']
        self.assertEqual(PraiseUserListBlogId,self.blogId)

        #账号B取消点赞
        delPraiseBlogRes=Social.praiseBlog(userData['hostName']+socialData['praiseBlog_url1']+str(self.blogId)+socialData['praiseBlog_url2'],headers=praiseHeaders)
        self.assertEqual(delPraiseBlogRes.status_code,userData['status_code_200'])

        #
        # #取消点赞后，检查收到的赞列表
        # delPraiseListRes=Social.getPraiseList(userData['hostName']+socialData['getPraiseList_url'],datas=praiseListParams,headers=self.headers)
        # self.assertEqual(delPraiseListRes.status_code,userData['status_code_200'])
        # delPraiseUserList = json.loads(delPraiseListRes.text)['data']['List']
        # #取消点赞后，收到的赞列表为空
        # self.assertListEqual(delPraiseUserList,[])


        # #取消点赞后，检查该微博的点赞用户列表
        # getUserPraiseMicroBlogsRes=Social.getUserPraiseMicroBlogs(userPraiseBlogsUrl,datas=userPraiseParams)
        # self.assertEqual(getUserPraiseMicroBlogsRes.status_code,userData['status_code_200'])
        # userPraise=json.loads(getUserPraiseMicroBlogsRes.text)['data']['Items']
        # #断言，取消点赞后，该微博的点赞用户列表为空
        # self.assertListEqual(userPraise,[])
        # FMCommon.printLog('取消点赞后，该微博的点赞用户列表为空 '+str(userPraise))

        #退出账号B
        signoutRes = Auth.signout(userData['hostName'] + authData['signout_url'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

    def tearDown(self):
        #还原测试环境
        #账号A删除微博
        delBlogRes=Social.deleteBlog(userData['hostName']+socialData['deleteBlog_url']+str(self.blogId),headers=self.headers)
        self.assertEqual(delBlogRes.status_code,userData['status_code_200'])

        #退出账号
        signoutRes = Auth.signout(userData['hostName'] + authData['signout_url'],datas=self.headers)
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__=='__main__':
    unittest.main()