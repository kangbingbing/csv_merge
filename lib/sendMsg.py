# -*- coding:utf-8 -*-
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from lib.CCPRestSDK import REST

#--------------------------------邮箱配置------------------------------
mailto_list=['kangbing@ruanrongkeji.com']
mail_host="smtp.mxhichina.com"
mail_user="kangbing"
mail_postfix="ruanrongkeji.com"
#--------------------------------邮箱配置------------------------------

#--------------------------------短信配置------------------------------
accountSid= '8a48b5515388ec150153c6682c8c6005'
accountToken= '5606ebc2b7be4a729dde8fe2ad0b4bf1'
appId='8aaf0708560730a501560b263c340299'
serverIP='app.cloopen.com'
serverPort='8883'
softVersion='2013-12-26'
#--------------------------------短信配置------------------------------


class Mail:

    @classmethod
    def send_mail(self,to_list,sub,content):
        '''
        :param to_list:     ['493043919@qq.com'] 多个收件人,号隔开
        :param sub:         邮件子标题
        :param content:     邮件正文
        :return:            返回是否发送成功
        '''
        me="机器人小冰"+"<"+mail_user+"@"+mail_postfix+">"
        msg = MIMEText(content,'plain', 'utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(mail_host)      #连接服务器
            server.login("kangbing@ruanrongkeji.com","Kb123!@#")
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False


    @classmethod
    def send_mail_part(self,to_list,sub,content,path):
        '''
        :param to_list:     ['493043919@qq.com'] 多个收件人,号隔开
        :param sub:         邮件子标题
        :param content:     邮件正文
        :param path:        附件路径
        :return:            返回是否发送成功
        '''
        text = MIMEText(content, 'plain', 'utf-8')

        msg = MIMEMultipart()
        msg.attach(text)
        try:
            with open(path, 'rb') as rb:
                apart = MIMEApplication(rb.read())
                file_name = os.path.basename(path)
                apart.add_header('Content-Disposition', 'attachment', filename=file_name)
                msg.attach(apart)
        except:
            print '没有附件文件'

        # apart = MIMEApplication(open(file_path, 'rb').read())

        me="机器人处理"+"<"+mail_user+"@"+mail_postfix+">"
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(mail_host)      #连接服务器
            server.login("kangbing@ruanrongkeji.com","Kb123!@#")
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False


class Sms:

    @classmethod
    def sendTemplateSMS(cls,to,datas,tempId):
        '''
        :param to:      '18911606898' 多个收信人,隔开
        :param datas:   []  多个占位符, 里面为字符串
        :param tempId:  模板id
        :return:        无
        '''
        rest = REST(serverIP,serverPort,softVersion)
        rest.setAccount(accountSid,accountToken)
        rest.setAppId(appId)
        result = rest.sendTemplateSMS(to,datas,tempId)

        for k,v in result.iteritems():
            if k=='templateSMS' :
                    for k,s in v.iteritems():
                        print '%s:%s' % (k, s)
            else:
                print '%s:%s' % (k, v)