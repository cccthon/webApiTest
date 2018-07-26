#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_addOrCancelCollect
# 用例标题: 收藏微博，检查我的收藏列表
# testcase0011：
    #1、登录
    #2、收藏微博
    #3、检查我的收藏列表

import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,newSocial,FMCommon,Http

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadnewSocialYML()
authData=FMCommon.loadAuthYML()

class CollectBlog(unittest.TestCase):
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

    def test_addOrCancelCollectBlog(self):
        '''收藏微博，检查我的收藏列表，取消收藏'''
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

        #收藏微博
        collectBlogParams={"objId":blogId,    #被收藏的微博ID
                           "type":0           #type=0微博
                          }
        collectBlogRes=newSocial.addOrCancelCollect(userData['hostName']+socialData['addOrCancelCollect_url'],headers = self.headers,datas = collectBlogParams)
        #断言返回200，code=0，收藏微博成功
        self.assertEqual(collectBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(collectBlogRes.text)['code'],userData['code_0'])

        #检查我的收藏列表
        collectBlogListRes=newSocial.getMyCollect(userData['hostName']+socialData['getMyCollect_url'],headers = self.headers)
        #断言返回200，code=0,获取我的收藏列表成功
        self.assertEqual(collectBlogListRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(collectBlogListRes.text)['code'],userData['code_0'])
        #获取我的收藏列表第一条微博
        collectBlogId=json.loads(collectBlogListRes.text)['data']['Items'][0]['BlogInfo']['Id']
        self.assertEqual(blogId,collectBlogId)

        #取消收藏
        cancelCollectBlogRes=newSocial.addOrCancelCollect(userData['hostName']+socialData['addOrCancelCollect_url'],headers = self.headers,datas = collectBlogParams)
        #断言返回200，code=0，收藏微博成功
        self.assertEqual(cancelCollectBlogRes.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(cancelCollectBlogRes.text)['code'],userData['code_0'])

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