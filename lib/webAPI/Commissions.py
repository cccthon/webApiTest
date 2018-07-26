import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http,Auth,re,redis
from socketIO_client import SocketIO
from base64 import b64encode

userData = FMCommon.loadWebAPIYML()
userDataCommissions=FMCommon.loadCommissionsYML()

#本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作

# 获取交易员的跟随服务费核算列表（需要登录）
# 请求url：api/v2/trade/commissions
def getCommissions(url, headers="", params="",interfaceName="", printLogs=1):
    res = Http.get(url, headers=headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res


# 服务费申请（需要登录）
# 请求url：api/v2/trade/commission-apply
def applyCommission(url, headers="", interfaceName="",datas = "", printLogs=0):
    res = Http.post(url, headers=headers, interfaceName=interfaceName, datas = json.dumps(datas), logs=printLogs)
    return res

# 获取服务费申请记录（需要登录） 
# 请求url：api/v2/trade/commission-apply-histories
def getCommissionApplyHistories(url, headers="", params="",interfaceName="", printLogs=1):
    res = Http.get(url, headers=headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res

# 获取OA跟随服务费列表明细（需要登录）
# 请求url：Trader/GetTraderCommissionApplyList
def getTraderCommissionApplyList(url,headers="",datas="",timeout=60,interfaceName="", printLogs=0):
    res= Http.post(url,headers=headers,datas=json.dumps(datas),timeout=timeout,interfaceName=interfaceName,logs=printLogs)
    return res

# 获取OA审核服务费金额（需要登录）
# 请求url：Trader/CalcFee
def getCalcFee(url, headers="", params="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res

# OA审核跟随服务费（需要登录）
# 请求url：Trader/CommApplySubmit
def commApplySubmit(url,headers="",datas="",timeout=60,interfaceName="", printLogs=0):
    res= Http.post(url,headers=headers,datas=json.dumps(datas),timeout=timeout,interfaceName=interfaceName,logs=printLogs)
    return res

# OA设置汇率（需要登录）
# 请求url：Trader/AddExchangeRate
def addExchangeRate(url,headers="",datas="",timeout=60,interfaceName="", printLogs=0):
    res= Http.post(url,headers=headers,datas=json.dumps(datas),timeout=timeout,interfaceName=interfaceName,logs=printLogs)
    return res

# OA获得汇率（需要登录）
# 请求url：Trader/GetTodayExchangeRate
def getTodayExchangeRate(url, headers="", params="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res

# OA支付跟随服务费（需要登录）
# 请求url：Trader/CommApplySubmit
def commPlaymoneyApplySubmit(url,headers="",datas="",timeout=60,interfaceName="", printLogs=0):
    res= Http.post(url,headers=headers,datas=json.dumps(datas),timeout=timeout,interfaceName=interfaceName,logs=printLogs)
    return res

# 获取交易员的跟随服务费概览（需要登录）  
# 请求url：api/v2/trade/commission-summary
def getCommissionSummary(url, headers="", params="",interfaceName="", printLogs=1):
    res = Http.get(url, headers=headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res








