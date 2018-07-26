import sys,unittest,json,requests,gc,redis,re,time

sys.path.append("../../lib/business")
sys.path.append("../../lib/common")
sys.path.append("../../lib/webAPI")

import FMCommon

userData = FMCommon.loadWebAPIYML()

class OperationMysqlDB():
    @staticmethod
    def operationPyramidDB(mysql):
        row = FMCommon.mysql_operaters(userData['beta_mysql_host'],
                                       userData['beta_mysql_port'],
                                       'pyramid',
                                       userData['beta_mysql_user'],
                                       userData['beta_mysql_passwd'],
                                       mysql)
        return row