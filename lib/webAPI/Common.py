import sys,os,json,requests,yaml
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http
from socketIO_client import SocketIO
from base64 import b64encode

# 本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作

##########################################################################
###↓↓↓######################   公 共 模 块   #######################↓↓↓###
##########################################################################

# 获取首页的热门交易员信息
# 接口名称：getHomeHotTrader
# 请求方法：get
# 请求url：api/v1/common/home/hot-trader
def getHomeHotTrader(url, headers="", params="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, params=json.dumps(params), interfaceName=interfaceName, logs=printLogs)
    return res

# 获取首页明星交易员信息
# 接口名称：getHomeStarTrader
# 请求方法：get
# 请求url：api/v1/common/home/star-trader
def getHomeStarTrader(url, headers="", params="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, params=json.dumps(params), interfaceName=interfaceName, logs=printLogs)
    return res

# 获取首页跟随者收益信息
# 接口名称：getHomeFollower
# 请求方法：get
# 请求url：api/v1/common/home/follower-profit
def getHomeFollower(url, headers="", params="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, params=json.dumps(params), interfaceName=interfaceName, logs=printLogs)
    return res

# 获取首页交易动态信息
# 接口名称：getHomeTradeDynamic
# 请求方法：get
# 请求url：api/v1/common/home/trade-dynamic
def getHomeTradeDynamic(url, headers="", params="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, params=json.dumps(params), interfaceName=interfaceName, logs=printLogs)
    return res