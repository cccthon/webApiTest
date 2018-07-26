#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_addOrCancelPraise
# 用例标题: 点赞微博，获取微博对应的赞，获取用户收到的赞，取消点赞
# 流程：
    #1、登录账号A
    #2、发布微博
    #3、登录账号B点赞微博，获取微博对应的赞
    #4、账号A检查收到的赞
    #5、账号B取消点赞
    #6、删除微博，退出账号

import sys,requests,unittest,yaml,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,newSocial,FMCommon,Http,time

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadnewSocialYML()
authData=FMCommon.loadAuthYML()

class addOrCancelPraise(unittest.TestCase):
    def setUp(self):
        #登录账号A
        siginParams= {"account": userData['account'], "password": userData['passwd'], "remember": False}
        siginRes=Auth.signin(userData['hostName']+authData['signin_url'],headers = userData['headers'],datas = siginParams)
        #断言返回200登录成功
        self.assertEqual(siginRes.status_code,userData['status_code_200'])
        #获取headers
        self.token=json.loads(siginRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})
        self.userId=json.loads(siginRes.text)['data']['id']

        #登录账号B
        siginFollowParams= {"account": userData['followAccount'], "password": userData['followPasswd'], "remember": False}
        siginFollowRes=Auth.signin(userData['hostName']+authData['signin_url'],headers = userData['headers'],datas = siginFollowParams)
        #断言返回200登录成功
        self.assertEqual(siginFollowRes.status_code,userData['status_code_200'])
        #获取headers
        self.followToken=json.loads(siginFollowRes.text)['data']['token']
        self.followHeaders=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.followToken})
        self.followUserId=json.loads(siginFollowRes.text)['data']['id']

    def test_addAndCancelPraise(self):
        '''登录账号A，发布微博-》登录账号B,点赞该微博，获取该微博对应的赞-》账号A查看收到的赞列表-》取消点赞,删除微博，退出账号'''

        #发布微博
        blogParams={"isLongBlog": False,                     #boolean  true表示长微博，false表示短微博
                    "body": "test short blog test",          #短微博内容
                    "blogType": 0,                           #微博类型：0：普通微博；1：公告；2：品种资讯；3：交易动态
                    "symbol": "",
                    "postType": 0                            #发布类型: 0-用户微博,1-推广,2-认证用户微博,3-名人大咖,4-分析师,5-媒体号,6-经纪商
                   }
        shortBlogRes=newSocial.addBlog(userData['hostName']+socialData['addBlog_url'],headers = self.headers,datas = blogParams)
        #断言返回200，发布微博成功
        self.assertEqual(shortBlogRes.status_code,userData['status_code_200'],"微博发布失败")
        self.assertEqual(json.loads(shortBlogRes.text)['code'],userData['code_0'])
        #获取微博id,用于删除微博
        blogId=json.loads(shortBlogRes.text)['data']['ObjectId']

        #点赞微博
        praiseBlogParams={'toUserId':self.userId,      #用户id
                          'objId':blogId,              #微博id
                          'type':1                     #type=1微博 2评论
                          }
        praiseBlogRes=newSocial.addOrCancelPraise(userData['hostName']+socialData['addOrCancelPraise_url'],datas = praiseBlogParams,headers = self.followHeaders)
        #断言返回200，code=0,点赞成功
        self.assertEqual(praiseBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(praiseBlogRes.text)['code'],userData['code_0'])

        #获取该微博对应的赞
        blogPraiseListParams={'type':1}  #type=1 微博
        blogPraiseListRes=newSocial.getPraiseList(userData['hostName']+socialData['getPraiseList_url']+str(blogId),params = blogPraiseListParams, headers = self.followHeaders)
        #断言返回200，code=0,点赞成功
        self.assertEqual(blogPraiseListRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(blogPraiseListRes.text)['code'],userData['code_0'])
        #断言，该微博的赞的数量为1
        self.assertEqual(int(json.loads(blogPraiseListRes.text)['data']['TotalCount']),1)

        #账号A检查收到的赞列表
        getMyReceiveRes=newSocial.getMyReceive(userData['hostName']+socialData['getMyReceive_url'],headers = self.headers )
        #断言返回200，code=0,点赞成功
        self.assertEqual(getMyReceiveRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getMyReceiveRes.text)['code'],userData['code_0'])
        #断言，收到的赞列表第一条微博为该微博
        blogIdList=json.loads(getMyReceiveRes.text)['data']['Items'][0]['BlogInfo']['Id']
        self.assertEqual(blogIdList,blogId,"新收到的赞，没有显示在第一位")

        #取消点赞
        cancelPraiseBlogRes=newSocial.addOrCancelPraise(userData['hostName']+socialData['addOrCancelPraise_url'],datas = praiseBlogParams,headers = self.followHeaders)
        #断言返回200，code=0,点赞成功
        self.assertEqual(cancelPraiseBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(cancelPraiseBlogRes.text)['code'],userData['code_0'])

        #删除微博
        delBlogRes=newSocial.delBlogById(userData['hostName']+socialData['delBlogById_url']+str(blogId),headers = self.headers)
        self.assertEqual(delBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(delBlogRes.text)['code'],0)

    def tearDown(self):
        #退出登录
        signOutRes=Auth.signout(userData['hostName']+ authData['signout_url'],datas = self.headers)
        self.assertEqual(signOutRes.status_code,userData['status_code_200'])
if __name__=='__main__':
    unittest.main()