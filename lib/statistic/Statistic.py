import sys
import os
import json
import yaml
import datetime,time
from socketIO_client import SocketIO
from base64 import b64encode
sys.path.append("../../lib/common")
import FMCommon
from pyhive import presto 
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dateutil.parser import parse

webAPIData = FMCommon.loadWebAPIYML()
tradeScoreData = FMCommon.loadTradeScoreYML()
statisticConf = FMCommon.loadStatisticYML()

#######################################################
##presto 数据库表结构
class t_mt4trades(declarative_base()):
    # 表的名字:
    __tablename__ = 't_mt4trades'
    # 表的结构:
    Id = Column(INT, primary_key=True)
    ticket = Column(INT())
    login = Column(String(64))
    brokerid = Column(INT)
    symbol = Column(String(64))
    # DIGITS = Column(INT)
    cmd = Column(INT)
    volume = Column(INT)
    open_time = Column(String(64))
    open_price = Column(Float(53))
    # point = Column(Float(53))
    # SL = Column(Float(53))
    # TP = Column(Float(53))
    close_time = Column(String(64))
    # EXPIRATION = Column(String(64))
    # REASON = Column(INT)
    # CONV_RATE1 = Column(Float(53))
    # CONV_RATE2 = Column(Float(53))
    commission = Column(Float(53))
    # COMMISSION_AGENT = Column(Float(53))
    swaps = Column(Float(53))
    close_price = Column(Float(53))
    profit = Column(Float(53))
    # TAXES = Column(Float(53))
    comment = Column(String(256))
    # INTERNAL_ID = Column(INT)
    # MARGIN_RATE = Column(Float(53))
    # TIMESTAMP = Column(INT)
    modify_time = Column(String(64))
    # ManagerAccount = Column(String(64))
    # TPOrderID = Column(INT)
    # SLOrderID = Column(INT)
    # extraderid = Column(INT)
    # CommissionStatus = Column(INT)
    standardsymbol = Column(String(100))
    standardlots = Column(Float(53))
    pips = Column(Float(53),nullable=True)

class t_followorders(declarative_base()):
    # 表的名字:
    __tablename__ = 't_followorders'
    # 表的结构:
    Id = Column(INT, primary_key=True)
    masteraccount = Column(String(64))       
    masterbrokerid = Column(INT())      
    masterorderid = Column(INT())      
    followaccount = Column(String(64))         
    followbrokerid = Column(INT())        
    followorderid = Column(INT())         
    status = Column(INT())                
    closetime = Column(String)

class T_followreport(declarative_base()):
    # 表的名字:
    __tablename__ = 'T_FollowReport'
    # 表的结构:
    masteraccount = Column(String(64),primary_key = True)       
    masterbrokerid = Column(INT())           
    followaccount = Column(String(64))         
    followbrokerid = Column(INT())               
    startdate = Column(String)                
    enddate = Column(String)

class TD_followorders(declarative_base()):
    # 表的名字:
    __tablename__ = 'TD_FollowOrders'
    # 表的结构:
    Id = Column(INT, primary_key=True)
    masteraccount = Column(String(64))       
    masterbrokerid = Column(INT())      
    masterorderid = Column(INT())      
    followaccount = Column(String(64))         
    followbrokerid = Column(INT())        
    followorderid = Column(INT())         
    status = Column(INT())                
    closetime = Column(String)

class t_mt4tradesinfo(declarative_base()):
    # 表的名字:
    __tablename__ = 't_mt4tradesInfo'
    # 表的结构:
    Id = Column(INT, primary_key=True)
    ticket = Column(INT())            
    login = Column(String(64))         
    brokerid = Column(INT())        
    point = Column(Float())         

class T_mt4users(declarative_base()):
    # 表的名字:
    __tablename__ = 'T_MT4Users'
    # 表的结构:            
    login = Column(String(64),primary_key=True)         
    brokerid = Column(INT())        
    equity = Column(Float()) 
    balance = Column(Float()) 
    margin = Column(Float()) 

