import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http
from socketIO_client import SocketIO
from base64 import b64encode

webAPIData = FMCommon.loadWebAPIYML()
socialData = FMCommon.loadSocialYML()
#本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作
# 获取发布微博的id
def getBlogId(url,headers=""):
    res = Http.get(url,headers=headers,interfaceName="getBlogId")
    return res

#发短微博
def postShortBlog(url,headers,datas=""):
    res=Http.post(url,headers=headers,datas=json.dumps(datas),interfaceName="postShortBlog")
    return res

#发长微博
def postLongBlog(url,headers,datas=""):
    res=Http.post(url,headers=headers,datas=json.dumps(datas),interfaceName="postLongBlog")
    return res

#批量上传文件(传参方式：form-data)
def multiFileUpload(url,headers,datas=""):
    res=Http.post(url,headers=headers,datas=datas,interfaceName="multiFileUpload")
    return res


#删除微博
def deleteBlog(url,headers):
    res=Http.delete(url,headers=headers,interfaceName="deleteBlog")
    return res

#发布对微博的评论
def addComment(url,headers="",datas=""):
    # datas={'combody':combody,'whetherremind':False}
    res=Http.post(url,headers=headers,datas=json.dumps(datas),interfaceName="addComment")
    return res

#回复微博评论
def replyComment(url,headers="",datas=""):
    res=Http.post(url,headers=headers,datas=json.dumps(datas),interfaceName="replyComment")
    return res

#我评论的列表
def getMyComments(url,headers,datas=""):
    res=Http.get(url,headers=headers,params=json.dumps(datas),interfaceName="getMyComments")
    return res

#评论我的列表
def getCommentsAboutMe(url,headers,datas=""):
    res=Http.get(url,headers=headers,params=json.dumps(datas),interfaceName="getCommentsAboutMe")
    return res

#删除评论
def deleteComment(url,headers):
    res=Http.delete(url,headers=headers,interfaceName="deleteComment")
    return res

#微博点赞
def praiseBlog(url,headers):
    res=Http.put(url,headers=headers,interfaceName="praiseBlog")
    return res

#微博评论点赞
def praiseComment(url,headers):
    res=Http.put(url,headers=headers,interfaceName="praiseComment")
    return res

#获取微博新增的点赞数量
def getNewPraiseMicroBlogs(url,datas="",headers=""):
    # datas={'ids':ids}
    res=Http.get(url,headers=headers,interfaceName="getNewPraiseMicroBlogs")
    return res

#获取微博评论新增的点赞数量
def getNewPraiseComments(url,datas="",headers=""):
    res=Http.get(url,headers=headers,interfaceName="getNewPraiseComments")
    return res

#获取微博点赞的用户列表
def getUserPraiseMicroBlogs(url,datas="",headers=""):
    # datas={'id':id,'top':top,'authorId':authorId}
    res=Http.get(url,params=json.dumps(datas),headers=headers,interfaceName="getUserPraiseMicroBlogs")
    return res

#获取微博评论点赞的用户列表
def getUserPraiseComments(url,datas="",headers=""):
    res=Http.get(url,params=json.dumps(datas),headers=headers,interfaceName="getUserPraiseComments")
    return res


#收到的赞列表
def getPraiseList(url,datas,headers=""):
    # datas = {"pageIndex": pageIndex, "pageSize": pageSize}
    res=Http.get(url,headers=headers,params=json.dumps(datas),interfaceName="getPraiseList")
    return res


#收藏微博
def collectBlog(url,headers):
    res=Http.put(url,headers=headers,interfaceName="collectBlog")
    return res

#我的收藏列表
def getCollectionList(url,datas="",headers=""):
    # datas = {"pageIndex": pageIndex, "pageSize": pageSize}
    res=Http.get(url,headers=headers,params=json.dumps(datas),interfaceName="getCollectionList")
    return res

#关注用户
def attentionUser(url,headers=""):
    res=Http.put(url,headers=headers,interfaceName="attentionUser")
    return res

#获取关注列表
def getMyAttentions(url,datas="",headers=""):
    # datas = {"pageIndex": pageIndex, "pageSize": pageSize}
    res=Http.get(url,headers=headers,params=json.dumps(datas),interfaceName="getMyAttentions")
    return res

#获取粉丝列表
def getMyFans(url,datas="",headers=""):
    # datas = {"pageIndex": pageIndex, "pageSize": pageSize}
    res=Http.get(url,headers=headers,params=json.dumps(datas),interfaceName="getMyFans")
    return res


#微博分享
def blogShare(url,headers="",datas=""):
    # datas={'blogId':blogId}
    res=Http.get(url,headers=headers,params=json.dumps(datas),interfaceName="blogShare")
    return res

#获取所有微博动态
def getAllBlog(url,headers="",datas=""):
    res=http.get(url,headers=headers,params=json.dumps(datas),interfaceName="getAllBlog")
    return res

#获取热门微博
def getMicroBlogs(url,headers="",datas=""):
    res=Http.get(url,headers=headers,params=json.dumps(datas),interfaceName="getMicroBlogs")
    return res

#获取我的微博列表
def getMyBlogList(url,datas="",headers=""):
    # datas = {"pageIndex": pageIndex, "pageSize": pageSize,'startId':startId}
    res=Http.get(url,headers=headers,params=datas,interfaceName="getMyBlogList")
    return res

#@用户
def getFriends(url,headers="",datas=""):
    res=Http.get(url,headers=headers,params=json.dumps(datas),interfaceName="getFriends")
    return res

#微博置顶
def setHotBlogTop(url,datas="",headers=""):
    res=Http.post(url,headers=headers,datas=json.dumps(datas),interfaceName="setHotBlogTop")
    return res

#获取@我的评论列表
def getAtMeComments(url,datas= "",headers = ""):
    res = Http.get(url, headers=headers, params=json.dumps(datas), interfaceName="getAtmeComments")
    return res


##################################################################################################
################################### social 通用方法 ##############################################

#通过搜索结果，获取用户的userid
def getUserID(url=webAPIData['hostName'] + socialData['searchUsers_url'] + "?pageIndex=1&pageSize=15&keyWord=", keyword="",headers="", params="", interfaceName="", printLogs=0):
    res = Http.get(url + keyword, headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    return json.loads(res.text)['data']['List'][0]['id']

