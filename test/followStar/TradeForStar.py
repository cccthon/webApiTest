import sys,unittest,json,requests,gc,redis,re,time

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import FMCommon,Account,Auth,Trade
from lib.tradeOnline import TradeOnline

userData = FMCommon.loadWebAPIYML()
userDataAccountUrl=FMCommon.loadAccountYML()
userDataAuthUrl=FMCommon.loadAuthYML()
userDataAuth=FMCommon.loadAuthYML()
userDataAccount=FMCommon.loadAccountYML()
userDataWebSocket = FMCommon.loadTradeOnlineYML()

class TradeForStar(object):
    @staticmethod
    def tradeForStar(self,myaccount,mypassword,myvolume):

        # 登录
        datas = {"account": myaccount, "password": mypassword,"remember": "false"}
        traderLoginRes = Auth.signin(userData['hostName'] + userDataAuth['signin_url'], userData['headers'], datas)
        token = json.loads(traderLoginRes.text)['data']['token']
        userData['headers'][userData['Authorization']] = userData['Bearer'] + token
        time.sleep(1)
        print('Account: '+myaccount)
        # 切换到交易员账户
        Account.switchAccount(userData['hostName'] + userDataAccount['switchAccount'],userData['headers'], '2')
        time.sleep(1)
        print('switchAccount ！！！' + userData['hostName'] + userDataAccount['switchAccount'])

        # 获取交易token
        getTokenRes = Trade.getToken(userData['hostName'] + userDataAccount["getToken_url"], userData['headers'])
        tradeToken = str(json.loads(getTokenRes.content)["data"]["Token"]).replace("=", "@")

        # 开仓
        openPositionRes=''
        openParam = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_210'],
                     userDataWebSocket['orderParam_symbol']: userDataWebSocket['broker_EURCAD'],
                     userDataWebSocket['orderParam_volume']: myvolume}

        openPositionRes = TradeOnline.OnlineTradeEvent.tradeEvent(self,userDataWebSocket['ws_host'],
                                                                  userDataWebSocket['ws_port'],
                                                                  {'token': "" + tradeToken}, openParam)

        #time.sleep(20)


        orderID = openPositionRes["order"]["order_id"]


        print('订单号： ' + str(orderID))


        # 平仓
        closeOrder = {userDataWebSocket['orderParam_code']: userDataWebSocket['ws_code_211'],
                      userDataWebSocket['orderParam_ticket']: orderID,
                      userDataWebSocket['orderParam_volume']: myvolume}
        closePositionRes=TradeOnline.OnlineTradeEvent.tradeEvent(self,userDataWebSocket['ws_host'],userDataWebSocket['ws_port'],
                                                {'token': "" + tradeToken}, closeOrder)

        #time.sleep(20)
        # print('xxxxxx',closePositionRes)
        return orderID
