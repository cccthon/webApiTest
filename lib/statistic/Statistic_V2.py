import sys
import json
import yaml
import consul
import datetime,time
from socketIO_client import SocketIO
from dateutil.parser import parse
sys.path.append("../../lib/common")
import FMCommon
from pyhive import presto 
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

webAPIData = FMCommon.loadWebAPIYML()
commonCof = FMCommon.loadPublicYML()
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
def getPrestoData(login='',brokerID='',quotaValue='',echo=True,startTime='1970-01-01 00:00:00.1',updatets='2036-01-01 00:00:00.0',day=None,week=None,month=None,hour=None,symbol=None,masteraccount=None):
    engine = create_engine(statisticConf.sqlalchemy_presto,echo = echo)
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        print("")
        print("sqlalchemy.engine.base.Engine >>>>>>>>>>>>>>>>>>>>>>>>:")
        
        #求当前brokerid所在时区
        brokerHour = brokerTimeZone(brokerID=brokerID,host=commonCof.consulHost,port=commonCof.consulPort)
        print("<<<",quotaValue,">>>","login:",login,"brokerID:",brokerID," brokerHour:",brokerHour)
        #计算时间减掉经纪商时间差
        brokerTimeEndTime =  str(datetime.datetime.strptime(updatets,"%Y-%m-%d %H:%M:%S.0") + datetime.timedelta(hours = brokerHour)) + '.0'
        #openTime N小时以前，一般用于减去经纪商时间后
        nHourAgo = text("interval '%s' hour" % (brokerHour))
        nHourAgo_op = cast(t_mt4trades.open_time, TIMESTAMP) - nHourAgo

        filterType_op = text('')
        #判断指标类型
        if hour != None:
            filterType_op = extract('hour', cast(t_mt4trades.open_time,TIMESTAMP)) - brokerHour == hour
        elif week != None:
            #extract 星期：dow，小时：hour，月：month
            filterType_op = extract('dow', cast(nHourAgo_op,TIMESTAMP))  == week
        
        #总收益为：profit+commission+swaps. 当为null时置0
        totalProfit = (func.if_(t_mt4trades.profit == None, 0,t_mt4trades.profit) + func.if_(t_mt4trades.swaps == None, 0,t_mt4trades.swaps) + 
            func.if_(t_mt4trades.commission == None, 0,t_mt4trades.commission))

        #查询条件定义####################
        #总收益
        if quotaValue in ['money_profit_close','money_loss_close','moneyop_close_profit','moneyop_close_loss']:
            sqlQuery = func.sum(totalProfit)
        #总点数
        if quotaValue in ['point_profit_close','point_loss_close','pointop_close_profit','pointop_close_loss']:
            sqlQuery = func.sum(t_mt4trades.pips)
        #总手数
        if quotaValue in ['standardlotsop_close','standardlotsop_close_profit','standardlotsop_close_loss','standardlotsop_close_short','standardlotsop_close_long']:
            sqlQuery = func.sum(t_mt4trades.standardlots)
        #总订单数
        if quotaValue in ['deal_close']:
            sqlQuery = func.count(t_mt4trades.ticket)

        ##过滤条件定义######################
        ##############################  open_time相关指标  ################################
        ##过滤条件： 总（收益，手数，点数）
        if quotaValue in ['standardlotsop_close','deal_close']:
            sqlFilter = and_(t_mt4trades.cmd.in_([0,1]), filterType_op)
        ##过滤条件： 盈利相关（收益，手数，点数）
        if quotaValue in ['pointop_close_profit','moneyop_close_profit','standardlotsop_close_profit']:
            sqlFilter = and_(t_mt4trades.cmd.in_([0,1]),totalProfit >= 0, filterType_op)
        ##过滤条件： 亏损相关（收益，手数，点数）
        if quotaValue in ['pointop_close_loss','moneyop_close_loss','standardlotsop_close_loss']:
            sqlFilter = and_(t_mt4trades.cmd.in_([0,1]),totalProfit < 0, filterType_op)
        ##过滤条件： 做多相关（收益，手数，点数）
        if quotaValue in ['standardlotsop_close_long']:
            sqlFilter = and_(t_mt4trades.cmd == 0, filterType_op)
        ##过滤条件： 做空相关（收益，手数，点数）
        if quotaValue in ['standardlotsop_close_short']:
            sqlFilter = and_(t_mt4trades.cmd == 1, filterType_op)

        #查出某个用户所有数据
        t_mt4tradesTable = session.query(
            sqlQuery.label(quotaValue)
            # t_mt4trades.cmd,
            # t_mt4trades.ticket,
            # t_mt4trades.pips,
            # t_mt4trades.profit,
            # t_mt4trades.swaps,
            # t_mt4trades.commission,
            # t_mt4trades.open_time,
            # t_mt4trades.close_time,
            # func.cast(t_mt4trades.open_time, TIMESTAMP) - text("interval '6' hour")
            ).outerjoin(
            t_followorders,and_(t_mt4trades.login==t_followorders.followaccount,
                t_mt4trades.brokerid==t_followorders.followbrokerid,
                t_mt4trades.ticket==t_followorders.followorderid)).outerjoin(
            TD_followorders,and_(t_mt4trades.login==TD_followorders.followaccount,
                t_mt4trades.brokerid==TD_followorders.followbrokerid,
                t_mt4trades.ticket==TD_followorders.followorderid)).filter(t_mt4trades.login==login,t_mt4trades.brokerid==brokerID).filter(
                sqlFilter
            ).filter(and_(t_mt4trades.close_time >= startTime,
            t_mt4trades.close_time < brokerTimeEndTime,
            )).all()
        # res = {}
        # for i in t_mt4tradesTable:
        #     # print(i)
        #     res[quotaValue] = i[0]
        for i in t_mt4tradesTable:
            # print(i)
            if None == i[0]:
                res = 0
            else:
                res = i[0]
        return res

    finally:        
        session.close()


#获取kev/value 相关信息.获取经纪商时区信息
def brokerTimeZone(brokerID='',host='',port=8500,node='broker_location',kv='followme/config'):
    c = consul.Consul(host=host,port=port,scheme='http')
    data = c.kv.get(kv)
    try:
        for zone in json.loads(data[1]['Value'].decode('utf-8'))[node]:
            if zone['id'] == brokerID:
                res = zone["locations"][0]["timezone"].split('GMT')[-1]
        #东八区加上经纪商时区，
        return  8 + int(res)
    except:
        return "consul: srv connect fail or no data."


###获取规整mongoDB数据
def mongoData(host='',port=3717,db='',table='',find={}):
    mongoDB = FMCommon.mongoDB_operater(host = host, port = port,db = db,table = table,find = find)
    print("MongoClient info: %s %s %s" % (db,table,find))
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
        print("Error: connect mongo DB fail or %s %s no data." % (table,find))



if __name__ == '__main__':
    #################################################################################
    login = '830005'   #trader
    brokerID = 5


    pointop_close_profit = getPrestoData(login=login,brokerID=brokerID,week=2,echo=True,quotaValue='pointop_close_profit',updatets='2018-07-23 09:47:00.0')

    print(pointop_close_profit)




    # print(parse('20160101-11:00:00'))

    # currtime = datetime.datetime.now()
    # print(type(currtime))
    # print((currtime -datetime.timedelta(hours=6)).strftime("%Y-%m-%d %H:%M"))

    # str1 = '2018-04-20 20:07:52.000'

    # # print(str1.split('.')[0])

    # date_time = datetime.datetime.strptime(str1.split('.')[0], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=-6)

    # print(date_time,type(date_time))

    # print(date_time + datetime.timedelta(hours=-6))