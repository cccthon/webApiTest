import sys,unittest,yaml,uuid,json,time,datetime
from dateutil.parser import parse #pip3 install python-dateutil
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
import FMCommon,consul

tradeMegagameData = FMCommon.loadTradeMegagameYML()
userData = yaml.load(open('../../conf/common/common.yml', 'r',encoding='utf-8'))
userDataAPI = FMCommon.loadWebAPIYML()


# startTime = '2018-01-06'
# endTime = '2018-01-10'


# #传入起始时间，求出有多少交易日
# def trade_numOfDay(startTime='',endTime='',dbHost='',dbPort='',dbName='',dbID='',dbPWD=''):
#     sql = "select starttime,endtime from T_Holiday where starttime >= '%s' and endtime <= '%s'" % (startTime,endTime)
#     mysqlHoliday = FMCommon.mssql_operater_all(host=dbHost, port=dbPort,
#                                                database=dbName, uid=dbID,
#                                                pwd=dbPWD, sql=sql)

#     totalDay = (parse(endTime) - parse(startTime)).days + 1
#     dayList = []
#     for i in mysqlHoliday:
#         nDay = parse(i["endtime"]) - parse(i["starttime"])
#         dayList.append(nDay.days + 1)
#     # print(mysqlHoliday)
#     # print("totalDay:",totalDay,"holiday:",sum(dayList),"tradeDay:",totalDay - sum(dayList))
#     return totalDay - sum(dayList)

# startTime = '2018-04-20'
# endTime = '2018-07-24'

startTime = '2018-04-20 20:07:52.0'
endTime = '2018-07-24 18:23:01.0'

print(parse(startTime).strftime("%Y-%m-%d"))

dbHost=userDataAPI['dataHost']
dbPort=userDataAPI['dataPost']
dbName=userDataAPI['database_V3']
dbID=userDataAPI['dataID']
dbPWD=userDataAPI['dataPWD']

trade_numOfDay = FMCommon.trade_numOfDay(startTime,endTime,dbHost,dbPort,dbName,dbID,dbPWD)
print(trade_numOfDay)



# if __name__ == '__main__':
#     startTime = '2018-01-04'
#     endTime = '2018-01-15'
#     dbHost=userDataAPI['dataHost']
#     dbPort=userDataAPI['dataPost']
#     dbName=userDataAPI['database_V3']
#     dbID=userDataAPI['dataID']
#     dbPWD=userDataAPI['dataPWD']

#     trade_numOfDay = trade_numOfDay(startTime,endTime,dbHost,dbPort,dbName,dbID,dbPWD)
#     print(trade_numOfDay)


