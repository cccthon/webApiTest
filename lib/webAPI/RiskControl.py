import sys,os,json,requests,yaml,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http
from socketIO_client import SocketIO
from base64 import b64encode

userData = FMCommon.loadWebAPIYML()
riskcontrolData = FMCommon.loadRiskControlYML()
# 本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作

##########################################################################
###↓↓↓######################   风 控 模 块   #######################↓↓↓###
##########################################################################
# 获取风控设置
# 接口名称：getRiskControl
# 请求方法：get
# 请求url：/api/v2/trade/riskcontrol
# 入参：url, headers, accountIndex  (#accountIndex 可选 number  跟随者账号的账号索引（如：1，默认当前切换到的跟随者账号）)
def getRiskControl(url, headers="", params="", accountIndex="", interfaceName="", printLogs=0):
    res = Http.get(url + userData['accountIndex'] + accountIndex, headers=headers,
                   params=params, interfaceName=interfaceName, logs=printLogs)
    return res

# 修改跟随者风控全局设置
# 接口名称：setRiskControl
# 请求方法：put
# 请求url：/api/v2/trade/riskcontrol
# 入参：url, headers, accountIndex (#accountIndex 可选 number
# 跟随者账号的账号索引（如：1，默认当前切换到的跟随者账号）)
def setRiskControl(url, headers, accountIndex="", datas="", interfaceName="", printLogs=0):
    res = Http.put(url + userData['accountIndex'] + accountIndex, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

# 修改跟随者针对指定交易员的风控设置
# 接口名称：setRiskControlForTrader
# 请求方法：put
# 请求url：/api/v2/trade/riskcontrol
# 入参：
'''
trader_index              string  交易员 ID 加索引（例如：90063_2）
accountIndex        可选  number  跟随者账号的账号索引（如：1，默认当前切换到的跟随者账号）
maxPositionLots     可选  number  最大持仓总手数（默认：0，表示无限制）
maxPositionOrders   可选  number  最大持仓总订单数（必须是整数，默认：0，表示无限制）
stopFollowPeriods   可选  array   停止跟随时间（默认：[]，表示不设置）
'''
def setRiskControlForTrader(url, headers, datas="", interfaceName="", printLogs=0):
    res = Http.put(url, headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res

# 修改跟随者针对指定交易员的风控品种设置
# 接口名称：setRiskControlForTraderSymbols
# 请求方法：put
# 请求url：api/v2/trade/riskcontrols/:trader_index/symbols
# 入参：
'''
trader_index              string  交易员 ID 加索引（例如：90063_2）
accountIndex        可选  number  跟随者账号的账号索引（如：1，默认当前切换到的跟随者账号）
symbolList          可选  array   品种列表（默认：[]，表示不设置）{
            Symbol:            #品种
            FollowType:        #交易类型：全部1；仅买；仅卖；不跟随
            StrategyType:      #跟随策略：固定；按比列
            Direction:         #跟随方向：正向；反向
            FollowSize:        #跟随数量
            SLPips:            #止损          
            TPPips:            #止盈
            Locked:            #锁定 }
'''
def setRiskControlForTraderSymbols(url, headers, datas="", interfaceName="", printLogs=0):
    res = Http.put(url + riskcontrolData['setRiskControlForTraderSymbols_url2'], headers=headers, datas=json.dumps(datas), interfaceName=interfaceName, logs=printLogs)
    return res


