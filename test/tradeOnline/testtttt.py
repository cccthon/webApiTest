import sys,unittest,json
sys.path.append("../../lib/common")
sys.path.append("../../lib/tradeOnline")
import FMCommon,TradeOnline
from socketIO_client import SocketIO
from base64 import b64encode

userData = FMCommon.loadTradeOnlineYML()

class openAndClosePosition(unittest.TestCase):
    def setUp(self):
        pass

    def test_openAndClosePosition(self):
        # def result_handler(*args):
        #     for tuple in args:
        #         # print(json.loads(tuple))
        #         openPositionRes = json.loads(tuple)
        #         #打印response对象。
        #         FMCommon.printLog(openPositionRes)
        #         #校验code等于0，为及时单开仓成功
        #         self.assertEqual(openPositionRes["code"], userData['ws_code_0'])
        #         #校验rcmd等于210，为及时单开仓
        #         self.assertEqual(openPositionRes["rcmd"], userData['ws_code_210'])
        #         #校验手数为下单时的手数
        #         self.assertEqual(openPositionRes["order"]["volume"], 300)
        #         #校验品种为下单时的经纪商品种
        #         self.assertEqual(openPositionRes["order"]["symbol"], userData['broker_EURCAD'])
        #         #保存orderID,待开仓使用
        #         self.orderID = openPositionRes["order"]["order_id"]
        #         #收到要求的响应事件后断开socket链接
        #         io.disconnect()
        # #建立socket连接
        # io = SocketIO(userData['ws_host'], userData['ws_port'], params = userData['brokerToken'])
        # #发起开仓请求
        # openParam = json.dumps({ userData['orderParam_code']: userData['ws_code_210'], userData['orderParam_symbol']: userData['broker_EURCAD'], userData['orderParam_volume']: 300 })
        # io.emit(userData['ws_event_order'], openParam)
        # #监听开仓result
        # io.on(userData['ws_event_result'], result_handler)
        # #设置监听超时时间
        # io.wait(seconds = 5)

        # #再下一单
        # def result_handler(*args):
        #     for tuple in args:
        #         # print(json.loads(tuple))
        #         openPositionRes = json.loads(tuple)
        #         #打印response对象。
        #         FMCommon.printLog(openPositionRes)
        #         #校验code等于0，为及时单开仓成功
        #         self.assertEqual(openPositionRes["code"], userData['ws_code_0'])
        #         #校验rcmd等于210，为及时单开仓
        #         self.assertEqual(openPositionRes["rcmd"], userData['ws_code_210'])
        #         #校验手数为下单时的手数
        #         self.assertEqual(openPositionRes["order"]["volume"], 300)
        #         #校验品种为下单时的经纪商品种
        #         self.assertEqual(openPositionRes["order"]["symbol"], userData['broker_EURCAD'])
        #         #保存orderID,待开仓使用
        #         self.orderID = openPositionRes["order"]["order_id"]
        #         #收到要求的响应事件后断开socket链接
        #         io.disconnect()
        # #建立socket连接
        # io = SocketIO(userData['ws_host'], userData['ws_port'], params = userData['brokerToken'])
        # #发起开仓请求
        # openParam = json.dumps({ userData['orderParam_code']: userData['ws_code_210'], userData['orderParam_symbol']: userData['broker_EURCAD'], userData['orderParam_volume']: 300 })
        # io.emit(userData['ws_event_order'], openParam)
        # #监听开仓result
        # io.on(userData['ws_event_result'], result_handler)
        # #设置监听超时时间
        # io.wait(seconds = 5)

        print("----------------------------批量平仓--------------------")
        #web sockets部分平仓
        def result_handler1(*args):
            # print(args)
            for tuple in args:
                if json.loads(tuple)['rcmd'] == 224:
                    print(tuple)
                    #保存orderID,待开仓使用
                    self.orderID224 = json.loads(tuple)["order"]["order_id"]
                    print("self.orderID224: ",self.orderID224)
                elif json.loads(tuple)['rcmd'] == 223:
                    print(tuple)
                elif json.loads(tuple)['rcmd'] == 219:
                    print(tuple)
                elif json.loads(tuple)['rcmd'] == 222:
                    print(tuple)
                else :
                    print("webSockets monitor order event fail!!!")
        #建立socket连接
        io = SocketIO(userData['ws_host'], userData['ws_port'], params = userData['brokerToken'])
        #发起平仓请求
        io.emit('order', json.dumps({ 'code': 219, 'tickets': [21875,21870] }))
        io.on('result',  result_handler1)
        io.wait(seconds = 3)


        # print("----------------------------部分平仓--------------------")
        #web sockets部分平仓
        # def result_handler1(*args):
        #     # print(args)
        #     for tuple in args:
        #         if json.loads(tuple)['rcmd'] == 224:
        #             print(tuple)
        #             #保存orderID,待开仓使用
        #             self.orderID224 = json.loads(tuple)["order"]["order_id"]
        #             print("self.orderID224: ",self.orderID224)
        #         elif json.loads(tuple)['rcmd'] == 223:
        #             print(tuple)
        #         elif json.loads(tuple)['rcmd'] == 211:
        #             print(tuple)
        #         else :
        #             print("webSockets monitor order event fail!!!")
        # #建立socket连接
        # io = SocketIO(userData['ws_host'], userData['ws_port'], params = userData['brokerToken'])
        # #发起平仓请求
        # io.emit('order', json.dumps({ userData['orderParam_code']: userData['ws_code_211'], userData['orderParam_ticket']: 21872, userData['orderParam_volume']: 300 }))
        # io.on('result',  result_handler1)
        # io.wait(seconds = 5)


        # print("----------------------------平掉剩余--------------------")
        # #web sockets平仓剩余部分
        # def result_handler1(*args):
        #     for tuple in args:
        #         print(json.loads(tuple))
        # #建立socket连接
        # io = SocketIO(userData['ws_host'], userData['ws_port'], params = userData['brokerToken'])
        # #发起平仓请求
        # io.emit('order', json.dumps({ userData['orderParam_code']: userData['ws_code_211'], userData['orderParam_ticket']: self.orderID224, userData['orderParam_volume']: 200 }))
        # io.on('result',  result_handler1)
        # io.wait(seconds = 5)


    def tearDown(self):
        #清空测试环境，还原测试数据
        #将测试订单平掉。平仓
        #登出followme系统
        pass

if __name__ == '__main__':
    unittest.main()
