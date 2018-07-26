#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getAtMeComment
# 用例标题: 发布@我的评论，检查@我的评论列表
# 流程：
    #1、登录
    #2、发布微博
    #3、别人评论，@我
    #4、检查@我的评论列表
    #5、删除评论，删除微博，退出登录

import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,newSocial,FMCommon,Http

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadnewSocialYML()
authData=FMCommon.loadAuthYML()

class GetAtMeComment(unittest.TestCase):
    def setUp(self):
        #登录账号
        siginParams= {"account": userData['account'], "password": userData['passwd'], "remember": False}
        siginRes=Auth.signin(userData['hostName']+authData['signin_url'],headers = userData['headers'],datas = siginParams)
        #断言返回200登录成功
        self.assertEqual(siginRes.status_code,userData['status_code_200'])
        #获取headers
        self.token=json.loads(siginRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})
        self.userId=json.loads(siginRes.text)['data']['id']
        self.nickName=json.loads(siginRes.text)['data']['nickname']

    def test_getAtMeComment(self):
        '''发布@用户的评论，检查用户的@我的评论列表'''
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
        blogId=json.loads(shortBlogRes.text)['data']['ObjectId']

        #登录账号B对微博进行评论并@账号A
        #登录账号B
        siginFollowParams= {"account": userData['followAccount'], "password": userData['followPasswd'], "remember": False}
        siginFollowRes=Auth.signin(userData['hostName']+authData['signin_url'],headers = userData['headers'],datas = siginFollowParams)
        #断言返回200登录成功
        self.assertEqual(siginFollowRes.status_code,userData['status_code_200'])
        #获取headers
        followToken=json.loads(siginFollowRes.text)['data']['token']
        followHeaders=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+followToken})

        #发布对微博的评论，并@用户A
        addCommentParams={"content": "comment blog at me @"+self.nickName,
                          "toUserId":self.userId,       #被评论人id
                          "blogId":blogId              #微博id
                          }
        addCommentRes=newSocial.addComment(userData['hostName']+socialData['addComment_url'], headers = followHeaders,datas = addCommentParams)
        #断言返回200，code=0，发布评论成功
        self.assertEqual(addCommentRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(addCommentRes.text)['code'],0)

        #获取该微博的评论列表
        # params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
        commentListRes=newSocial.getCommentList(userData['hostName']+socialData['getCommentList_url']+str(blogId),headers = self.headers)
        #断言返回200，code=0，获取微博评论列表成功
        self.assertEqual(commentListRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(commentListRes.text)['code'],0)
        #取出该微博的评论id
        commentId=json.loads(commentListRes.text)['data']['Items'][0]['Id']

        #检查用户A的@我的评论列表
        getAtMeCommentRes=newSocial.getAtMeBlogAndComment(userData['hostName']+socialData['getAtMeBlogAndComment_url']+str(userData['atmeType_comment']),headers = self.headers)
        #断言200，code=0,获取@我的微博成功
        self.assertEqual(getAtMeCommentRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getAtMeCommentRes.text)['code'],0)

        #刚发布的评论id=@我的评论第一条数据
        atMeCommentList=json.loads(getAtMeCommentRes.text)['data']['Items']
        atMeCommentInfoList=[]
        for i in atMeCommentList:
            atMeCommentInfoList.append(i['CommentInfo'])
        self.assertEqual(commentId,atMeCommentInfoList[0]['Id'])

        #删除评论
        delCommentRes=newSocial.delComment(userData['hostName']+socialData['delComment_url']+str(commentId),headers = followHeaders)
        self.assertEqual(delCommentRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(delCommentRes.text)['code'],0)

        # 删除微博
        delBlogRes = newSocial.delBlogById(userData['hostName'] + socialData['delBlogById_url'] + str(blogId),headers = self.headers)
        self.assertEqual(delBlogRes.status_code, userData['status_code_200'])
        self.assertEqual(json.loads(delBlogRes.text)['code'], 0)

    def tearDown(self):
        #清空测试环境
        #退出登录
        signOutRes=Auth.signout(userData['hostName']+ authData['signout_url'],datas = self.headers)
        self.assertEqual(signOutRes.status_code,userData['status_code_200'])
if __name__=='__main__':
    unittest.main()