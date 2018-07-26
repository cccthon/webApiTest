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

#获取所有产品列表
def getAllProducts(url, headers="", params="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    return res

#发布产品（需要登录） 
def createProduct(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

#OA审核产品通过/驳回
def ProductProposeAction(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas),interfaceName=interfaceName,logs=printLogs)
    return res

#OA产品申请审核记录分页查询
def GetPageProductPropose(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas),interfaceName=interfaceName,logs=printLogs)
    return res

#申请提前结束产品前查看产品状态的，是否还有持仓单
def GetProductStatus(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url,headers=headers, interfaceName=interfaceName,logs=printLogs)
    return res

#参与产品
def JoinProduct(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas),interfaceName=interfaceName,logs=printLogs)
    return res

#获取产品信息
def GetProduct(url, headers="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,interfaceName=interfaceName,logs=printLogs)
    return res

#申请提前结束产品
def EndProduct(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

#获取短信验证码（申请提前结束产品）
def endProductSMSCode(url, headers="", datas="", interfaceName="", printLogs=0):
    res =  Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

#校验短信验证码
def endProductSMSCodeVerify(url, headers="", datas="", interfaceName="", printLogs=0):
    res =  Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

#获取产品的订单列表
def getProductOrders(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res

#OA修改产品开始时间
def updatePendingProduct(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

#OA结束产品
def productEndOA(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

