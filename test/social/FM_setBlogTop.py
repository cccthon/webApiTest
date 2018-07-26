#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_SetHotBlogTop
# 用例标题: 置顶微博（用户ID:121145）
#流程：
    #1、登录，获取微博ID,发布微博
    #2、置顶该微博
    #3、检查热门微博列表
    #4、取消置顶
    #5、删除微博，退出账号


import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,Social,FMCommon,Http

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadSocialYML()
authData=FMCommon.loadAuthYML()

class SetHotBlogTop(unittest.TestCase):
    def setUp(self):
        # 登录账号A获取headers
        signinParams = {"account": userData['followAccount'], "password": userData['followPasswd'], "remember": False}
        signinRes = Auth.signin(userData['hostName'] + authData['signin_url'], datas=signinParams,
                                headers=userData['headers'])
        self.assertEqual(signinRes.status_code, userData['status_code_200'])
        self.token = json.loads(signinRes.text)['data']['token']
        self.headers = dict(userData['headers'], **{userData['Authorization']: userData['Bearer'] + self.token})
        self.userId = json.loads(signinRes.text)['data']['id']

        # 获取要发布的微博ID
        getBlogIdRes = Social.getBlogId(userData['hostName'] + socialData['getNewBlogid_url'], headers=self.headers)
        self.assertEqual(getBlogIdRes.status_code, userData['status_code_200'])
        self.blogId = json.loads(getBlogIdRes.text)['data']['Imsg']

        # 账号A发布微博
        params = {'blogBody': 'test blog', 'blogid': self.blogId,
                  'haspicture': False,  # 是否有图片 有为 true 没有为false
                  'whetherremind': False,  # 是否需要后台额外提醒 需要提醒为 true 否为false 默认为false
                  'blogType': 0,  # blogType微博类型：0：普通微博；1：公告；2：品种；3：交易动态
                  'symbol': ""}
        postShortBlogRes = Social.postShortBlog(userData['hostName'] + socialData['postShortBlog_url'],headers=self.headers, datas=params)
        self.assertEqual(postShortBlogRes.status_code, userData['status_code_200'])
    def test_setHotBlogTop01(self):
        '''微博置顶'''
        setHotBlogTopUrl = userData['hostName'] + socialData['setHotBlogTop_url']
        payload = {'blogId': self.blogId, 'isTop': True}
        blogTopRes = Social.setHotBlogTop(setHotBlogTopUrl, headers=self.headers, datas=payload)
        self.assertEqual(blogTopRes.status_code, userData['status_code_200'])

        # 检查热门微博第一条是否是该条微博
        blogsPayload = {'time': 48, 'pageIndex': 1, 'pageSize': 10}  # time多少小时之内的热门微博 48热门微博 24 最新微博
        MicroBlogsRes = Social.getMicroBlogs(userData['hostName'] + socialData['getMicroBlogs_url'], headers=self.headers, datas=blogsPayload)
        self.assertEqual(MicroBlogsRes.status_code, userData['status_code_200'])
        # 断言置顶成功后，第一条微博为置顶的微博
        setTopBlogId = json.loads(MicroBlogsRes.text)['data']['List'][0]['MBlog']['id']
        self.assertEqual(setTopBlogId, self.blogId)


    def tearDown(self):
        # 清空测试环境
        # 删除微博
        delBlogRes = Social.deleteBlog(userData['hostName'] + socialData['deleteBlog_url'] + str(self.blogId),headers=self.headers)
        self.assertEqual(delBlogRes.status_code, userData['status_code_200'])

        # 退出账号
        signoutRes = Auth.signout(userData['hostName'] + authData['signout_url'],datas=self.headers)
        self.assertEqual(signoutRes.status_code, userData['status_code_200'])

if __name__=='__main__':
    unittest.main()