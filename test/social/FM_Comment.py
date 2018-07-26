#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_WebAPI_Social_deleteComment
# 流程:
    #1、登录，发微博，对微博进行评论
    #2、删除评论，删除微博，退出登录
import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,Social,FMCommon,Http

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadSocialYML()
authData=FMCommon.loadAuthYML()

class DeleteComment(unittest.TestCase):
    def setUp(self):
        #登录获取headers
        signinParams={"account":userData['account'], "password":userData['passwd'], "remember":False}
        singinRes=Auth.signin(userData['hostName'] + authData['signin_url'], datas=signinParams, headers=userData['headers'])
        self.assertEqual(singinRes.status_code, userData['status_code_200'])
        self.token = json.loads(singinRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})

        #获取要发布的微博ID
        getBlogIdRes = Social.getBlogId(userData['hostName'] + socialData['getNewBlogid_url'], headers=self.headers)
        self.assertEqual(getBlogIdRes.status_code,userData['status_code_200'])
        self.blogId = json.loads(getBlogIdRes.text)['data']['Imsg']

        # 发布短微博
        params = {'blogBody': '测试发短微博',
                  'blogid': self.blogId,
                  'haspicture': False,  # 是否有图片 有为 true 没有为false
                  'whetherremind': False,  # 是否需要后台额外提醒 需要提醒为 true 否为false 默认为false
                  'blogType': 0,  # blogType微博类型：0：普通微博；1：公告；2：品种；3：交易动态
                  'symbol': ""
                  }
        postShortBlogRes = Social.postShortBlog(userData['hostName'] + socialData['postShortBlog_url'], headers=self.headers,datas=params)
        self.assertEqual(postShortBlogRes.status_code, userData['status_code_200'])


    def test_addAndDeleteComment(self):
        '''发布短微博，评论微博，删除评论，删除微博'''
        # 对该微博进行评论
        commentParams={'combody':'测试评论微博'}
        commentUrl= userData['hostName'] + socialData['addComment_url1'] + str(self.blogId) + socialData['addComment_url2']
        commentRes = Social.addComment(commentUrl,headers=self.headers,datas=commentParams)
        self.assertEqual(commentRes.status_code, userData['status_code_200'])

        #取出评论ID
        self.commentId = json.loads(commentRes.text)['data']['Imsg']


        #检查对微博的评论是否在我评论的列表中
        myCommentParms = {'pageindex': 1, 'pagesize': 100}
        myCommentUrl=userData['hostName'] + socialData['getMyComments_url']
        MyCommentRes = Social.getMyComments(myCommentUrl,headers=self.headers,datas=myCommentParms)
        self.assertEqual(MyCommentRes.status_code, userData['status_code_200'])

    # 断言，评论成功后，该评论id,存在于我评论的列表中
        MyCommentList = json.loads(MyCommentRes.text)['data']['List']
        MyCommentId_list = []
        for i in MyCommentList:
            MyCommentId_list.append(i['Id'])
        self.assertIn(self.commentId,MyCommentId_list)
        FMCommon.printLog('我评论的列表 '+str(MyCommentId_list))

    #检查微博评论是否存在于评论我的列表中
        comAboutMeParams= {'pageindex': 1, 'pagesize': 100}
        commentAboutMeRes= Social.getCommentsAboutMe(userData['hostName']+socialData['getCommentsAboutMe_url'],headers=self.headers,datas=comAboutMeParams)
        self.assertEqual(commentAboutMeRes.status_code,userData['status_code_200'])

    #断言，评论成功后，该评论id，存在于评论我的列表中
        commentAboutMeList=json.loads(commentAboutMeRes.text)['data']['List']
        commentAboutMeId_list=[]
        for x in commentAboutMeList:
            commentAboutMeId_list.append(x['Id'])
        self.assertIn(self.commentId,commentAboutMeId_list)
        FMCommon.printLog('评论我的列表 '+str(commentAboutMeId_list))


    # 删除评论
        delCommentURl=userData['hostName'] + socialData['deleteComment_url'] + str(self.commentId)
        delCommentRes = Social.deleteComment(delCommentURl,headers=self.headers)
        self.assertEqual(delCommentRes.status_code, userData['status_code_200'])

    #检查删除的评论是否从我的评论列表中删除
        delMyCommentParms = {'pageindex': 1, 'pagesize': 100}
        delMyCommentRes = Social.getMyComments(userData['hostName'] + socialData['getMyComments_url'], datas=delMyCommentParms, headers=self.headers)
        self.assertEqual(delMyCommentRes.status_code, userData['status_code_200'])

    # 断言，删除评论后，该评论ID不存在于我评论的列表中，即为删除评论成功
        delMyCommentList = json.loads(delMyCommentRes.text)['data']['List']
        delMyCommentId_list = []
        for j in delMyCommentList:
            delMyCommentId_list.append(j['Id'])
        self.assertNotIn(self.commentId, delMyCommentId_list)


    #检查删除的评论是否从评论我的列表中删除
        delCommentAboutMeParams= {'pageindex': 1, 'pagesize': 100}
        delCommentAboutMeRes= Social.getCommentsAboutMe(userData['hostName']+socialData['getCommentsAboutMe_url'],headers=self.headers,datas=delCommentAboutMeParams)
        self.assertEqual(delCommentAboutMeRes.status_code,userData['status_code_200'])
    #断言，删除评论后，该评论ID,不存在于评论我的列表中，即为删除评论成功
        delCommentAboutMeList= json.loads(delCommentAboutMeRes.text)['data']['List']
        delCommentAboutMeId_list= []
        for k in delCommentAboutMeList:
            delCommentAboutMeId_list.append(k['Id'])
        self.assertNotIn(self.commentId,delCommentAboutMeId_list)


    #检查删除的评论是否从微博评论列表中删除
        res_blogCommentList=requests.get(userData['hostName']+socialData['getComments_url1']+str(self.blogId)+socialData['getComments_url2'])
        self.assertEqual(res_blogCommentList.status_code,userData['status_code_200'])

    #断言删除评论后，该微博的评论列表为空，即为删除评论成功
        blogCommentList=json.loads(res_blogCommentList.text)['data']['List']
        self.assertListEqual(blogCommentList,[])



    def tearDown(self):
        #清空测试环境，删除微博
        res_delBlog=Social.deleteBlog(userData['hostName']+socialData['deleteBlog_url']+str(self.blogId),headers=self.headers)
        self.assertEqual(res_delBlog.status_code, userData['status_code_200'])

        #退出登录
        signout = Auth.signout(userData['hostName']+ authData['signout_url'],datas=self.headers)
        self.assertEqual(signout.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()