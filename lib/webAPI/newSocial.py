import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http

webAPIData = FMCommon.loadWebAPIYML()
socialData = FMCommon.loadnewSocialYML()


#本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作

#发布微博
def addBlog(url, headers = "", datas = "", interfaceName = "addBlog", printLogs = 0 ):
    res=Http.post(url,headers = headers,datas = json.dumps(datas),interfaceName = interfaceName, logs = printLogs)
    return res


#上传图片
def upload(url, headers = "", datas = "", interfaceName = "addBlog", printLogs = 0 ):
    res=Http.post(url,headers = headers,datas = json.dumps(datas),interfaceName = interfaceName, logs = printLogs)
    return res


#删除微博
def delBlogById(url,headers = "", datas = "" ,interfaceName = "delBlog", printlogs = 0 ):
    res=Http.delete(url,headers = headers, datas = datas, interfaceName = interfaceName, logs = printlogs)
    return res

#获取我的微博
def getMyBlogs(url,headers = "",  params = "", interfaceName = "getMyBlogs", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res

#上传图片
def singleFileUpload(url,headers = "", datas = "",interfaceName = "", printlogs = 0):
    res=Http.post(url,headers = headers, datas = datas, interfaceName = interfaceName, logs = printlogs)
    return res

#获取品种资讯或者交易动态
def getBlogByType(url,headers = "", params = "", interfaceName = "getBlogByTypeSymbol", printlogs = 0):
    res=Http.get(url,headers = headers, params = params, interfaceName = interfaceName, logs = printlogs)
    return res

#发布评论
def addComment(url,headers = "", datas = "",interfaceName ="addComment", printlogs = 0):
    res=Http.post(url,headers = headers,datas = json.dumps(datas), interfaceName = interfaceName, logs = printlogs)
    return res

#获取我评论的列表
def getCommentFromMe(url,headers = "",  params = "", interfaceName = "getCommentFromMe", printlogs = 0 ):
    res = Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printlogs)
    return res

#获取评论我的列表
def getCommentToMe(url,headers = "",  params = "", interfaceName = "getCommentToMe", printlogs = 0 ):
    res = Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printlogs)
    return res

#获取微博评论列表
def getCommentList(url,headers = "", params = "", interfaceName = "getCommentList", printlogs = 0):
    res=Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printlogs)
    return res

#获取获取@我的微博或@我的评论
def getAtMeBlogAndComment(url,headers = "", params = "", interfaceName = "getAtMeBlogAndComment", printlogs = 0):
    res=Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printlogs)
    return res

#删除评论
def delComment(url, headers = "",datas = "", timeout= 5, interfaceName = "delComment", printlogs = 0):
    res=Http.delete(url,headers = headers ,datas = datas ,interfaceName = interfaceName, logs = printlogs)
    return res

#关注用户
def addOrCancelAttention(url,headers = "", datas = "",interfaceName ="addOrCancelAttention", printlogs = 0):
    res=Http.post(url,headers = headers,datas = json.dumps(datas), interfaceName = interfaceName, logs = printlogs)
    return res

#获取关注列表
def getMyAttentions(url,headers = "", params = "", interfaceName = "getMyAttentions", printlogs = 0):
    res=Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printlogs)
    return res

#获取粉丝列表
def getMyFans(url,headers = "", params = "", interfaceName = "getMyFans", printlogs = 0):
    res=Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printlogs)
    return res

#收藏或取消收藏微博
def addOrCancelCollect(url,headers = "", datas = "",interfaceName ="addOrCancelCollect", printlogs = 0):
    res=Http.post(url,headers = headers,datas = json.dumps(datas), interfaceName = interfaceName, logs = printlogs)
    return res

#获取我的收藏列表
def getMyCollect(url,headers = "", params = "", interfaceName = "getMyCollect", printlogs = 0):
    res=Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printlogs)
    return res

#点赞微博
def addOrCancelPraise(url,headers = "", datas = "",interfaceName ="addOrCancelPraise", printlogs = 0):
    res=Http.post(url,headers = headers,datas = json.dumps(datas), interfaceName = interfaceName, logs = printlogs)
    return res

#获取微博对应的赞
def getPraiseList(url,headers = "", params = "", interfaceName = "getPraiseList", printlogs = 0):
    res=Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printlogs)
    return res

#收到的赞列表
def getMyReceive(url,headers = "", params = "", interfaceName = "getMyReceivePraise", printlogs = 0):
    res=Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printlogs)
    return res

#根据关键字搜索
def searchByKeyWord(url,headers = "", params = "", interfaceName = "searchByKeyWord", printlogs = 0):
    res=Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printlogs)
    return res

def setUserNickname(url, headers = "",datas = "", interfaceName = "setUserNickname", printlogs = 0):
    res=Http.put(url, headers = headers,datas = datas, interfaceName = interfaceName, logs = printlogs)
    return res

#分享微博
def blogShare(url,headers = "",  params = "", interfaceName = "blogShare", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res

#获取所有微博动态
def getAllBlog(url, headers = "", params = "", interfaceName = "getAllBlog", printlogs = 0):
    res=Http.get(url,headers = headers, params = params, interfaceName = interfaceName, logs = printlogs)
    return res

#获取热门微博
def getHotBlog(url, headers = "", params = "", interfaceName = "getHotBlog", printlogs = 0):
    res = Http.get(url, headers = headers, params = params, interfaceName = interfaceName, logs = printlogs)
    return res

#按推荐位获取热门推荐
def getBlogByLocation(url, headers = "", params = "", interfaceName = "getBlogByLocation", printlogs = 0):
    res = Http.get(url, headers = headers, params = params, interfaceName = interfaceName, logs = printlogs)
    return res

#根据PostType类型获取相应的微博 
def getBlogByPostType(url, headers = "", params = "", interfaceName = "getBlogByPostType", printlogs = 0):
    res = Http.get(url, headers = headers, params = params, interfaceName = interfaceName, logs = printlogs)
    return res

#获取所有微博动态
def getAllBlog(url,headers = "",  params = "", interfaceName = "getAllBlog", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res

#获取热门微博
def getHotBlog(url,headers = "",  params = "", interfaceName = "getHotBlog", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res

#分享微博
def blogShare(url,headers = "",  params = "", interfaceName = "blogShare", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res

#按推荐位获取热门推荐
def getBlogByLocation(url,headers = "",  params = "", interfaceName = "getBlogByLocation", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res

#根据PostType类型获取相应的微博
def getBlogByPostType(url,headers = "",  params = "", interfaceName = "getBlogByPostType", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res

#获取微博详情
def getBlogDetail(url,headers = "",  params = "", interfaceName = "getBlogDetail", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res

#获取公告banner列表
def getNoticeList(url,headers = "",  params = "", interfaceName = "getNoticeList", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res

#获取微博最后id
def getLastId(url,headers = "",  params = "", interfaceName = "getLastId", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res

#获取全局提醒列表[需要登录]
def getGlobalRemind(url,headers = "",  params = "", interfaceName = "getGlobalRemind", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res

#获取财经要闻
def getFinanceList(url,headers = "",  params = "", interfaceName = "getFinanceList", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res

#获取财经要闻页的热门推荐
def getHotRecommendList(url,headers = "",  params = "", interfaceName = "getHotRecommendList", printlogs = 0 ):
    res=Http.get(url,headers = headers, params = params,interfaceName = interfaceName, logs = printlogs)
    return res