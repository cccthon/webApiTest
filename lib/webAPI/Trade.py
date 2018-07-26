import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
import FMCommon,Http
from socketIO_client import SocketIO
from base64 import b64encode

userData = FMCommon.loadWebAPIYML()

#新建跟随
def getToken(url,headers):
    res=Http.get(url,headers=headers)
    return res

#查询订单
def getOrders(url,headers,orderStatus="",orderType="",symbolType="",openStartTime="",openEndTime="",closeStartTime="",closeEndTime=""):
    params={
        "orderStatus": orderStatus,
        "orderType": orderType,
        "symbolType": symbolType,
        "openStartTime": openStartTime,
        "openEndTime": openEndTime,
        "closeStartTime": closeStartTime,
        "closeEndTime": closeEndTime
    }
    res=Http.get(url, headers=headers,params=json.dumps(params),logs = 1)
    return res


#获取品种
def getAllSymbols(url,headers,full=""):
    res=Http.get(url+userData['wgetAllSymbolparam']+full,headers=headers)
    return res

#获取跟随者列表
def getCustomers(url, headers="", params="", interfaceName="", printLogs=1):
    res = Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    return res

#获取当前用户的账户资产
def getProperty(url, headers="", params="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    return res








