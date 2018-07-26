import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http,Auth,re,redis
from socketIO_client import SocketIO
from base64 import b64encode

userData = FMCommon.loadWebAPIYML()
userDataAccount=FMCommon.loadAccountYML()

#本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作

#切换账号
def switchAccount(url,headers,index="", printLogs=0):
    res=Http.get(url+index+userDataAccount['switch'],headers=headers,logs=printLogs)
    return res

#设置昵称
def setUserNickname(url, headers="", datas="",interfaceName="", printLogs=0):
    res=Http.put(url,headers=headers,datas=json.dumps(datas),interfaceName=interfaceName,logs=printLogs)
    return res

#获取当前用户的当前切换至的交易账号（需要登录）
def getAccount(url,headers=""):
	res=Http.get(url,headers=headers)
	return res

# 获取在线交易 Token
# 接口名称：getToken
# 请求方法：get
# 请求url：api/v2/trade/token
# 入参：headers
def getToken(headers="", onlyTokn="false", interfaceName="", printLogs=0):
    res = Http.get(userData['hostName'] + userDataAccount['getToken_url'], headers=headers, params='', interfaceName=interfaceName, logs=printLogs)
    if onlyTokn == "true":
        return str(json.loads(res.content)["data"]["Token"]).replace("=", "@")
    return res

# 获取对应经纪商账号的accountIndex
# 请求url：api/v2/trade/account
# 入参：brokenID, 默认模拟账号的索引
# accountType:账户类型。默认：1 fm账户  3 mam  ,0 demo, 2 sam
# UserType:默认跟随者 交易员 1 ， 跟随者 2
def getSpecialAccountIndex(headers="", brokerID=3, accountType=1,interfaceName="getAccounts", printLogs=1):
    res = Http.get(userData['hostName'] + userDataAccount['getAccounts_url'] + userDataAccount['getAccounts_url2'], headers=headers,interfaceName=interfaceName,logs=printLogs)
    resList = []
    for tuple in json.loads(res.text)['data']['accounts']:
        if tuple['BrokerId'] == brokerID and tuple['AccountType'] == accountType:
            resList.append(str(tuple['AccountIndex']))
    return resList
     

# 获取对应经纪商的mt4账号
# 请求url：api/v2/trade/account
# 入参：brokenID, 默认模拟账号的索引
def getSpecialmt4Account(headers="", brokerID = "3", interfaceName="getmt4Account", printLogs=1):
    res = Http.get(userData['hostName'] + userDataAccount['getAccounts_url'] + userDataAccount['getAccounts_url2'], headers=headers,interfaceName=interfaceName,logs=printLogs)
    for tuple in json.loads(res.text)['data']['accounts']:
            if tuple['BrokerId'] == brokerID:
                return str(tuple['MT4Account'])


# 获取用户信息
# 请求url：api/v2/trade/account/users/:id
# 入参：brokenID, 默认模拟账号的索引
def getUserInfo(url, headers="", params="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res


# 获取经纪商列表
# 请求url：api/v2/trade/brokers

def getBrokers(url, headers="", params="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res

# 获取当前用户的账号列表（个人中心）（需要登录）
# 请求url：api/v2/trade/accounts

def getAccounts(url, headers="", params="",interfaceName="", printLogs=1):
    res = Http.get(url, headers=headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res

def updateUserInfo(url,headers="",datas="",interfaceName="", printLogs=0):
    res=Http.post(url,headers=headers,datas=json.dumps(datas),interfaceName=interfaceName,logs=printLogs)
    return res
################################ OA #######################################

#获取账户总览列表
#请求url： /Account/GetUserAccountSummaryReport
def getUserAccountSummaryReport(url,headers="",datas="",timeout=60,interfaceName="", printLogs=0):
    res= Http.post(url,headers=headers,datas=json.dumps(datas),timeout=timeout,interfaceName=interfaceName,logs=printLogs)
    return res


################################ 公共方法 #######################################
#根据图形验证码获取未登录token
def getTokenForCaptcha(url):
    captchaRes=Auth.getCaptcha(url,userData['headers'])
    userToken = ('').join(re.findall(r"USER_TOKEN=(.+); Max-Age", captchaRes.headers["Set-Cookie"])).replace("'","")
    # userToken = ('').join(re.findall(r"USER_TOKEN=(.+); Max-Age", cookie)).replace("'","")
    return userToken

#读取redis
def getRedis(redisHost="",port="",db="",password=""):
    # redisRes = redis.Redis(host=userData['apiRedis_host'], port=56368, db=2, password='myredis')
    redisRes = redis.Redis(host=redisHost, port=port, db=db, password=password)
    return redisRes

#获取图形验证码
def getCaptchaForRedis(userToken=""):
    header={'content-type': 'application/json', 'Authorization': 'Bearer ' + str(userToken)}
    #获取redis
    redisRes = getRedis(redisHost=userData['apiRedis_host'], port=userData['apiRedis_port'], db='2', password='myredis')
    #获取验证码
    ccap = ('').join(re.findall(r"b(.+)", str(redisRes.get(('').join(userToken) + ".ccap")))).replace("'","")
    return ccap

#获取短信验证码
def getSMSCodeForRedis(url,userToken="",headers="",registerAccount=""):
    #根据图形验证码获取短信验证码
    smsCodeRes = Auth.getSMSScode(url, headers=headers)
    #获取redis
    redisRes = getRedis(redisHost=userData['apiRedis_host'], port=userData['apiRedis_port'], db='2', password='myredis')

    #从redis读取短信验证码
    smsCode=json.loads(redisRes.get(('').join(userToken) +"."+registerAccount+ ".verifyInfo"))["smscode"]

    return smsCode

