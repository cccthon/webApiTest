import sys
import os
import json
import yaml
import datetime
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
megagameData = FMCommon.loadTradeMegagameYML()


#######################################################
##presto 数据库表结构
class T_mt4trades(declarative_base()):
    # 表的名字:
    __tablename__ = 'T_MT4Trades'
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
    # COMMENT = Column(String(256))
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
    # Pips = Column(Float(53),nullable=True)

class T_followreport(declarative_base()):
    # 表的名字:
    __tablename__ = 'T_FollowReport'
    # 表的结构:
    Id = Column(INT, primary_key=True)
    masteraccount = Column(String(64))       
    masterbrokerid = Column(INT())  
    traderid = Column(INT())        
    followaccount = Column(String(64))         
    followbrokerid = Column(INT())                               
    endDate = Column(String)

class T_followorders(declarative_base()):
    # 表的名字:
    __tablename__ = 'T_FollowOrders'
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

class T_mt4tradesinfo(declarative_base()):
    # 表的名字:
    __tablename__ = 'T_mt4TradesInfo'
    # 表的结构:
    Id = Column(INT, primary_key=True)
    ticket = Column(INT())            
    login = Column(String(64))         
    brokerid = Column(INT())        
    point = Column(Float())         

#####获取presto数据
def getMssqlData(login='',brokerID='',echo=False,positTime='1970-01-01 00:00:00.000',closeTime='1970-01-01 00:00:00.000'):
    try:
        engine = create_engine(megagameData["sqlalchemy_mssql"],echo = echo)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        #查出某个用户所有数据
        T_MT4TradesTable = session.query(
            T_mt4trades.login,T_mt4trades.brokerid,T_mt4trades.cmd,
            T_mt4trades.profit,T_mt4trades.swaps,T_mt4trades.commission,
            T_mt4trades.standardlots,T_followorders.status,
            func.if_(T_followorders.masteraccount != None, T_followorders.masteraccount,('0')),
            func.if_(T_followorders.masterbrokerid != None, T_followorders.masterbrokerid,(0)),
            T_mt4trades.open_time,T_mt4trades.close_time).outerjoin(
            T_followorders,and_(T_mt4trades.login==T_followorders.followaccount,
                T_mt4trades.brokerid==T_followorders.followbrokerid,
                T_mt4trades.ticket==T_followorders.followorderid)).filter(
            T_mt4trades.login==login,T_mt4trades.brokerid==brokerID,
            or_(T_mt4trades.close_time==positTime,T_mt4trades.close_time >= closeTime)).all()
        return T_MT4TradesTable
    finally:
        session.close()
        # print("session.close()")

quotaValue = ''
def statisticQuota(table=[],quota='',closeTime='1970-01-01 00:00:00.000'):
    ##获取基础指标#############
    #平仓收益
    profit_close = 0
    #交易手数
    standard_lots = 0
    #交易笔数
    orders = 0
    #实盘跟随人数，去除模拟跟随
    follower_count = []

    global quotaValue
    for collect in table:
        # print(collect.status)
        totalProfit = collect.profit + collect.swaps + collect.commission
        #平仓收益
        if  quota == 'profit_close' and collect.cmd in (0,1) and collect.close_time > datetime.datetime.strptime(closeTime,'%Y-%m-%d 00:00:00.000'):
            profit_close += totalProfit
            quotaValue = profit_close
        #交易手数
        if  quota == 'standard_lots' and collect.cmd in (0,1) and collect.close_time > datetime.datetime.strptime(closeTime,'%Y-%m-%d 00:00:00.000'):
            standard_lots += collect.standardlots
            quotaValue = standard_lots
        #交易笔数
        if  quota == 'orders' and collect.cmd in (0,1) and collect.close_time > datetime.datetime.strptime(closeTime,'%Y-%m-%d 00:00:00.000'):
            orders += 1
            quotaValue = orders
        #交易笔数
        if  quota == 'follower_count' and collect.endDate == '1970-01-01 00:00:00.000': #datetime.datetime.strptime(,'%Y-%m-%d 00:00:00.000'):
            print("11111")
            follower_count.append(collect.masteraccount)
            print("222",follower_count)
            quotaValue = follower_count

    return quotaValue






