import sys,os,json,requests,yaml,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http
from socketIO_client import SocketIO
from base64 import b64encode
from retrying import retry
userData = FMCommon.loadWebAPIYML()
followData = FMCommon.loadFollowYML()

#新建跟随
# 接口名称：createFollow
# 请求方法：post
# 请求url：api/v1/trade/follows/:trader_index
# 入参：
'''
字段              类型  描述
trader_index    string  交易员 ID 和账号索引（如：74592_3）
accountIndex    number  当前登录用户的账号索引（如：1）
strategy        string  跟随策略(fixed: 固定手数,ratio: 按比例)
setting         number  跟随配置（根据跟随策略不同而表示的意义不同，比如 1.00 固定手数时表示 1 手，按比例时表示 1 倍）
direction       string  跟随方向(positive: 正向跟随,negative: 反向跟随)
'''
def createFollow(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

#获取指定交易员存在的跟随关系
# 接口名称：getFollow
# 请求方法：get
# 请求url：/api/v1/trade/follows/74592_3?accountIndex=1
# 入参：
'''
字段              类型  描述
trader_index    string  交易员 ID 和账号索引（如：74592_3）
accountIndex    number  当前登录用户的账号索引（如：1）
'''
def getFollow(url, traderindex="", accountIndex="", headers="", interfaceName="", printLogs=0):
    res = Http.get(url + traderindex + userData['accountIndex'] + str(accountIndex), headers=headers)
    return res

#修改一个跟随
# 接口名称：updateFollow
# 请求方法：put
# 请求url：/api/v1/trade/follows/74592_3
# 入参：
'''
trader_index    string  交易员 ID 和账号索引（如：74592_3）
accountIndex    number  当前登录用户的账号索引（如：1）
strategy        string  跟随策略(fixed: 固定手数,ratio: 按比例)
setting         number  跟随配置（根据跟随策略不同而表示的意义不同，比如 1.00 固定手数时表示 1 手，按比例时表示 1 倍）
direction       string  跟随方向(positive: 正向跟随,negative: 反向跟随)
'''
def updateFollow(url, traderindex="", headers="", datas="", interfaceName="", printLogs=0):
    res = Http.put(url + traderindex, headers=headers, data=json.dumps(datas))
    return res

#取消跟随
def deleteFollow(url, traderindex="", accountIndex="", headers="", datas="", interfaceName="", printLogs=0):
    res = Http.delete(url + traderindex + userData['accountIndex'] + accountIndex, headers=headers)
    return res

#获取交易员列表
def getTraders(url, headers="", params="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    return res

#获取排行榜交易员列表
def getRankTraders(url, headers="", params="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    return res


#获取跟随(正在/历史)
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

#获取跟随概要
def getFollowSummary(url,headers=""):
    res=requests.get(url,headers=headers)
    return res

#跟随多个交易员，组合跟随（需要登录）
def followMulti(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res


##########################  通用方法 #############################
#通过nickName获取用户的userID
#传入nickName即可
def getUserID(url=userData['hostName'] + followData['getTraders_url'], headers="", params={"category":"sam"}, interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    return json.loads(res.text)['data']['items'][0]['UserId']

#交易员通过nickName和accountIndex获取该跟随者的跟随订单
#传入nickName和accountIndex
def getFollowOrder(orderList, nickName="", accountIndex=""):
    # time.sleep(1)
    res = json.loads(orderList.text)["data"]["items"]
    # if res == []:
    #     raise "follow order not found."
    for js in res:
        if js['CustomerNickName'] == nickName and js['AccountCurrentIndex'] == int(accountIndex):
            return js