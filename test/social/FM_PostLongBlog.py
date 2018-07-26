
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_PostLongBlog
# 流程:
# 1、登录--》获取微博id，发布一条长微博
# 2、删除微博，退出登录
import sys,requests,unittest,yaml,json,time,imghdr
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,Social,FMCommon,Http



userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadSocialYML()
authData=FMCommon.loadAuthYML()

class PostLongBlog(unittest.TestCase):
    def setUp(self):
        signinParams={"account":userData['followAccount'], "password":userData['followPasswd'], "remember":False}
        singinRes = Auth.signin(userData['hostName'] + authData['signin_url'],datas=signinParams, headers=userData['headers'])
        self.assertEqual(singinRes.status_code, userData['status_code_200'])
        self.token = json.loads(singinRes.text)['data']['token']
        self.headers=dict(userData['headers'],**{userData['Authorization'] : userData['Bearer']+self.token})
        self.nickName=json.loads(singinRes.text)['data']['nickname']

    # 获取发布微博的id
        getBlogIdRes=Social.getBlogId(userData['hostName']+socialData['getNewBlogid_url'],headers=self.headers)
        self.assertEqual(getBlogIdRes.status_code, userData['status_code_200'])
        self.blogId=json.loads(getBlogIdRes.text)['data']['Imsg']



    def test_ostLongBlog_001(self):
        '''发布不带图片的长微博'''
        params={"blogBody":"<p>微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文"
                           "的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的微博正文的</p>",
                "blogTitle":"标题",       #长微博标题
                "blogIntro":"导语",       #长微博导语
                "longblogimg":"",         #长微博缩略图
                "noIntro":False,          #是否带导语，不带为true
                "blogid":self.blogId,     #微博id
                "whetherremind":False,    #是否需要后台额外提醒 需要提醒为 true 否为false 默认为false
                "blogType": 0,            #微博类型：0：普通微博；1：公告；2：品种；3：交易动态
                "symbol":""
                }
        longBlogRes=Social.postLongBlog(userData['hostName']+socialData['postLongBlog_url'],datas=params,headers=self.headers)
        self.assertEqual(longBlogRes.status_code,userData['status_code_200'])

        # 检查我的微博列表存在该微博
        blogListParams = {'pageIndex': 1, 'pageSize': 10}
        myblogListRes = Social.getMyBlogList(userData['hostName'] + socialData['getMyBlogList_url'], headers=self.headers,datas=blogListParams)
        self.assertEqual(myblogListRes.status_code, userData['status_code_200'])
        MyBlogList = json.loads(myblogListRes.text)['data']['List']
        self.assertEqual(self.blogId, MyBlogList[0]['MBlog']['id'])

        # 删除微博
        delBlogRes = Social.deleteBlog(userData['hostName'] + socialData['deleteBlog_url'] + str(self.blogId),headers=self.headers)
        self.assertEqual(delBlogRes.status_code, userData['status_code_200'])

    def tearDown(self):
        # 清空测试环境,退出登录
        signout = Auth.signout(userData['hostName']+ authData['signout_url'],datas=self.headers)
        self.assertEqual(signout.status_code, userData['status_code_200'])

if __name__ == '__main__':
    unittest.main()



