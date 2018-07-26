import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import Http
import FMCommon
from socketIO_client import SocketIO
from base64 import b64encode


#本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作


#封装交易员账号的跟随者列表接口
def getFollowersOfTrader(url,headers="",pageSize="10",pageIndex="1",pageField="PROFIT",pageSort="DESC",isFollowing="全部",
                         isReal="否",flag="0"):

     param = {"pageSize":pageSize,
              "pageIndex":pageIndex,
              "pageField":pageField,
              "pageSort":pageSort,
              "isFollowing":isFollowing,
              "isReal":isReal,"flag":flag}

     res=Http.get(url,headers=headers,params= json.dumps(param))
     return res

def getFollowsOfCustomer(url,headers="",pageSize="10",pageIndex="1",pageField="PROFIT",pageSort="DESC",isFollowing="全部",flag="0"):

     param = {"pageSize":pageSize, "pageIndex":pageIndex,"pageField":pageField, "pageSort":pageSort,"isFollowing":isFollowing,"flag":flag}

     res=Http.get(url,headers=headers,params= json.dumps(param))
     return res


#获取交易员账号的交易图表统计数据
def getGraphicsOfTrader(url,headers):
    res=Http.get(url,headers)
    return res

#获取交易员账号的交易图表统计数据
def getOrdersOfUserAccount(url,headers):
    res=Http.get(url,headers)
    return res

#获取交易员账号的交易统计数据
def getStatisticsOfTrader(url,headers, params="",interfaceName="", printLogs=0):
    res=Http.get(url,headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res

#获取跟随者账号的交易统计数据 
def getStatisticsOfCustomer(url,headers, params="",interfaceName="", printLogs=0):
    res=Http.get(url,headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res

#获取交易员账号的交易图表数据
def getGraphicsOfTrader(url,headers, params="",interfaceName="", printLogs=0):
    res=Http.get(url,headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res

#获取跟随者账号的交易图表数据 
def getGraphicsOfCustomer(url,headers, params="",interfaceName="", printLogs=0):
    res=Http.get(url,headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res

#获取用户的交易账号列表（个人展示页）
def getAccountsOfUser(url,headers, params="",interfaceName="", printLogs=0):
    res=Http.get(url,headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res

#获取某用户交易账号关注品种（个人展示页）
def getAttentionSymbols(url,headers):
    res=Http.get(url,headers)
    return res