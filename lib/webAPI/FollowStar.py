import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http
from socketIO_client import SocketIO
from base64 import b64encode

# 本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作

##########################################################################
###↓↓↓##################   followStar 模 块   ######################↓↓↓###
##########################################################################

def loginFStar(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

# def GetMyTradeInfo(url, headers="", interfaceName="", printLogs=0):
#     res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
#     return res

# 首页--个人信息
# 我的交易
# 我的团队
def GetMemberInfo(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

def GetTeamInfoPage(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

def GetTeamInfoStatistics(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

def GetTeamPersonInfoPage(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

def GetTeamPersonStatistics(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

def GetTeamTradePage(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

def GetTeamTradeStatistics(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

# def GetUpgradeInfo(url, headers="", interfaceName="", printLogs=0):
#     res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
#     return res

# 是否升级
def TakeUserUpgradeTip(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

def GetUserInfo(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

def FollowStarLogout(url, headers="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

# 根据关键字搜索昵称,只显示五条
def SearchNickNameWithKey(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

# 我的服务费-获取银行卡信息
def getPayment(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

# 我的服务费-绑定/更新银行卡
def CreateNewOrUpdatePayment(url, headers="",datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas),interfaceName=interfaceName, logs=printLogs)
    return res

# 我的服务费-服务费明细
def GetCommissionLogPage(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

# 我的服务费-数据总览
def GetMyCommissionSummary(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

# 我的服务费-提取服务费
def ApplyingCommissionWithdraw(url, headers="",datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas),interfaceName=interfaceName, logs=printLogs)
    return res

# 我的服务费-服务费提取记录
def GetCommissionWithdrawRecord(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
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

# OA服务费审核--获取数据列表
# def GetCommissionList(url, headers="", params="",interfaceName="", printLogs=1):
#     res = Http.post(url, headers=headers,params=params,interfaceName=interfaceName,logs=printLogs)
#     return res

def GetCommissionList(url,headers="",datas="",timeout=60,interfaceName="", printLogs=0):
    res= Http.post(url,headers=headers,datas=json.dumps(datas),timeout=timeout,interfaceName=interfaceName,logs=printLogs)
    return res


# OA服务费审核--审核通过和审核失败
def AuditingCommission(url, headers="",datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas),interfaceName=interfaceName, logs=printLogs)
    return res

# OA服务费审核--已打款和打款失败
def AuditingCommissionPayMoney(url, headers="",datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas),interfaceName=interfaceName, logs=printLogs)
    return res