#####获取presto数据
def getPrestoData(login='',brokerID='',echo=False,startTime='1970-01-01 00:00:00.0',endTime='2036-01-01 00:00:00.0',day=None,week=None,month=None,hour=None,symbol=None,masteraccount=None):
    try:
        engine = create_engine(statisticConf.sqlalchemy_presto,echo = echo)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        #查出某个用户所有数据
        t_mt4tradesTable = session.query(
            t_mt4trades.login,t_mt4trades.brokerid,t_mt4trades.cmd,
            t_mt4trades.pips,
            # func.if_(t_mt4trades.point == None, 0,t_mt4trades.point),
            t_mt4trades.profit,
            # func.if_(t_mt4trades.profit == None, 0,t_mt4trades.profit),
            t_mt4trades.swaps,
            # func.if_(t_mt4trades.swaps == None, 0,t_mt4trades.swaps),
            t_mt4trades.commission,
            # func.if_(t_mt4trades.commission == None, 0,t_mt4trades.commission),
            t_mt4trades.standardsymbol,
            t_mt4trades.standardlots,
            t_mt4trades.ticket,
            t_followorders.followorderid,
            t_followorders.status,
            t_followorders.followbrokerid,
            t_followorders.masteraccount,
            t_followorders.masterbrokerid,
            # func.if_(t_mt4trades.standardlots != None, t_mt4trades.standardlots,(0)),
            # func.if_(t_followorders.status != None, t_followorders.status,(0)),
            # func.if_(t_followorders.masteraccount != None, t_followorders.masteraccount,('0')),
            # func.if_(t_followorders.masterbrokerid != None, t_followorders.masterbrokerid,(0)),
            t_mt4trades.open_time,t_mt4trades.close_time).outerjoin(
            t_followorders,and_(t_mt4trades.login==t_followorders.followaccount,
                t_mt4trades.brokerid==t_followorders.followbrokerid,
                t_mt4trades.ticket==t_followorders.followorderid)).outerjoin(
            TD_followorders,and_(t_mt4trades.login==TD_followorders.followaccount,
                t_mt4trades.brokerid==TD_followorders.followbrokerid,
                t_mt4trades.ticket==TD_followorders.followorderid)).filter(
            t_mt4trades.login==login,t_mt4trades.brokerid==brokerID,
            t_mt4trades.close_time >= startTime,t_mt4trades.open_time<endTime,
            t_mt4trades.close_time < endTime).filter(t_mt4trades.profit.isnot(None)).all()
        t_mt4tradesTable_new = []
        #判断经纪商时间
        if brokerID == 1:
            brokerHour = 6
        elif brokerID == 5 or brokerID == 6:
            brokerHour = 6
        elif brokerID == 4:
            brokerHour = 8
        #返回指定时间的数据。如所有星期2/ 所有5月的数据
        if week == None and month == None and hour == None and symbol == None and masteraccount == None and day == None:
            return t_mt4tradesTable
        #symmonth
        elif month != None and symbol != None:
            for i in t_mt4tradesTable:
                    #month需要传入年月，如 2018-6  与mongoDB对应
                    localtime = time.strptime(str(datetime.datetime.strptime(i.close_time, "%Y-%m-%d %H:%M:%S.0") + datetime.timedelta(hours=-brokerHour)), "%Y-%m-%d %H:%M:%S")
                    #月份小于10时，在前面补零。  如： 06月
                    if localtime.tm_mon < 10:
                        months = '0' + str(localtime.tm_mon)
                    else:
                        months = str(localtime.tm_mon)
                    if str(localtime.tm_year) + '-' + months == month and i.standardsymbol == symbol:
                        t_mt4tradesTable_new.append(i)
            return t_mt4tradesTable_new
        #follDay
        elif day != None and masteraccount != None:
            for i in t_mt4tradesTable:
                #day需要传入年月日，如 2018-06-14  与mongoDB对应
                localtime = time.strptime(str(datetime.datetime.strptime(i.close_time, "%Y-%m-%d %H:%M:%S.0") + datetime.timedelta(hours=-brokerHour)), "%Y-%m-%d %H:%M:%S")
                #月份小于10时，在前面补零。  如： 06月
                if localtime.tm_mon < 10:
                    months = '0' + str(localtime.tm_mon)
                else:
                    months = str(localtime.tm_mon)
                #get days
                if localtime.tm_mday < 10:
                    days = '0' + str(localtime.tm_mday)
                else:
                    days = str(localtime.tm_mday)
                if str(localtime.tm_year) + '-' + months + '-' + days == day and i.masteraccount == masteraccount:
                    t_mt4tradesTable_new.append(i)
            return t_mt4tradesTable_new
        else:
            if hour != None:
                for i in t_mt4tradesTable:
                    if time.strptime(str(i.close_time), "%Y-%m-%d %H:%M:%S.%f").tm_hour == hour + brokerHour:
                        t_mt4tradesTable_new.append(i)
                return t_mt4tradesTable_new
            elif day != None:
                for i in t_mt4tradesTable:
                    #day需要传入年月日，如 2018-06-14  与mongoDB对应
                    localtime = time.strptime(str(datetime.datetime.strptime(i.close_time, "%Y-%m-%d %H:%M:%S.0") + datetime.timedelta(hours=-brokerHour)), "%Y-%m-%d %H:%M:%S")
                    #月份小于10时，在前面补零。  如： 06月
                    if localtime.tm_mon < 10:
                        months = '0' + str(localtime.tm_mon)
                    else:
                        months = str(localtime.tm_mon)
                    #get days
                    if localtime.tm_mday < 10:
                        days = '0' + str(localtime.tm_mday)
                    else:
                        days = str(localtime.tm_mday)
                    if str(localtime.tm_year) + '-' + months + '-' + days == day:
                        t_mt4tradesTable_new.append(i)
                return t_mt4tradesTable_new
            elif week != None:
                for i in t_mt4tradesTable:
                    #i.close + 经济上时间 = week
                    if time.strptime(str(datetime.datetime.strptime(i.close_time, "%Y-%m-%d %H:%M:%S.0") + datetime.timedelta(hours=-brokerHour)), "%Y-%m-%d %H:%M:%S").tm_wday + 1 == week:
                        t_mt4tradesTable_new.append(i)
                return t_mt4tradesTable_new
            elif month != None:
                for i in t_mt4tradesTable:
                    #month需要传入年月，如 2018-6  与mongoDB对应
                    localtime = time.strptime(str(datetime.datetime.strptime(i.close_time, "%Y-%m-%d %H:%M:%S.0") + datetime.timedelta(hours=-brokerHour)), "%Y-%m-%d %H:%M:%S")
                    #月份小于10时，在前面补零。  如： 06月
                    if localtime.tm_mon < 10:
                        months = '0' + str(localtime.tm_mon)
                    else:
                        months = str(localtime.tm_mon)
                    if str(localtime.tm_year) + '-' + months == month:
                        t_mt4tradesTable_new.append(i)
                return t_mt4tradesTable_new
            elif symbol != None:
                for i in t_mt4tradesTable:
                    if i.standardsymbol == symbol:
                        t_mt4tradesTable_new.append(i)
                return t_mt4tradesTable_new
            elif masteraccount != None:
                for i in t_mt4tradesTable:
                    if i.masteraccount == masteraccount:
                        t_mt4tradesTable_new.append(i)
                return t_mt4tradesTable_new
    finally:    
        session.close()
        # print("session.close()")


