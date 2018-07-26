#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_WebAPI_CollectBlog
# 流程:
    # 1、登录账号A,发布一条短微博
    # 2、登录账号收藏微博，检查我的收藏列表
    # 3、账号B取消收藏，检查我的收藏列表
    # 4、删除微博，退出登录

import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,Social,FMCommon,Http

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadSocialYML()
authData=FMCommon.loadAuthYML()

class CollectBlog(unittest.TestCase):
    def setUp(self):

        # 登录获取headers
        signinParams={"account":userData['account'], "password":userData['passwd'], "remember":False}
        signinRes = Auth.signin(userData['hostName'] + authData['signin_url'],datas=signinParams, headers=userData['headers'])
        self.assertEqual(signinRes.status_code, userData['status_code_200'])
        self.token = json.loads(signinRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})


        # 获取要发布的微博ID
        getBlogIdRes = Social.getBlogId(userData['hostName'] + socialData['getNewBlogid_url'], headers=self.headers)
        self.assertEqual(getBlogIdRes.status_code, userData['status_code_200'])
        self.blogId = json.loads(getBlogIdRes.text)['data']['Imsg']

        # 发布微博
        params={'blogBody':'测试收藏微博微博',
                'blogid':self.blogId,
                'haspicture':False,     # 是否有图片 有为 true 没有为false
                'whetherremind':False,  # 是否需要后台额外提醒 需要提醒为 true 否为false 默认为false
                'blogType':0,           # blogType微博类型：0：普通微博；1：公告；2：品种；3：交易动态
                'symbol':""
                }
        postShortBlogRes = Social.postShortBlog(userData['hostName'] + socialData['postShortBlog_url'],headers=self.headers,datas=params)
        self.assertEqual(postShortBlogRes.status_code, userData['status_code_200'])


    def test_collectBlog(self):
        '''收藏微博，检查我的收藏列表，取消收藏，检查我的收藏列表'''
        #登录账号B收藏微博
        signinParams={"account":userData['followAccount'], "password":userData['followPasswd'], "remember":False}
        singinRes = Auth.signin(userData['hostName'] + authData['signin_url'], datas=signinParams, headers=userData['headers'])
        self.assertEqual(singinRes.status_code, userData['status_code_200'])
        tokenRes = json.loads(singinRes.text)['data']['token']
        headersRes=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+tokenRes})


        #账号B收藏微博，断言，返回200即成功
        collectBlogRes = Social.collectBlog(userData['hostName'] + socialData['collectBlog_url1'] + str(self.blogId) + socialData['collectBlog_url2'],headers=headersRes)
        self.assertEqual(collectBlogRes.status_code, userData['status_code_200'])


        #检查我的收藏列表
        params={'pageIndex':1,'pageSize':10}
        collectBlogListRes=Social.getCollectionList(userData['hostName']+socialData['getCollectionList_url'],datas=params,headers=headersRes)
        self.assertEqual(collectBlogListRes.status_code,userData['status_code_200'])
        collectBlogList=json.loads(collectBlogListRes.text)['data']['List']

        #断言：B收藏A的微博后，该微博存在于B的我的收藏列表中
        collectBlogListId=[]
        for i in collectBlogList:
            collectBlogListId.append(i['MBlog']['id'])
        self.assertIn(self.blogId,collectBlogListId)


        #取消收藏，断言，返回200即成功
        delCollectBlogRes=Social.collectBlog(userData['hostName'] + socialData['collectBlog_url1'] + str(self.blogId) + socialData['collectBlog_url2'],headers=headersRes)
        self.assertEqual(delCollectBlogRes.status_code, userData['status_code_200'])


        #取消收藏后，检查我的收藏列表
        delcollectBlogListRes=Social.getCollectionList(userData['hostName']+socialData['getCollectionList_url'],datas=params,headers=headersRes)
        self.assertEqual(delcollectBlogListRes.status_code,userData['status_code_200'])
        delcollectBlogList=json.loads(delcollectBlogListRes.text)['data']['List']
        #断言，B取消收藏后，我的收藏列表没有该条微博
        delCollectBlogListId = []
        for x in delcollectBlogList:
            delCollectBlogListId.append(x['MBlog']['id'])
        self.assertNotIn(self.blogId, delCollectBlogListId)




    def tearDown(self):
        #清空测试环境

        # 删除微博
        delBlogRes=Social.deleteBlog(userData['hostName']+socialData['deleteBlog_url']+str(self.blogId),headers=self.headers)
        self.assertEqual(delBlogRes.status_code,  userData['status_code_200'])

        #退出登录
        signout = Auth.signout(userData['hostName']+ authData['signout_url'],datas=self.headers)
        self.assertEqual(signout.status_code, userData['status_code_200'])


if __name__ == '__main__':
    unittest.main()