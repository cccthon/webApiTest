import grpc,sys,unittest,yaml,uuid,json,time,datetime
from dateutil.parser import parse #pip3 install python-dateutil
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")
import FMCommon,consul

tradeMegagameData = FMCommon.loadTradeMegagameYML()
userData = yaml.load(open('../../conf/common/common.yml', 'r',encoding='utf-8'))
userDataAPI = FMCommon.loadWebAPIYML()

with open("TimeInterval.json", 'r', encoding='utf-8') as load_file:
    load_dict = json.load(load_file)

class GetPeriodStartTime(object):
    def getTimeInterval(time='2018-03-11 08:00:00', brokerid='1'):
        timezone = 0
        for key in load_dict:

            if key['id'] == brokerid and key['id'] == 1:
                for locations in key['locations']:
                    if locations['start'] <= time and time <= locations['end']:
                        if locations['timezone'] == 'Etc/GMT-3':
                            # brokerTime = (bj_time - datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
                            timezone = 5
                        if locations['timezone'] == 'Etc/GMT-2':
                            # brokerTime = (bj_time - datetime.timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")
                            timezone = 6
            if key['id'] == brokerid and key['id'] == 3:

                for locations in key['locations']:
                    if locations['start'] <= time and time <= locations['end']:
                        if locations['timezone'] == 'Etc/GMT-3':
                            # brokerTime = (bj_time - datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
                            timezone = 5
            if key['id'] == brokerid and key['id'] == 4:
                # brokerTime = (bj_time - datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
                timezone = 8
            if key['id'] == brokerid and key['id'] == 5:

                for locations in key['locations']:
                    if locations['start'] <= time and time <= locations['end']:
                        if locations['timezone'] == 'Etc/GMT-2':
                            # brokerTime = (bj_time - datetime.timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")
                            timezone = 6

            if key['id'] == brokerid and key['id'] == 6:

                for locations in key['locations']:
                    if locations['start'] <= time and time <= locations['end']:
                        if locations['timezone'] == 'Etc/GMT-2':
                            # brokerTime = (bj_time - datetime.timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")
                            timezone = 6
        return timezone

        #传入截止时间 北京时间
    def getPeriodStartTime(initialTime,period,brokerid,timeType):

        sql = "select starttime,endtime from T_Holiday order by starttime desc"

        mysqlHoliday = FMCommon.mssql_operater_all(host=userDataAPI['dataHost'], port=userDataAPI['dataPost'],
                                                   database=userDataAPI['database_V3'], uid=userDataAPI['dataID'],
                                                   pwd=userDataAPI['dataPWD'], sql=sql)
        brokerTime = initialTime
        period_current = 0
        # print(mysqlHoliday)
        if timeType == 'start':
            while True:
                flag = True
                for key in mysqlHoliday:
                    if brokerTime >= key["starttime"] and brokerTime <= key["endtime"]:
                        flag = False
                        break
                if flag:
                    period_current += 1

                if period_current == period:
                    break
                brokerTime = datetime.datetime.strptime(brokerTime, "%Y-%m-%d")
                brokerTime = (brokerTime - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        else:
                brokerTime = datetime.datetime.strptime(brokerTime, "%Y-%m-%d").strftime("%Y-%m-%d")


        brokerTime = datetime.datetime.strptime(brokerTime + ' 00:00:00', "%Y-%m-%d 00:00:00").strftime(
            "%Y-%m-%d 00:00:00")

        timezone = GetPeriodStartTime.getTimeInterval(brokerTime, brokerid)

        bjTime=(datetime.datetime.strptime(brokerTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=timezone)).strftime(
            "%Y-%m-%d %H:%M:%S")
        return bjTime


