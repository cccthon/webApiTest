import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http
from socketIO_client import SocketIO
from base64 import b64encode

# 本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作

##########################################################################
###↓↓↓######################   鉴 权 模 块   ########################↓↓↓###
##########################################################################

# 通过账号密码登入followme系统
# 接口名称：signin
# 请求方法：post
# 请求url：/api/v1/auth/signin
# 入参：
'''
account       string     tel or email
password      string     volume number
remember      boolean    remember me for auto signin
captcha 可选  string     verification code
oauth2  可选  boolean   是否是第三方登录
'''
# def signin(url,account, password, headers, remember = "false", captcha = '', oauth2 = "false"):
#     param = {"account":account, "password":password, "remember":remember}
#     res = requests.post(url, headers = headers, data = json.dumps(param))
#     FMCommon.printUrl("request url: " + url)
#     return res


def signin(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res
# def jydssignin(url, headers="", params="", interfaceName="", printLogs=0):
#     res = Http.post(url, headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
#     return res






# 通过token登出followme系统
# 接口名称：signout
# 请求方法：post
# 请求url：/api/v1/auth/signout
# 入参：url, token
# def signout(url, token=""):
#     res = requests.post(url, token)
#     FMCommon.printUrl("request url: " + url)
#     return res


def signout(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res


# 获取短信验证码
# 请求url：'域名/api/v1/auth/smscode'
# 请求方法： get

def getSMSScode(url, headers):
    res = requests.get(url, headers=headers)
    return res

# 获取图形的验证码
# 请求url：'域名/api/v1/auth/captcha'
# 请求方法： get


def getCaptcha(url, header=""):
    res = requests.get(url, header)
    return res

# 注册账号
# 请求url：'域名/api/v1/auth/register'
# 请求方法：post


def register(url, headers="", account="", password="", platform="", captcha="", smscode="", emailcode="", invite="", nickname="", oauth2=""):
    params = {"account": account,
              "password": password,
              "platform": platform,
              "captcha": captcha,
              "smscode": smscode,
              "emailcode": emailcode,
              "invite": invite,
              "nickname": nickname,
              "oauth2": oauth2
              }
    res = Http.post(url, headers=headers, datas=json.dumps(params))
    return res

#注销用户
#请求url：'域名/OAAccount/LogOut'
def logOut(url,headers="",userId="",interfaceName="", printLogs=0):
    params={"userId":userId}
    res=Http.get(url,headers=headers,interfaceName=interfaceName,logs=printLogs)
    return res

def loginOA(url,headers="",username="",password="",timeout=60, interfaceName="", printLogs=0):
    params={"username":username,
            "password":password}
    res=Http.post(url,headers=headers,datas=json.dumps(params),timeout=timeout, interfaceName=interfaceName, logs=printLogs)
    return res

def loginOut(url,headers="",userId=""):
    params={"userId":userId}
    res=Http.post(url,headers=headers,datas=json.dumps(params))
    return res

def closeAccount(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

def getUserToken(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

