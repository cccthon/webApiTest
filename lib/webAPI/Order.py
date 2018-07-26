import sys,os,json,requests,yaml,time
sys.path.append("../../lib/common")
sys.path.append("../../lib/http")
import FMCommon,Http
from socketIO_client import SocketIO
from base64 import b64encode
from retrying import retry
orderData = FMCommon.loadOrderYML()
# 本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作

##########################################################################
###↓↓↓######################   订单管理   ########################↓↓↓###
##########################################################################

# 获取订单的跟随订单
# 接口名称：getFollowOrdersOfOrder
# 请求方法：get
# 请求url：/v2/trade/orders/398890/follow-orders    #398890为交易员订单id 
# 入参：
'''
id                number  跟随订单 ID
pageSize    可选  number  每页条目数量（默认：10）
pageIndex   可选  number  分页索引（默认：1）
pageField   可选  string  排序字段名称
pageSort    可选  string  排序形式（默认：DESC）DESC：倒序ASC：正序
orderStatus 可选  string  订单状态（默认：OPEN）OPEN：正在持仓CLOSE：已平仓
existOrder  1:预期有订单，   0 ：预期没有订单
'''
@retry(stop_max_attempt_number=10,wait_fixed=2000)
def getFollowOrdersOfOrder(url, headers="", params={}, tradeOrderID="", interfaceName="", printLogs=1,existOrder=1):
    # time.sleep(3) #等待跟随订单生成
    res = Http.get(url + tradeOrderID + orderData['getFollowOrdersOfOrder_url2'], headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    if existOrder == 1:
        if json.loads(res.text)["data"]["items"] == []:
            raise "follow Order not found."
    elif existOrder == 0:
        if json.loads(res.text)["data"]["items"] != []:
            raise "found follow Order."
    return res

# 获取当前用户的交易订单（需要登录）
# 接口名称：getOrders
# 请求方法：get
# 请求url：api/v2/trade/orders
# 入参：
'''
pageSize        可选  number  每页条目数量:按订单（默认：10）按交易员（默认：10000）按品种（默认：10000）
pageIndex       可选  number  分页索引（默认：1）
pageField       可选  string  排序字段名称（默认：OPEN_TIME）SYMBOL: 交易品种,STANDARDSYMBOL: 标准品种,STANDARDLOTS: 标准手,CMD: 交易类别,VOLUME: 手数,OPEN_TIME: 开仓时间,CLOSE_TIME: 平仓时间,SL: 止损,TP: 止盈,
                              OPEN_PRICE:开仓价格,CLOSE_PRICE: 平仓价格,PROFIT: 盈亏,SWAPS: 利息,COMMISSION: 手续费,ORDERCOUNT: 交易笔数,NETWORTH: 净仓,TICKET: 订单号,NICKNAME: 交易员
pageSort        可选  string  排序形式（默认：DESC）DESC：倒序,ASC：正序
orderStatus     可选  string  订单状态（默认：ALL）ALL：全部,OPEN：正在持仓,CLOSE：历史交易
orderType       可选  string  订单类型（默认：ALL）ALL：全部,BUYING：买入,SELLING：卖出
symbolType      可选  string  交易品种（例如：AUDUSD，如果筛选多个品种使用逗号分隔，默认 ALL 全部）
openTime        可选  string  开仓时间查询（格式：2017-05-03，默认：无）
openStartTime   可选  string  开仓时间查询起始时间（格式：2017-05-03，默认：无）
openEndTime     可选  string  开仓时间查询结束时间（格式：2017-05-03，默认：无）
closeTime       可选  string  平仓时间查询（格式：2017-05-03，默认：无）
closeStartTime  可选  string  平仓时间查询起始时间（格式：2017-05-03，默认：无）
closeEndTime    可选  string  平仓时间查询结束时间（格式：2017-05-03，默认：无）
view            可选  string  视图（默认：ORDER）ORDER：按订单,SYMBOL：按品种,TRADER：按交易员
accountIndex    可选  string  账号索引筛选（例如：76016_3，默认：无）获取跟随者跟随的指定交易员账号的订单，则此处为交易员账号索引,获取交易员的指定跟随者跟随自己的订单，则此处为跟随者账号索引
flag            可选  number  标记位（默认：0）0：旧接口,1：新接口
'''
def getOrders(url, headers="", params="", tradeOrderID="", interfaceName="", printLogs=1):
    time.sleep(7) #等待跟随订单生成
    res = Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    return res

#获取精选交易员列表（排行榜）
def getExcellentTraders(url, headers="", params="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    return res

#获取智能组合列表（排行榜）
def getCombinedTraders(url, headers="", params="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, params=params, interfaceName=interfaceName, logs=printLogs)
    return res


###↓↓↓######################   订单管理通用方法  ########################↓↓↓###
# 获取当前用户的交易订单的订单id列表，用于批量平仓
# 入参：订单信息
'''
orders
'''
def getOrdersID(orders):
    orderList = []
    for order in json.loads(orders.text)['data']['items']:
            orderList.append(order['TICKET'])
    return orderList