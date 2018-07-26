#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_getBlogByPostType

# 用例标题: 根据PostType类型获取相应的微博 
# 流程：
    #1、获取名人大咖微博
    #2、获取获取分析师微博
    #3、获取经纪商微博

# 脚本作者: zhangyanyun
# 写作日期: 2018/06/29
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
        #获取名人大咖微博
        params={"pageIndex":1,"pageSize":15,"type":3}  #有默认值可以不用传参
        #发布类型： 3：名人大咖  4：分析师  5：媒体号  6：经纪商
        getBlogByType=newSocial.getBlogByPostType(userData['hostName']+socialData['getBlogByPostType_url'],params=params)
        #断言返回200，code=0,获取热门微博列表成功
        self.assertEqual(getBlogByType.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getBlogByType.text)['code'],0)

    def test_getBlogByType002(self):
        #获取名人大咖微博
        params={"pageIndex":1,"pageSize":15,"type":4}  #有默认值可以不用传参
        #发布类型： 3：名人大咖  4：分析师  5：媒体号  6：经纪商
        getBlogByType=newSocial.getBlogByPostType(userData['hostName']+socialData['getBlogByPostType_url'],params=params)
        #断言返回200，code=0,获取热门微博列表成功
        self.assertEqual(getBlogByType.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getBlogByType.text)['code'],0)

    def test_getBlogByType003(self):
        #获取名人大咖微博
        params={"pageIndex":1,"pageSize":15,"type":6}  #有默认值可以不用传参
        #发布类型： 3：名人大咖  4：分析师  5：媒体号  6：经纪商
        getBlogByType=newSocial.getBlogByPostType(userData['hostName']+socialData['getBlogByPostType_url'],params=params)
        #断言返回200，code=0,获取热门微博列表成功
        self.assertEqual(getBlogByType.status_code,userData['status_code_200'])
        self.assertEqual(json.loads(getBlogByType.text)['code'],0)

    


    def tearDown(self):
        pass


if __name__=='__main__':
    unittest.main()