def statisticQuota(table=[],quota='',openTime='1970-01-01 00:00:00.0',closeTime='1970-01-01 00:00:00.0'):
    ##获取基础指标#############
    #平仓亏损订单数
    deal_loss_close = []
    #平仓盈利订单数
    deal_profit_close = []
    #平仓做多盈利笔数
    deal_profit_long_close = []
    #平仓做空盈利笔数
    deal_profit_short_close = []
    #平仓做多订单
    deal_long_close = []
    #持仓盈利订单
    deal_profit_open = []
    ##平仓盈利
    money_profit_close = []
    #平仓亏损
    money_loss_close = []
    #盈利总额
    money_profit_sum = []
    #平仓收益总额，平仓订单收益
    money_close = []
    money_long_close = []
    money_short_close = []
    #近N天平仓收益总额
    profit_close_sum_Nday = []
    #N天前的净值
    deposit_sum_Nday = []
    #平仓亏损总额
    money_loss_sum = []
    #每张订单的收益.包括持仓单求在途回撤率的的历史已平仓订单最大收益需要用到
    deal_profit =[]
    #做空盈利订单收益列表
    money_profit_short_close = []
    #做空亏损订单收益列表
    money_loss_short_close = []
    #做多盈利订单收益列表
    money_profit_long_close = []
    #做多亏损订单收益列表
    money_loss_long_close = []
    #做空盈利订单点数列表
    point_profit_short_close = []
    #做空亏损订单点数列表
    point_loss_short_close = []
    #做多盈利订单点数列表
    point_profit_long_close = []
    #做多亏损订单点数列表
    point_loss_long_close = []
    #平仓点数
    point_close = []
    #平仓盈利点数
    point_profit_close = []
    #平仓亏损点数
    point_loss_close = []
    #盈利订单总点数，包括持仓
    point_profit_sum = []
    #亏损订单总点数，包括持仓
    point_loss_sum = []
    #持仓时间
    time_possession = []
    time_possession_long = []
    time_possession_short = []
    #交易周期
    period_trade = []
    #平仓标准手
    standardlots_close = []
    #买标准手
    standardlots_long_close = []
    #卖标准手
    standardlots_short_close = []
    # #累计如金
    deposit = []
    #累计出金
    withdraw = []
    #净值
    equity = []
    #余额
    balance = []
    #跟随者自主平仓订单笔数
    deal_cs = []
    #跟随者跟随平仓订单笔数
    deal_cf = []
    #盈利订单数量，包括持仓
    deal_profit_sum = []
    #亏损订单数量，包括持仓
    deal_loss_sum = []
    #做空订单
    deal_short_close = []
    #自主开仓笔数
    deal_os = []
    #跟随者自主开仓笔数
    deal_foll_os = []
    #跟随开仓笔数
    deal_of = []
    #跟随开仓盈利笔数
    deal_profit_cf = []
    deal_profit_cs = []
    deal_loss_cf = []
    #交易笔数
    deal_close = []
    #全部跟随收益
    money_follow_close_all = []
    #跟随获利点数
    point_cf = []
    point_cs = []
    #自主收益
    money_cs = []
    #跟随获利
    money_cf = []
    #自主开仓
    money_os = []
    #跟随开仓
    money_of = []
    #自主手数
    standardlots_cs = []
    #自主亏损
    money_loss_cs = []
    money_loss_cf = []
    deal_loss_cs = []
    #跟随手数
    standardlots_cf = []
    #自主平仓盈利收益金额
    money_profit_cs = []
    #跟随平仓盈利收益金额
    money_profit_cf = []

    allDealTime = []
    if len(table) > 0:
        for i in table:
            allDealTime.append(i.close_time)
        lastDealTime = max(allDealTime)
    else:
        lastDealTime = '2036-01-01 00:00:00.0'
    

    quotaValue = []
    for collect in table:
        # print(collect)
        if collect.profit != None and collect.swaps != None and collect.commission != None:
            totalProfit = collect.profit + collect.swaps + collect.commission

        #平仓所有相关指标
        if collect.cmd in (0,1) and collect.close_time > closeTime:
            if quota == 'money_close':
                money_close.append(totalProfit)
                quotaValue = money_close
            if quota == 'point_close':
                point_close.append(collect.pips)
                quotaValue = point_close
            if quota == 'standardlots_close':
                standardlots_close.append(collect.standardlots)
                quotaValue = standardlots_close
            if quota == 'deal_close':
                deal_close.append(collect)
                quotaValue = deal_close
            if quota == 'time_possession':
                #持仓时间
                diffTime = (parse(collect.close_time) - parse(collect.open_time)).total_seconds()  #计算结束时间与开始时间的时间差（秒）
                time_possession.append(diffTime)
                quotaValue = time_possession
            if quota == 'period_trade':
                #交易周期
                period_trade.append(collect.open_time)
                quotaValue = period_trade



        #平仓做多相关指标
        if collect.cmd == 0  and collect.close_time > closeTime:
            if quota == 'money_long_close':
                money_long_close.append(totalProfit)
                quotaValue = money_long_close
            if quota == 'standardlots_long_close':
                standardlots_long_close.append(collect.standardlots)
                quotaValue = standardlots_long_close
            if quota == 'deal_long_close':
                deal_long_close.append(collect)
                quotaValue = deal_long_close
            if quota == 'time_possession_long':
                #持仓时间
                diffTime = (parse(collect.close_time) - parse(collect.open_time)).total_seconds()  #计算结束时间与开始时间的时间差（秒）
                time_possession_long.append(diffTime)
                quotaValue = time_possession_long

        #平仓做空相关指标
        if collect.cmd == 1  and collect.close_time > closeTime:
            if quota == 'money_short_close':
                money_short_close.append(totalProfit)
                quotaValue = money_short_close
            if quota == 'standardlots_short_close':
                standardlots_short_close.append(collect.standardlots)
                quotaValue = standardlots_short_close
            if quota == 'deal_short_close':
                deal_short_close.append(collect)
                quotaValue = deal_short_close
            if quota == 'time_possession_short':
                #持仓时间
                diffTime = (parse(collect.close_time) - parse(collect.open_time)).total_seconds()  #计算结束时间与开始时间的时间差（秒）
                time_possession_short.append(diffTime)
                quotaValue = time_possession_short

        #平仓盈利相关指标
        if collect.cmd in (0,1) and totalProfit >= 0 and collect.close_time > closeTime:
            if quota == 'money_profit_close':
                money_profit_close.append(totalProfit)
                quotaValue = money_profit_close
            if quota == 'point_profit_close':
                point_profit_close.append(collect.pips)
                quotaValue = point_profit_close
            if quota == 'deal_profit_close':
                deal_profit_close.append(collect)
                quotaValue = deal_profit_close

        #平仓亏损相关指标
        if collect.cmd in (0,1) and totalProfit < 0 and collect.close_time > closeTime:
            if quota == 'money_loss_close':
                money_loss_close.append(totalProfit)
                quotaValue = money_loss_close
            if quota == 'point_loss_close':
                point_loss_close.append(collect.pips)
                quotaValue = point_loss_close
            if quota == 'deal_loss_close':
                deal_loss_close.append(collect)
                quotaValue = deal_loss_close

        #平仓做多盈利相关指标
        if collect.cmd == 0 and totalProfit >= 0 and collect.close_time > closeTime:
            if quota == 'money_profit_long_close':
                money_profit_long_close.append(totalProfit)
                quotaValue = money_profit_long_close
            if quota == 'point_profit_long_close':
                point_profit_long_close.append(collect.pips)
                quotaValue = point_profit_long_close
            if quota == 'deal_profit_long_close':
                deal_profit_long_close.append(collect)
                quotaValue = deal_profit_long_close

        #平仓做多亏损相关指标
        if collect.cmd == 0 and totalProfit < 0 and collect.close_time > closeTime:
            if quota == 'money_loss_long_close':
                money_loss_long_close.append(totalProfit)
                quotaValue = money_loss_long_close
            if quota == 'point_loss_long_close':
                point_loss_long_close.append(collect.pips)
                quotaValue = point_loss_long_close

        #平仓做空盈利相关指标
        if collect.cmd == 1 and totalProfit >= 0 and collect.close_time > closeTime:
            if quota == 'money_profit_short_close':
                money_profit_short_close.append(totalProfit)
                quotaValue = money_profit_short_close
            if quota == 'point_profit_short_close':
                point_profit_short_close.append(collect.pips)
                quotaValue = point_profit_short_close
            if quota == 'deal_profit_short_close':
                deal_profit_short_close.append(collect)
                quotaValue = deal_profit_short_close

        #平仓做空亏损相关指标
        if collect.cmd == 1 and totalProfit < 0 and collect.close_time > closeTime:
            if quota == 'money_loss_short_close':
                money_loss_short_close.append(totalProfit)
                quotaValue = money_loss_short_close
            if quota == 'point_loss_short_close':
                point_loss_short_close.append(collect.pips)
                quotaValue = point_loss_short_close

        #平仓+持仓盈利相关指标
        if collect.cmd in (0,1) and totalProfit >= 0:
            if quota == 'money_profit_sum':
                money_profit_sum.append(totalProfit)
                quotaValue = money_profit_sum
            if quota == 'point_profit_sum':
                point_profit_sum.append(collect.pips)
                quotaValue = point_profit_sum

        #平仓+持仓亏损相关指标
        if collect.cmd in (0,1) and totalProfit < 0 and collect.close_time > closeTime:
            if quota == 'money_loss_sum':
                money_loss_sum.append(totalProfit)
                quotaValue = money_loss_sum
            if quota == 'point_loss_sum':
                point_loss_sum.append(collect.pips)
                quotaValue = point_loss_sum

        #持仓盈利相关指标
        if collect.cmd in (0,1) and totalProfit >= 0 and collect.close_time == closeTime:
            if quota == 'money_profit_open':
                money_profit_open.append(totalProfit)
                quotaValue = money_profit_open

        ###################################################
        ######跟随者相关指标###############################
        #跟随平仓所有相关指标
        if collect.ticket==collect.followorderid and collect.brokerid==collect.followbrokerid and collect.cmd in (0,1) and collect.status!=20 and collect.close_time>closeTime:
            if quota == 'money_cf':
                money_cf.append(totalProfit)
                quotaValue = money_cf
            if quota == 'point_cf':
                point_cf.append(collect.pips)
                quotaValue = point_cf
            if quota == 'standardlots_cf':
                standardlots_cf.append(collect.standardlots)
                quotaValue = standardlots_cf
            if quota == 'deal_cf':
                deal_cf.append(collect)
                quotaValue = deal_cf
        #自主平仓所有相关指标
        # if collect.ticket!=collect.followorderid and collect.brokerid==collect.followbrokerid and collect.cmd in (0,1) and collect.status!=20 and collect.close_time>closeTime:
        if (collect.ticket!=collect.followorderid and collect.cmd in (0,1) and collect.close_time > closeTime) or\
                (collect.status==20 and collect.ticket == collect.followorderid and collect.brokerid==collect.followbrokerid and collect.cmd in (0,1) and collect.close_time>closeTime) :
            if quota == 'money_cs':
                money_cs.append(totalProfit)
                quotaValue = money_cs
            if quota == 'point_cs':
                point_cs.append(collect.pips)
                quotaValue = point_cs
            if quota == 'standardlots_cs':
                standardlots_cs.append(collect.standardlots)
                quotaValue = standardlots_cs
            if quota == 'deal_cs':
                deal_cs.append(collect)
                quotaValue = deal_cs
        #跟随平仓盈利相关指标
        if collect.ticket==collect.followorderid and collect.brokerid==collect.followbrokerid and collect.cmd in (0,1) and totalProfit>=0 and collect.status!=20 and collect.close_time>closeTime:
            if quota == 'money_profit_cf':
                money_profit_cf.append(totalProfit)
                quotaValue = money_profit_cf
            if quota == 'deal_profit_cf':
                deal_profit_cf.append(collect)
                quotaValue = deal_profit_cf
        #跟随亏损相关指标
        if collect.ticket==collect.followorderid and collect.brokerid==collect.followbrokerid and collect.cmd in (0,1) and totalProfit<0 and collect.status!=20 and collect.close_time>closeTime:
            if quota == 'money_loss_cf':
                money_profit_cf.append(totalProfit)
                quotaValue = money_profit_cf
            if quota == 'deal_loss_cf':
                deal_loss_cf.append(collect)
                quotaValue = deal_loss_cf
        #自主平仓盈利相关指标
        # if collect.ticket==collect.followorderid and collect.brokerid==collect.followbrokerid and collect.cmd in (0,1) and collect.profit>=0 and collect.status==20 and collect.close_time>closeTime:
        if (collect.ticket != collect.followorderid and collect.cmd in (0, 1) and collect.close_time > closeTime and totalProfit >=0) or \
                    (collect.status == 20 and collect.ticket == collect.followorderid and collect.brokerid == collect.followbrokerid and collect.cmd in (0, 1)
                     and collect.close_time > closeTime and totalProfit >=0):
            if quota == 'money_profit_cs':
                money_profit_cs.append(totalProfit)
                quotaValue = money_profit_cs
            if quota == 'deal_profit_cs':
                deal_profit_cs.append(collect)
                quotaValue = deal_profit_cs
        #自主平仓亏损相关指标
        # if collect.ticket==collect.followorderid and collect.brokerid==collect.followbrokerid and collect.cmd in (0,1) and collect.profit<0 and collect.status==20 and collect.close_time>closeTime:
        if (collect.ticket != collect.followorderid and collect.cmd in (0, 1) and collect.close_time > closeTime and totalProfit < 0) or\
                  (collect.status == 20 and collect.ticket == collect.followorderid and collect.brokerid == collect.followbrokerid and collect.cmd in (0, 1)
             and collect.close_time > closeTime and totalProfit < 0):
            if quota == 'money_loss_cs':
                money_profit_cs.append(totalProfit)
                quotaValue = money_profit_cs
            if quota == 'deal_loss_cs':
                deal_loss_cs.append(collect)
                quotaValue = deal_loss_cs
        #自主开仓相关指标
        if collect.ticket!=collect.followorderid and collect.cmd in (0,1) and collect.open_time>openTime:
            if quota == 'money_os':
                money_os.append(totalProfit)
                quotaValue = money_os
            if quota == 'deal_os':
                deal_os.append(collect)
                quotaValue = deal_os

        #跟随开仓相关指标
        if collect.ticket==collect.followorderid and collect.brokerid == collect.followbrokerid and collect.cmd in (0,1) and collect.open_time>openTime:
            if quota == 'money_of':
                money_of.append(totalProfit)
                quotaValue = money_of
            if quota == 'deal_of':
                deal_of.append(collect)
                quotaValue = deal_of

        #入金相关
        if collect.cmd in (6,7) and collect.profit > 0:
            if quota == 'deposit':
                deposit.append(collect.profit)
                quotaValue = deposit
        #出金相关
        if collect.cmd in (6,7) and collect.profit < 0:
            if quota == 'withdraw':
                withdraw.append(collect.profit)
                quotaValue = withdraw
        #余额相关
        if collect.close_time > closeTime:
            if quota == 'balance':
                balance.append(totalProfit)
                quotaValue = balance
        #净值相关
        if  quota == 'equity':
            equity.append(totalProfit)
            quotaValue = equity
    return quotaValue


