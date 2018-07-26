#========================================================
#+++++++++++++++++  测试运行和测试报告设置   ++++++++++++++++
#   默认跑account目录下的全部用例
#   可以通过addTest方法添加指定测试用例进行连跑
#=========================================================
import sys,unittest,time,yaml,re,os,string,shutil
sys.path.append("../../lib/common")
import HTMLTestRunnerEN
import FMCommon
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

#读入配置文件中数据
commonData = FMCommon.loadPublicYML()
webApiData = FMCommon.loadWebAPIYML()
#####################################
#定义需要参与连跑的测试用例
#将account目录下的所有FM开头的python脚本加入测试套
testSuite = FMCommon.testSuite('../../test', 'FM*.py')
# tester = FMCommon.get_computer_info()
print("countTestCases: ", testSuite.countTestCases())
for i in testSuite:
    print(str(i).split('tests=')[-1])

currYear = time.strftime('%Y',time.localtime(time.time()))
currMonth = time.strftime('%m',time.localtime(time.time()))
currDay = time.strftime('%d',time.localtime(time.time()))

reportDir = '../../report/webApiTest' + '/' + currYear + currMonth + '/' + currDay + '/' + 'new'
#创建报告目录
FMCommon.mkdir(reportDir)



######################################
#开始主程序
if __name__ == '__main__':
    report = open(reportDir + '/index.html','wb')
    testRunner = HTMLTestRunnerEN.HTMLTestRunner(
        stream=report, 
        title=commonData['reportTitle'],
        description=commonData['reportFitTitle'] + webApiData['hostName'],
        tester = FMCommon.lastCommit())
    testRunner.run(testSuite)
    report.close()

#将生成的测试报告备份为带时间后缀的html。如：index_201801151415.html
currTime = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
shutil.copyfile(reportDir + '/index.html', '../../report/webApiTest' + '/' + currYear + currMonth + '/' + currDay + '/' + currTime + '.html')

#获取测试结果
status = FMCommon.getCharInFile(reportDir + '/index.html','</strong>')
print("Test Result " + str(status))

###################################
#通过邮件发送测试结果
print("send test result to mail...")
currTime = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
localtime = time.localtime()
mmeText = '\n' + str(commonData['reportMailContent']) + '\n\n' + str(status) + '\n\n' + str(commonData['reportMailContent2']) + '/' + currYear+currMonth + '/' + currDay + '/' + 'new'
fromAddr = commonData['reportFromAddr']
reportToTest = commonData['reportToTest']
reportToAll = commonData['reportToAll']

subject = commonData['reportSubject'] + currTime
smtpServer = commonData['reportSmtpServer']
passwd= commonData['reportPasswd']
#发送邮件。当前时间小于7时或者大于22点。收件人为all。
if localtime.tm_hour < 7 or localtime.tm_hour > 22:
    print(reportToAll)
    FMCommon.sendMail(mmeText,fromAddr,reportToAll,subject,smtpServer,passwd)
else:
    print(reportToTest)
    FMCommon.sendMail(mmeText,fromAddr,reportToTest,subject,smtpServer,passwd)

print("=================autoTest done.===================")