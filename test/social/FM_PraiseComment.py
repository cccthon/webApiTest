#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PraiseComment
# 流程:
    # 1、账号A登录,发布一条短微博,并评论该微博
    # 2、账号B登录，点赞该微博评论
    # 3、检查微博评论列表的点赞用户，账号A检查收到的赞列表，并获取微博评论新增的点赞数，
    # 4、账号B取消点赞，检查A的点赞列表和微博评论点赞列表
    # 5、账号A删除微博


import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
import Auth,Social,FMCommon

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadSocialYML()
authData=FMCommon.loadAuthYML()

class PraiseComment(unittest.TestCase):
    def setUp(self):
        # 登录账号A获取headers
        signinParams={"account":userData['followAccount'], "password":userData['followPasswd'], "remember":False}
        signinRes = Auth.signin(userData['hostName'] + authData['signin_url'],datas=signinParams,headers=userData['headers'])
        self.assertEqual(signinRes.status_code, userData['status_code_200'])
        self.token = json.loads(signinRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})
        self.userId = json.loads(signinRes.text)['data']['id']

        # 获取要发布的微博ID
        getBlogIdRes = Social.getBlogId(userData['hostName'] + socialData['getNewBlogid_url'], headers=self.headers)
        self.assertEqual(getBlogIdRes.status_code, userData['status_code_200'])
        self.blogId = json.loads(getBlogIdRes.text)['data']['Imsg']

        # 账号A发布微博
        params={'blogBody':'测试点赞微博',
                'blogid':self.blogId,
                'haspicture':False,     # 是否有图片 有为 true 没有为false
                'whetherremind':False,  # 是否需要后台额外提醒 需要提醒为 true 否为false 默认为false
                'blogType':0,           # blogType微博类型：0：普通微博；1：公告；2：品种；3：交易动态
                'symbol':""
                }
        postShortBlogRes = Social.postShortBlog(userData['hostName'] + socialData['postShortBlog_url'],headers=self.headers,datas=params )
        self.assertEqual(postShortBlogRes.status_code, userData['status_code_200'])


        # 对该微博进行评论
        commentUrl=userData['hostName'] + socialData['addComment_url1'] + str(self.blogId) + socialData['addComment_url2']
        commentParam={'combody':'对微博进行评论','whetherremind':False}
        commentRes = Social.addComment(commentUrl,headers=self.headers,datas=commentParam)
        self.assertEqual(commentRes.status_code, userData['status_code_200'])

        #取出评论id
        self.commentId=json.loads(commentRes.text)['data']['Imsg']

    def test_praiseCommentAndDelPraiseComment(self):
        '''微博评论点赞，检查点赞的用户列表，检查收到的赞列表以及微博评论新增的赞数量'''

        # 登录账号B点赞该条微博的评论
        signinParams={"account":userData['account'], "password":userData['passwd'], "remember":False}
        signinRes = Auth.signin(userData['hostName'] + authData['signin_url'],datas=signinParams,headers=userData['headers'])
        self.assertEqual(signinRes.status_code, userData['status_code_200'])
        praiseToken = json.loads(signinRes.text)['data']['token']
        praiseHeaders=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+praiseToken})
        praiseUserId = json.loads(signinRes.text)['data']['id']

        #账号B点赞微博评论
        praiseCommentUrl=userData['hostName']+socialData['praiseComment_url']+str(self.commentId)+socialData['praiseComment_url2']
        praiseCommentRes=Social.praiseComment(praiseCommentUrl,headers=praiseHeaders)
        self.assertEqual(praiseCommentRes.status_code,userData['status_code_200'])


        # #检查微博评论点赞的用户列表
        # getUserPraiseCommentsUrl=userData['hostName']+socialData['getUserPraiseComments_url']+str(self.commentId)+socialData['getUserPraiseComments_url2']
        # userPraiseCommentParams={'id':self.commentId,
        #                          'top':100,                #获取数量
        #                          'authorId':self.userId #评论人id
        #                          }
        # userPraiseCommentRes=Social.getUserPraiseComments(getUserPraiseCommentsUrl,datas=userPraiseCommentParams,headers=self.headers)
        # self.assertEqual(userPraiseCommentRes.status_code,userData['status_code_200'])
        # #取出微博评论点赞的用户列表最新一个用户userId
        # praiseCommentUserList=json.loads(userPraiseCommentRes.text)['data']['Items']
        # # 断言，评论点赞的用户userid==取出的微博评论点赞的用户Userid
        # self.assertEqual(praiseUserId, praiseCommentUserList[0])
        # FMCommon.printLog('微博评论点赞的用户userid:'+str(praiseCommentUserList))


        #账号A检查收到的赞列表
        praiseCommentListUrl=userData['hostName'] + socialData['getPraiseList_url']
        praiseCommentListParams={'pageIndex': 1, 'pageSize': 10}
        praiseCommentListRes = Social.getPraiseList(praiseCommentListUrl, datas=praiseCommentListParams,headers=self.headers)
        self.assertEqual(praiseCommentListRes.status_code, userData['status_code_200'])
        #断言，点赞评论后，收到的赞列表的第一条点赞消息commentId = self.commentId
        PraiseUserListCommentId = json.loads(praiseCommentListRes.text)['data']['List'][0]['Comment']['Comment']['Id']
        self.assertEqual(PraiseUserListCommentId, self.commentId)

        #检查微博评论新增的点赞数量
        getNewPraiseCommentsURL=userData['hostName']+socialData['getNewPraiseComments_url']+str(self.commentId)
        newPraiseCommentsRes=Social.getNewPraiseComments(getNewPraiseCommentsURL,headers=self.headers)
        self.assertEqual(newPraiseCommentsRes.status_code,userData['status_code_200'])
        #断言，该微博评论新增的点赞数量为1
        numNewPraiseComment=json.loads(newPraiseCommentsRes.text)['data'][str(self.commentId)]
        self.assertEqual(numNewPraiseComment,1)


        #账号B取消点赞
        delPraiseCommentUrl=userData['hostName']+socialData['praiseComment_url']+str(self.commentId)+socialData['praiseComment_url2']
        delPraiseCommentRes=Social.praiseComment(delPraiseCommentUrl,headers=praiseHeaders)
        self.assertEqual(delPraiseCommentRes.status_code,userData['status_code_200'])

        # '''微博评论取消点赞后，该评论的点赞用户列表为空'''
        # #微博评论取消点赞后，检查评论的点赞用户列表
        # delUserPraiseCommentParams={'id':self.commentId,
        #                          'top':1,                #获取数量
        #                          'authorId':self.userId #评论人id
        #                          }
        # delUserPraiseCommentRes=Social.getUserPraiseComments(getUserPraiseCommentsUrl,datas=delUserPraiseCommentParams,headers=praiseHeaders)
        # self.assertEqual(delUserPraiseCommentRes.status_code,userData['status_code_200'])
        # # 取消微博评论点赞的用户列表
        # delPraiseCommentUserList = json.loads(delUserPraiseCommentRes.text)['data']['Items']
        # # 断言，微博评论取消点赞后，评论点赞的用户列表为空
        # self.assertListEqual(delPraiseCommentUserList,[])


        #微博评论取消点赞后，账号A检查，收到的赞列表，收到的评论的赞也已经删除
        # delPraiseCommentListRes = Social.getPraiseList(praiseCommentListUrl, datas=praiseCommentListParams,headers=self.headers)
        # self.assertEqual(delPraiseCommentListRes.status_code, userData['status_code_200'])
        # # 断言，微博评论取消点赞后，收到的赞列表的第一条点赞消息commentId ！= self.commentId
        # PraiseUserListCommentId = json.loads(delPraiseCommentListRes.text)['data']['List'][0]['Comment']['Comment']['Id']
        # self.assertNotEqual(PraiseUserListCommentId, self.commentId)



    def tearDown(self):
        #还原测试环境
        #删除微博
        delBlogRes=Social.deleteBlog(userData['hostName']+socialData['deleteBlog_url']+str(self.blogId),headers=self.headers)
        self.assertEqual(delBlogRes.status_code,userData['status_code_200'])

        #退出账号
        signoutRes = Auth.signout(userData['hostName'] + authData['signout_url'],datas=self.headers)
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__=='__main__':
    unittest.main()