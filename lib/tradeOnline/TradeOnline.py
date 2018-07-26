import sys
import os
import json
import yaml
import logging
from socketIO_client import SocketIO
from base64 import b64encode
sys.path.append("../../lib/common")
import FMCommon
from Timer import func_timer
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('webSockets')

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

class OnlineTradeEvent():
    @func_timer
    def tradeEvent(self, ws_host, ws_port, brokerToken, openParam, ws_EmitEvent=userData['ws_event_order'], ws_OnEvent=userData['ws_event_result'], waitTime=userData['ws_waitTime'], logs=0):
        def result_handler(*args):
            self.socketsEvent = json.loads(*args)
            print('SocketsResult: ',args)
            if 0 == logs:
                FMCommon.printLog("")
                FMCommon.printLog("---> 【OnlineTrade RequestParam】:")
                # logger.info("【OnlineTrade RequestParam】:")
                FMCommon.printLog(openParam)
                FMCommon.printLog("<--- 【OnlineTrade " + ws_EmitEvent + " Event】:")
                # logger.info("【OnlineTrade " + ws_EmitEvent + " Event】:")
                FMCommon.printLog(self.socketsEvent)
            io.disconnect()
        # 建立socket连接
        io = SocketIO(ws_host, ws_port, params=brokerToken)
        print('ws_host: ',ws_host)
        print('SocketIO: ',io)
        # 发起开仓请求
        io.emit(ws_EmitEvent, json.dumps(openParam))
        # 监听开仓result
        io.on(ws_OnEvent, result_handler)
        # 设置监听超时时间
        io.wait(seconds=waitTime)

        # web sockets平仓
        try:
            return self.socketsEvent
        except Exception as e:
            print(e)
            print("Error: OnlineTrade srv abnormal!!!! webSockets monitor order event fail.")
'''
class OnlineTradeEvent():
    def tradeEvent(self, ws_host, ws_port, brokerToken, openParam, ws_EmitEvent=userData['ws_event_order'], ws_OnEvent=userData['ws_event_result'], waitTime=userData['ws_waitTime'], logs=0):
        def result_handler(*args):
            # for tuple in args:
            #     self.res = json.loads(tuple)
            #     print(self.res)
            # if 0 == logs:
            #     FMCommon.printLog("---> 【OnlineTrade " + ws_EmitEvent + " Event】:")
            #     FMCommon.printLog(self.socketsEvent)
            # self.socketsEvent = []
            # print(args)
            for tuple in args:
                self.openPosition = json.loads(tuple)
                print(tuple)
                if json.loads(tuple)['rcmd'] == 224:
                    print("------224",tuple)
                    self.socketsEvent = json.loads(tuple)
                # elif json.loads(tuple)['rcmd'] == 223:
                #     print("------223",tuple)
                #     self.socketsEvent = json.loads(tuple)
                # elif json.loads(tuple)['rcmd'] == 210:
                #     print("------210",tuple)
                #     self.socketsEvent = json.loads(tuple)
                # elif json.loads(tuple)['rcmd'] == 211:
                #     print("------211",tuple)
                #     self.socketsEvent = json.loads(tuple)
                # else :
                #     print("webSockets monitor order event fail!!!")
            io.disconnect()
        # 建立socket连接
        io = SocketIO(ws_host, ws_port, params=brokerToken)
        # 发起开仓请求
        io.emit(ws_EmitEvent, json.dumps(openParam))
        # 监听开仓result
        io.on(ws_OnEvent, result_handler)
        # 设置监听超时时间
        io.wait(seconds=waitTime)
        # web sockets平仓
        return self.openPosition
'''
class OnlineTradeEvent_sl():
    @func_timer
    def tradeEvent_sl(self, ws_host, ws_port, brokerToken, ws_EmitEvent=userData['ws_event_sl'], ws_OnEvent=userData['ws_event_sl'], waitTime=userData['ws_waitTime'], logs=0):
        def result_handler(*args):
            self.socketsEvent = json.loads(json.dumps(*args))
            io.disconnect()
        # 建立socket连接
        io = SocketIO(ws_host, ws_port, params=brokerToken)
        # 发起开仓请求
        io.emit(ws_EmitEvent, '', result_handler)
        # 监听开仓result
        io.on(ws_OnEvent, result_handler)
        # 设置监听超时时间
        io.wait(seconds=waitTime)
        try:
            return self.socketsEvent
        except:
            print("Error: OnlineTrade srv abnormal!!!! webSockets monitor sl event fail.")
