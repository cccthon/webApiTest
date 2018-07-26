#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getAtMeCommentList
# 流程:
    #1、登录，发微博，对该微博进行@用户的评论
    #2、检查@我的评论列表
    #3、删除评论，删除微博，退出登录
import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,Social,FMCommon,Http,time


userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadSocialYML()
authData=FMCommon.loadAuthYML()

class AtMeComment(unittest.TestCase):
    def setUp(self):
        signinParams = {"account": userData['followAccount'], "password": userData['followPasswd'], "remember": False}
        singinRes = Auth.signin(userData['hostName'] + authData['signin_url'], datas=signinParams,
                                headers=userData['headers'])
        self.assertEqual(singinRes.status_code, userData['status_code_200'])
        self.token = json.loads(singinRes.text)['data']['token']
        self.headers = dict(userData['headers'], **{userData['Authorization']: userData['Bearer'] + self.token})
        self.nickName = json.loads(singinRes.text)['data']['nickname']

        # 获取发布微博的id
        getBlogIdRes = Social.getBlogId(userData['hostName'] + socialData['getNewBlogid_url'], headers=self.headers)
        self.assertEqual(getBlogIdRes.status_code, userData['status_code_200'])
        self.blogId = json.loads(getBlogIdRes.text)['data']['Imsg']

        # 发布短微博
        params = {'blogBody': '发短微博，测试@用户的评论',
                  'blogid': self.blogId,
                  'haspicture': False,  # 是否有图片 有为 true 没有为false
                  'whetherremind': False,  # 是否需要后台额外提醒 需要提醒为 true 否为false 默认为false
                  'blogType': 0,  # blogType微博类型：0：普通微博；1：公告；2：品种；3：交易动态
                  'symbol': ""}
        postShortBlogRes = Social.postShortBlog(userData['hostName'] + socialData['postShortBlog_url'],headers=self.headers, datas=params)
        self.assertEqual(postShortBlogRes.status_code, userData['status_code_200'])


    def test_getAtMeCommentList(self):
        '''发布@用户的评论，检查@我的评论列表'''
        #对该微博发布@用户的评论，登录被@用户的账号
        signinParams = {"account": userData['account'], "password": userData['passwd'], "remember": False}
        singinRes = Auth.signin(userData['hostName'] + authData['signin_url'], datas=signinParams,headers=userData['headers'])
        self.assertEqual(singinRes.status_code, userData['status_code_200'])
        atToken = json.loads(singinRes.text)['data']['token']
        atHeaders = dict(userData['headers'], **{userData['Authorization']: userData['Bearer'] + atToken})
        atNickName = json.loads(singinRes.text)['data']['nickname']
        # atUserId=json.loads(singinRes.text)['data']['id']


        #发布@用户的评论
        commentParams = {'combody': '@'+atNickName +' test atMeComment','whetherremind':True}
        commentUrl = userData['hostName'] + socialData['addComment_url1'] + str(self.blogId) + socialData['addComment_url2']
        commentRes = Social.addComment(commentUrl, headers=self.headers, datas=commentParams)
        self.assertEqual(commentRes.status_code, userData['status_code_200'])
        # 取出评论ID
        self.commentId = json.loads(commentRes.text)['data']['Imsg']

        #获取@我的评论列表
        time.sleep(2)
        atMeCommentParms = {'pageindex': 1, 'pagesize': 100}
        atMeCommentRes = Social.getAtMeComments(userData['hostName'] + socialData['getAtMeCommentList_url'], datas=atMeCommentParms, headers=atHeaders)
        self.assertEqual(atMeCommentRes.status_code, userData['status_code_200'])
        # 断言刚发布的微博评论在@我的评论中第一条
        atMeCommentListCommentId = json.loads(atMeCommentRes.text)['data']['List'][0]['Id']
        self.assertEqual(atMeCommentListCommentId,self.commentId)


        #删除评论
        delCommentURl = userData['hostName'] + socialData['deleteComment_url'] + str(self.commentId)
        delCommentRes = Social.deleteComment(delCommentURl, headers=self.headers)
        self.assertEqual(delCommentRes.status_code, userData['status_code_200'])

    def tearDown(self):

        # 清空测试环境，删除微博
        res_delBlog = Social.deleteBlog(userData['hostName'] + socialData['deleteBlog_url'] + str(self.blogId),headers=self.headers)
        self.assertEqual(res_delBlog.status_code, userData['status_code_200'])

        # 退出登录
        signout = Auth.signout(userData['hostName'] + authData['signout_url'],datas=self.headers)
        self.assertEqual(signout.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()