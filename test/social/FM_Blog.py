#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_WebAPI_Social_blogShare
# 流程:
    # 1、登录,发布一条短微博
    # 2、评论，收藏，点赞，分享
    # 3、取消评论，取消收藏，取消点赞
    # 4、删除微博，退出登录


import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
import Auth,Social,FMCommon

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadSocialYML()
authData=FMCommon.loadAuthYML()


class Blog(unittest.TestCase):
    def setUp(self):
        #登录获取headers
        signinParams = {"account": userData['followAccount'], "password": userData['followPasswd'], "remember": False}
        signinRes=Auth.signin(userData['hostName'] + authData['signin_url'],datas=signinParams, headers=userData['headers'])
        self.assertEqual(signinRes.status_code,  userData['status_code_200'])
        self.token = json.loads(signinRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})


        #获取要发布的微博ID
        getBlogIdRes = Social.getBlogId(userData['hostName'] + socialData['getNewBlogid_url'], headers=self.headers)
        self.assertEqual(getBlogIdRes.status_code, userData['status_code_200'])
        self.blogId = json.loads(getBlogIdRes.text)['data']['Imsg']

        #发布微博
        params = {'blogBody': '测试发短微博',
                  'blogid': self.blogId,
                  'haspicture': False,  # 是否有图片 有为 true 没有为false
                  'whetherremind': False,  # 是否需要后台额外提醒 需要提醒为 true 否为false 默认为false
                  'blogType': 0,  # blogType微博类型：0：普通微博；1：公告；2：品种；3：交易动态
                  'symbol': ""}
        postShortBlogRes = Social.postShortBlog(userData['hostName'] + socialData['postShortBlog_url'], headers=self.headers,datas=params)
        self.assertEqual(postShortBlogRes.status_code,  userData['status_code_200'])


    def test_BlogAll_001(self):
        '''发布微博，对该条微博进行分享，评论，点赞，收藏，还原测试环境'''
        # 微博分享
        blogShareParams={'blogId':self.blogId}
        blogShareRes = Social.blogShare(userData['hostName'] + socialData['blogShare_url'], datas=blogShareParams,headers=self.headers)
        self.assertEqual(blogShareRes.status_code,  userData['status_code_200'])

        # 对该微博进行评论
        commentParams={'combody':'测试评论微博'}
        blogcommentRes = Social.addComment(userData['hostName'] + socialData['addComment_url1'] + str(self.blogId) + socialData['addComment_url2'],headers=self.headers,datas=commentParams)
        self.assertEqual(blogcommentRes.status_code,userData['status_code_200'])
        self.commentId = json.loads(blogcommentRes.text)['data']['Imsg']


        #对微博点赞
        praiseBlogRes= Social.praiseBlog(userData['hostName'] + socialData['praiseBlog_url1'] + str(self.blogId) + socialData['praiseBlog_url2'],headers=self.headers)
        self.assertEqual(praiseBlogRes.status_code, userData['status_code_200'])


    # 收藏微博
        collectBlogRes = Social.collectBlog(userData['hostName'] + socialData['collectBlog_url1'] + str(self.blogId) + socialData['collectBlog_url2'],headers=self.headers)
        self.assertEqual(collectBlogRes.status_code, userData['status_code_200'])



    # 删除评论
        delCommentRes = Social.deleteComment(userData['hostName'] + socialData['deleteComment_url'] + str(self.commentId),headers=self.headers)
        self.assertEqual(delCommentRes.status_code,userData['status_code_200'])


    # 取消点赞
        delPariseRes = Social.praiseBlog(userData['hostName'] + socialData['praiseBlog_url1'] + str(self.blogId) + socialData['praiseBlog_url2'],headers=self.headers)
        self.assertEqual(delPariseRes.status_code,userData['status_code_200'])


    # 取消收藏
        delcollectBlogRes = Social.collectBlog(userData['hostName'] + socialData['collectBlog_url1'] + str(self.blogId) + socialData['collectBlog_url2'],headers=self.headers)
        self.assertEqual(delcollectBlogRes.status_code, userData['status_code_200'])


    def tearDown(self):
        #清空测试环境，删除微博
        delBlogRes=Social.deleteBlog(userData['hostName']+socialData['deleteBlog_url']+str(self.blogId),headers=self.headers)
        self.assertEqual(delBlogRes.status_code,  userData['status_code_200'])

        #退出登录
        signout = Auth.signout(userData['hostName']+ authData['signout_url'],datas=self.headers)
        self.assertEqual(signout.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()