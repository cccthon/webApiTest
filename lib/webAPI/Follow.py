import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http
from socketIO_client import SocketIO
from base64 import b64encode

userData = FMCommon.loadWebAPIYML()

#获取指定交易员存在的跟随关系
def getFollow(url,traderindex="",accountIndex="",headers=""):
    res=requests.get(url+str(traderindex)+userData['accountIndex']+str(accountIndex),headers=headers)
    return res

#修改一个跟随
def updateFollow(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.put(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

#取消跟随
def DeleteFollow(url, headers="", interfaceName="", printLogs=0):
    res = Http.delete(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

#获取跟随(正在/历史)废弃
def getFollowers(url,headers="",isFollowing="",pageSize="",pageIndex="",pageField="",pageSort="",isReal="",direction="",strategy="",agency="",keyword=""):
    params={
        "isFollowing": isFollowing,
        "pageSize": pageSize,
        "pageIndex": pageIndex,
        "pageField": pageField,
        "pageSort": pageSort,
        "isReal": isReal,
        "direction": direction,
        "strategy": strategy,
        "agency": agency,
        "keyword": keyword
    }
    res=requests.get(url,headers=headers,params=json.dumps(params))
    return res

#获取跟随(正在/历史)
def getFollowersnew(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res


#获取跟随者概要废弃
def getFollowerSummary(url,headers="",flag=""):
    params={
        "flag": flag
    }
    res=requests.get(url,headers=headers,params=json.dumps(params))
    return res

#获取跟随者概要
def getFollowerSummarynew(url, headers="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,interfaceName=interfaceName, logs=printLogs)
    return res

#获取跟随交易员列表(正在/历史)(废弃)
def getFollows(url,headers="",isFollowing="",pageSize="",pageField="",pageIndex="",isAutonomy="",direction="",strategy="",agency="",keyword="",flag=""):
    params={
        "isFollowing": isFollowing,
        "pageSize": pageSize,
        "pageIndex": pageIndex,
        "pageField": pageField,
        "isAutonomy": isAutonomy,
        "direction": direction,
        "strategy": strategy,
        "agency": agency,
        "keyword": keyword,
        "flag": flag
    }
    res=requests.get(url,headers=headers,params=json.dumps(params))
    return res

#获取指定交易员存在的跟随关系
def getFollowsnew(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

#获取跟随概要(废弃)
def getFollowSummary(url,headers=""):
    res=requests.get(url,headers=headers)
    return res

#获取跟随概要
def getFollowSummarynew(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

#新建跟随
def createFollow(url, headers="", datas="", interfaceName="", printLogs=1):
    res = Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

#取消跟随
def deleteFollow(url,headers=""):
    res=requests.delete(url,headers=headers)
    return res

def getStatisticsOfAccount(url, headers="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,interfaceName=interfaceName, logs=printLogs)
    return res

#排行榜-跟随者跟随组合交易员
def follows(url,headers="",datas="",timeout=60,interfaceName="", printLogs=0):
    res= Http.post(url,headers=headers,datas=json.dumps(datas),timeout=timeout,interfaceName=interfaceName,logs=printLogs)
    return res

##########################  通用方法 #############################
#通过nickName获取用户的userID
#传入nickName即可
def getUserID(url="", headers="", params="", interfaceName="", printLogs=1):
    res = Http.get(userData['hostName'] + userData['getTraders_url'], headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    return json.loads(res.text)['data']['items'][0]['UserId']

#跟随者自主解除跟随订单
def unfollowOrder(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res
