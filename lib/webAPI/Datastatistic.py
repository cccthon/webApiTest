import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http
from socketIO_client import SocketIO
from base64 import b64encode

userData = FMCommon.loadWebAPIYML()



#获取收益率图表数据(个人展示页) 
def getAccountRoi(url, headers="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,interfaceName=interfaceName, logs=printLogs)
    return res

#获取净值余额图表数据(个人展示页) 
def getDayAccountBalanceAndEquityList(url, headers="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,interfaceName=interfaceName, logs=printLogs)
    return res

#获取收益图表数据(个人展示页) 
def getDayAccountMoneyAndEquityList(url, headers="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,interfaceName=interfaceName, logs=printLogs)
    return res

#获取跟随收益图表数据(个人展示页) 
def getFollowerFollowTraderList(url, headers="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,interfaceName=interfaceName, logs=printLogs)
    return res

#获取月分析报告图表数据(个人展示页) 
def getMonthAnalysisReport(url, headers="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,interfaceName=interfaceName, logs=printLogs)
    return res


#获取品种分析图表接口数据(个人展示页) 
def getSymbolAnalysis(url, headers="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,interfaceName=interfaceName, logs=printLogs)
    return res

#盈亏分析图表接口数据(个人展示页)
def getProfitAndLossAnalysis(url, headers="",params="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,params=params,interfaceName=interfaceName, logs=printLogs)
    return res



##########################  通用方法 #############################
#通过nickName获取用户的userID
#传入nickName即可
def getUserID(url="", headers="", params="", interfaceName="", printLogs=1):
    res = Http.get(userData['hostName'] + userData['getTraders_url'], headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    return json.loads(res.text)['data']['items'][0]['UserId']

