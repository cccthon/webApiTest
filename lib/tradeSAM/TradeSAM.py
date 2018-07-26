import sys
import os
import json
import yaml,grpc
import threading,time,unittest
from socketIO_client import SocketIO
from base64 import b64encode
sys.path.append("../../lib/common")
sys.path.append("../../lib/proto")
import FMCommon
from Timer import func_timer
from mt4api import mt4api_pb2
from mt4api import mt4api_pb2_grpc
from tradesignal import tradesignal_pb2
from tradesignal import tradesignal_pb2_grpc

userData = FMCommon.loadTradeOnlineYML()
##########################################################################
###↓↓↓######################   web sockets   #############################↓↓↓###
##########################################################################
# 本文件为二次封装web api接口。如果一个web接口被2个以上测试脚本调用，建议封装。减少后期接口变动维护工作

# onlineTrade服务的交易事件
# 入参：
'''
ws_host： web sockets服务地址
ws_port： web sockets服务端口
brokerToken： 经纪商token
openParam：为哈希表。ws_code决定是开仓还是平仓。{ userData['orderParam_code']: userData['ws_code_210'], userData['orderParam_symbol']: userData['broker_EURCAD'], userData['orderParam_volume']: 100 }
ws_EmitEvent：目前为交易事件（是否支持报价推送和品种列表待确认）
ws_OnEvent：  trade事件监听结果
waitTime：  web sockets链接持续的时间
'''

class varList():
    positionReply = ''
    apiSignal = ''

class TradeSAMStream():
    #获取订单信息
    def subscribeMT4API(stub='',tradeID=''):
        for times in range(1):
            for i in stub.SubscribeMT4API(mt4api_pb2.Empty()):
                for j in i.Trades:
                    # if j.TradeID == tradeID:
                    return j
    # 开仓
    # @func_timer
    def OpenPosition(stub='', account='',brokerID=5, symbol='', cmd=0, lots=0.1, waitTime = 4):
        print("stub:",stub)
        def samTrade():
            num = 1
            while num > 0:
                print("request id::", 10000+num)
                signal = tradesignal_pb2.TradeSignal(Account=account,BrokerID=brokerID,Symbol=symbol,Cmd=cmd,Lots=lots)
                res = mt4api_pb2.PositionRequest(Signal=signal,RequestID=10000 + num)
                yield res
                print("---> 【position request】:\n", res)
                time.sleep(1)
                num = num - 1
            time.sleep(waitTime)


        positionRequest_stream = stub.OpenPosition(samTrade())

        def read_PositionReply():
            num = 1
            while num >0:
                num -= 1
                varList.positionReply = next(positionRequest_stream)

        positionThread = threading.Thread(target=read_PositionReply)
        time.sleep(1)
        positionThread.start()
        time.sleep(waitTime)
        try:
            print("<--- 【position response】:", varList.positionReply)
            return varList.positionReply
        except:
            print("Error.....")

    # 平仓
    # @func_timer
    def ClosePosition(stub='', account='', brokerID=5, tradeID='', lots=0.1, waitTime=4):
        # tradeID传int类型
        def samTrade():
            num = 1
            while num > 0:
                print("request id::", 10000 + num)
                signal = tradesignal_pb2.TradeSignal(Account=account, BrokerID=brokerID, Lots=lots, TradeID=tradeID)
                res = mt4api_pb2.PositionRequest(Signal=signal, RequestID=10000 + num)
                yield res
                print("---> closePosition request】:\n", res)
                num = num - 1
                time.sleep(1)
            time.sleep(waitTime)

        input_stream = stub.ClosePosition(samTrade())
        def read_incoming():
            num = 1
            while num >0:
                num -= 1
                varList.readRes = next(input_stream)

        thread = threading.Thread(target=read_incoming)
        thread.start()
        time.sleep(waitTime)
        try:
            print("<--- 【closePosition response】:", varList.readRes)
            return varList.readRes
        except:
            print("Error.....")


if __name__ == '__main__':
    '''测试Sam经纪商开仓,平仓,历史订单'''
    backTestingChannel = grpc.insecure_channel('10.1.0.8' + ':' + str(36217))
    stub = mt4api_pb2_grpc.MT4APISrvStub(backTestingChannel)
    account='500383690'
    brokerID=106
    symbol='AUDCAD'
    cmd=1
    lots=0.1

    res = TradeSAMStream.OpenPosition(stub=stub,account=account,brokerID=brokerID,symbol=symbol,cmd=cmd,lots=lots)
    print(res)

    res1 = TradeSAMStream.subscribeMT4API(stub=stub,tradeID = res.Signal.TradeID)
    print(res1)