###获取规整mongoDB数据
def mongoData(host='',port=3717,db='',table='',find={}):
    mongoDB = FMCommon.mongoDB_operater(host = host, port = port,db = db,table = table,find = find)
    for i in mongoDB:
        mongoList = {}
        for key in statisticConf.mongoKeyListAll:
            try:
                value = i[key]
            except KeyError:
                value = statisticConf.keyErr
            mongoList[key]=value
    try:
        return FMCommon.Storage(mongoList)
    except:
        print("Error: connect mongo DB fail or no data.")

###获取规整peresto数据
def prestoData(login='',brokerID='',echo=False,startTime='1970-01-01 00:00:00.0',endTime='2036-01-01 00:00:00.0',day=None,week=None,month=None,hour=None,symbol=None,masteraccount=None):
    t_MT4TradesTable = getPrestoData(login=login,brokerID=brokerID,echo=echo,startTime=startTime,endTime=endTime,day=day,week=week,month=month,hour=hour,symbol=symbol,masteraccount=masteraccount)
    prestoList = {}
    for quota in statisticConf.prestoQuotaList:
        try:
            value = statisticQuota(table = t_MT4TradesTable, quota = quota)
        except KeyError:
            value = statisticConf.keyErr
        prestoList[quota] = value
    return FMCommon.Storage(prestoList)


