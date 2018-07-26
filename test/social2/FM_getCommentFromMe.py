#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getCommentFromMe
# 用例标题: 获取我评论的
# 流程：
    #1、登录
    #2、发布微博，并评论
    #3、获取我评论的列表
    #4、删除评论，删除微博
    #5、退出登录

import sys,requests,unittest,yaml,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,newSocial,FMCommon,Http,time

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadnewSocialYML()
authData=FMCommon.loadAuthYML()

class GetCommentFromMe(unittest.TestCase):
    def setUp(self):
        #登录账号
        signinPrams={"account":userData['account'],"password":userData['passwd'],"remember":False}
        signinRes=Auth.signin(userData['hostName']+authData['signin_url'],headers = userData['headers'],datas = signinPrams)
        #断言返回200，登录成功
        self.assertEqual(signinRes.status_code,userData['status_code_200'])
        #获取headers
        self.token=json.loads(signinRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization']:userData['Bearer']+self.token})
        self.userId=json.loads(signinRes.text)['data']['id']

    def test_getCommentFromMe(self):
        '''登录，发布微博，并评论，获取我评论的列表-》删除评论，删除微博，退出登录'''

        #发布微博
        blogParams = {"isLongBlog": False,  # boolean  true表示长微博，false表示短微博
                      "body": "test short blog test",  # 短微博内容
                      "blogType": 0,  # 微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
                      "symbol": "", "postType": 0  # 发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
                     }
        shortBlogRes = newSocial.addBlog(userData['hostName'] + socialData['addBlog_url'], headers=self.headers,datas=blogParams)
        # 断言返回200，发布微博成功
        self.assertEqual(shortBlogRes.status_code, userData['status_code_200'], "微博发布失败")
        self.assertEqual(json.loads(shortBlogRes.text)['code'],userData['code_0'])
        # 获取微博id,用于删除微博
        blogId = json.loads(shortBlogRes.text)['data']['ObjectId']


        #对微博进行评论
        addCommentParams={"content": "comment blog",
                          "toUserId":self.userId,           #被评论人id
                          "blogId":blogId              #微博id
                          }
        addCommentRes=newSocial.addComment(userData['hostName']+socialData['addComment_url'], headers = self.headers,datas = addCommentParams)
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

        #获取我评论的列表
        # params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
        commentFromMeRes=newSocial.getCommentFromMe(userData['hostName']+socialData['getCommentFromMe_url'], headers = self.headers)
        #断言返回200，code=0，获取我评论的列表成功
        self.assertEqual(commentFromMeRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(commentFromMeRes.text)['code'],0)
        #断言，刚发布的评论存在于我评论的列表中
        commentList=json.loads(commentFromMeRes.text)['data']['Items']
        commentIdList=[]
        for i in commentList:
            commentIdList.append(i['Id'])
        self.assertIn(commentId,commentIdList)

        # #删除评论
        # delCommentRes=newSocial.delComment(userData['hostName']+socialData['delComment_url']+str(commentId),headers = self.headers)
        # self.assertEqual(delCommentRes.status_code,userData['status_code_200'])
        # self.assertEqual(json.loads(delCommentRes.text)['code'],0)

        #删除微博
        delBlogRes=newSocial.delBlogById(userData['hostName']+socialData['delBlogById_url']+str(blogId),headers = self.headers)
        self.assertEqual(delBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(delBlogRes.text)['code'],0)


    def tearDown(self):
        #清空测试环境，退出登录
        signoutRes=Auth.signout(userData['hostName']+authData['signout_url'],datas = self.headers)
        self.assertEqual(signoutRes.status_code,userData['status_code_200'])

if __name__=='__main__':
    unittest.TestCase()