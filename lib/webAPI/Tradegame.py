import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http
from socketIO_client import SocketIO
from base64 import b64encode

userData = FMCommon.loadWebAPIYML()
userDataAccount=FMCommon.loadAccountYML()

#本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作



# 获取当前用户的账号列表（个人中心）（需要登录） 
# 请求url：jyds/api/get_accounts

def get_Accounts(url, headers="", params="",interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers,params=params,interfaceName=interfaceName,logs=printLogs)
    return res

#交易大赛登录
def jydssignin(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res


#交易大赛报名成功
def sign_up(url, headers="", datas="", interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res
