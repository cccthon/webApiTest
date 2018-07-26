import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http,Account
import time

userData = FMCommon.loadWebAPIYML()

# 本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作

##########################################################################
###↓↓↓######################   鉴 权 模 块   ########################↓↓↓###
##########################################################################


def sendSMScode(url,headers='',datas='',interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas),interfaceName=interfaceName,
                    logs=printLogs)
    return res

#获取短信验证码
def getSMSCodeForRedis(userToken="",registerAccount=""):
    #获取redis
    redisRes = Account.getRedis(redisHost=userData['apiRedis_host'], port=userData['apiRedis_port'], db='2', password='myredis')
    print('redisRes: ',redisRes)
    #从redis读取短信验证码
    smsCode=json.loads(redisRes.get(('').join(userToken) +"."+registerAccount+ ".verifyInfo"))["smscode"]
    return smsCode

#输入账户不存在则注册,存在就直接登陆
def login(url,headers='',datas='',interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas),interfaceName=interfaceName,
                    logs=printLogs)
    return res

#根据不同的参数查询用户是否存在
def checkUserExist(url,headers='',datas='',interfaceName="", printLogs=0):
    res = Http.post(url, headers=headers, datas=json.dumps(datas),interfaceName=interfaceName,
                    logs=printLogs)
    return res

# 获取短信验证码
def getSMScode(url='',registerAccount='',userToken='',header=''):
    # z: 手机号码加密的结果, 请在url携带m=手机号码方便日志查询
    # y: 验证码ticket, 这个由客户端腾讯的验证码回调给出
    # x: (可选)国家编码（默认：0086，表示中国）
    # w: 客户端标识
    # u: 当前时间戳
    # t: (可选)要发送的短信类型，text: 文本，voice: 语音， 默认text
    # s: (可选)要执行的动作，signin表示登陆，register表示注册类，reset表示重置类

    u = time.time()
    text = registerAccount + '::websms::fmfetestteam::websms::' + str(u)
    z = FMCommon.des_ecrypt(ecryptText=text, desKey='12345678')
    datas = {"z": z, "y": "", "w": '12345678', "u": u}

    '''手机号加密发送短信验证码'''
    sendSMScodeRes = sendSMScode(url=url, headers=header, datas=datas, interfaceName='sendSMScode')

    '''获取短信验证码'''
    smsCode = getSMSCodeForRedis(userToken=str(userToken), registerAccount=registerAccount)
    return smsCode