#获取n天以前的时间
#-1 表示1天前。返回的时间时秒分取整，例如：2018-04-07 00:00:00.000
def n_dayAgo(days=-1):
    curr_time = datetime.datetime.now() + datetime.timedelta(days=days)
    n_dayAgo = curr_time.strftime('%Y-%m-%d 00:00:00.000')
    return n_dayAgo

#获取consul某节点下符合某个条件的score
#node, tradescore-config 下所有数据
# quotaValue 给出的指标值，计算出得分
def tradeScore(node='',quotaValue=0,quotaName=''):
    for i in node.dimensions[0]["trader_condtion_groups"]:
        if i["name"] == quotaName:
            print("")
            print(i["conditions"])
            for j in i["conditions"]:
                if j['start'] <= quotaValue < j['end']:
                    return i['score'] * j['proportion_score']
                else:
                    return 0
########################公共#########################
#通过userid和accountindex获取mt4account
def getMt4Account(userID='',accountIndex=''):
    sql="SELECT Mt4Account from T_UserAccount where Userid="+ userID+ " and accountindex="+accountIndex
    resultList = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],sql=sql)
    for mtuple in resultList:
        for item in mtuple:
            return item

#通过userid和accountindex获取brokerid
def BrokerId(userID='',accountIndex=''):
    sql="SELECT brokerid from T_UserAccount where Userid="+ userID+ " and accountindex="+accountIndex
    resultList = FMCommon.mssql_operater(host=webAPIData['mssql_host'],port=webAPIData['mssql_port'],
            uid=webAPIData['db_user'],pwd=webAPIData['db_passwd'],database=webAPIData['FM_OS_DB'],sql=sql)
    for mtuple in resultList:
        for item in mtuple:
            return item