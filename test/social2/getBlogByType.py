#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_blogShare
# 用例标题: 获取品种资讯或交易动态 
# 流程：
    #1、获取品种资讯
    #2、获取交易动态 

# 脚本作者: zhangyanyun
# 写作日期: 2018/06/28
#=========================================================

import sys,requests,unittest,yaml,json,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
sys.path.append("../../lib/http")
import Auth,newSocial,FMCommon,Http
from requests_toolbelt.multipart import MultipartEncoder

userData = FMCommon.loadWebAPIYML()
socialData=FMCommon.loadnewSocialYML()
authData=FMCommon.loadAuthYML()

class Blog(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_getBlogByType001(self):
        #获取品种资讯
        params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
        type = 2  #博客类型：0-普通微博，1-公告，2-品种资讯，3-交易动态
        getBlogByType=newSocial.getBlogByType(userData['hostName']+socialData['getBlogByType_url']+str(type),params=params)
        #断言返回200，code=0,获取热门微博列表成功
        self.assertEqual(getBlogByType.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getBlogByType.text)['code'],0)

    def test_getBlogByType002(self):0
        #获取交易动态
        params={"pageIndex":1,"pageSize":15}  #有默认值可以不用传参
        type = 3  #博客类型：0-普通微博，1-公告，2-品种资讯，3-交易动态
        getBlogByType=newSocial.getBlogByType(userData['hostName']+socialData['getBlogByType_url']+str(type),params=params)
        #断言返回200，code=0,获取热门微博列表成功
        self.assertEqual(getBlogByType.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getBlogByType.text)['code'],0)


    def tearDown(self):
        pass


if __name__=='__main__':
    unittest.main()
