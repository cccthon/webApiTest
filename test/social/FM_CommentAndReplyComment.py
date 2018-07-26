#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_WebAPI_Social_CommentAndReply
# 流程:
    #1、登录账号A，发微博
    #2、登录账号B评论微博
    #3、A回复B的评论
    #4、删除回复的评论，退出登录
    #5、删除评论，删除微博，退出登录
import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,Social,FMCommon,Http

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadSocialYML()
authData=FMCommon.loadAuthYML()

class CommentAndReply(unittest.TestCase):
    def setUp(self):

        #登录账号A获取headers
        signinParams = {"account": userData['account'], "password": userData['passwd'], "remember": False}
        singinRes=Auth.signin(userData['hostName'] + authData['signin_url'], datas=signinParams, headers=userData['headers'])
        self.assertEqual(singinRes.status_code,  userData['status_code_200'])
        self.token = json.loads(singinRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})
        self.nickName = json.loads(singinRes.text)['data']['nickname']
        self.userId = json.loads(singinRes.text)['data']['id']

         #获取要发布的微博ID
        getBlogIdRes = Social.getBlogId(userData['hostName'] + socialData['getNewBlogid_url'], headers=self.headers)
        self.assertEqual(getBlogIdRes.status_code, userData['status_code_200'])
        self.blogId = json.loads(getBlogIdRes.text)['data']['Imsg']

        #账号A发布微博
        params = {'blogBody': '测试回复评论',
                  'blogid': self.blogId,
                  'haspicture': False,  # 是否有图片 有为 true 没有为false
                  'whetherremind': False,  # 是否需要后台额外提醒 需要提醒为 true 否为false 默认为false
                  'blogType': 0,  # blogType微博类型：0：普通微博；1：公告；2：品种；3：交易动态
                  'symbol': ""
                  }
        postShortBlogRes = Social.postShortBlog(userData['hostName'] + socialData['postShortBlog_url'], headers=self.headers,datas=params)
        self.assertEqual(postShortBlogRes.status_code,  userData['status_code_200'])


    def test_commentAndReplyComment_001(self):
        '''发布短微博，别人评论我的微博，对评论进行回复，还原测试环境'''
        #登录账号B对微博进行评论
        signinParams = {"account": userData['followAccount'], "password": userData['followPasswd'], "remember": False}
        singinRes = Auth.signin(userData['hostName'] + authData['signin_url'],datas=signinParams,headers=userData['headers'])
        self.assertEqual(singinRes.status_code,  userData['status_code_200'])
        tokenComment = json.loads(singinRes.text)['data']['token']
        headerComment=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+tokenComment})

        # 账号B对该微博进行评论
        commentParams={'combody':'测试评论微博'}
        blogCommentRes = Social.addComment(userData['hostName'] + socialData['addComment_url1'] + str(self.blogId) + socialData['addComment_url2'],datas=commentParams,headers=headerComment,)
        self.assertEqual(blogCommentRes.status_code, userData['status_code_200'])
        #获取评论id
        commentId = json.loads(blogCommentRes.text)['data']['Imsg']


        #账号A对评论进行回复
        ParamsreplyCom={'reblogId':self.blogId,
                         'parentUserId':self.userId,
                        'parentUserName':self.nickName,
                        'recombody':'测试对评论的回复',
                        'whetherremind':False}
        replyCommentRes=Social.replyComment(userData['hostName']+socialData['replyComment_url1']+str(commentId)+socialData['replyComment_url2'],headers=self.headers,datas=ParamsreplyCom)
        self.assertEqual(replyCommentRes.status_code, userData['status_code_200'])
        #回复评论id
        replyCommentID=json.loads(replyCommentRes.text)['data']['Imsg']


        #删除账号A回复的评论
        delReplyCommentRes=Social.deleteComment(userData['hostName']+ socialData['deleteComment_url'] + str(replyCommentID),headers=self.headers)
        self.assertEqual(delReplyCommentRes.status_code, userData['status_code_200'])


        #账号B删除评论
        delCommentRes = Social.deleteComment(userData['hostName'] + socialData['deleteComment_url'] + str(commentId),headers=headerComment)
        self.assertEqual(delCommentRes.status_code, userData['status_code_200'])


        #退出账号B
        signoutRes = Auth.signout(userData['hostName']+ authData['signout_url'])
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

    def tearDown(self):
        #清空测试环境
        # 账号A删除微博
        delBlogRes=Social.deleteBlog(userData['hostName']+socialData['deleteBlog_url']+str(self.blogId),headers=self.headers)
        self.assertEqual(delBlogRes.status_code,  userData['status_code_200'])
        #退出账号
        signoutRes = Auth.signout(userData['hostName']+ authData['signout_url'],datas=self.headers)
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()