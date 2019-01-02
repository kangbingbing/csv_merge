# coding:utf-8

import tornado.httpserver
import tornado.web
from MysqlHelper import MysqlHelper
from lib.CCPRestSDK import REST
import json
import os
import glob
import time
from lib.sendMsg import Mail
import random
import hashlib
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

upload_path = os.path.join(os.path.dirname(__file__), '../files')  # 文件的暂存路径


class IndexHandler(tornado.web.RequestHandler):

    def get(self):

        cookie = self.get_secure_cookie("sessionid")
        # print(cookie)
        # 没有cookie 设置cookie
        if not cookie:
            random_value = time.time() + random.uniform(0, 100)
            session_id =  hashlib.md5(str(random_value)).hexdigest()
            self.set_secure_cookie('sessionid', session_id)
        else:
            # 有cookie 找到这个文件夹, 删除所有文件
            session_id_path = upload_path + '/' + cookie
            report_path = './report/' + cookie
            self.del_file(session_id_path)
            self.del_file(report_path)

        self.render("index.html")

    def post(self):

        cookie = self.get_secure_cookie("sessionid")
        session_id_path = upload_path + '/' + cookie
        if not os.path.exists(session_id_path):
            os.makedirs(session_id_path)

        file_metas = self.request.files['file']  # 提取表单中‘name’为‘file’的文件元数据
        for meta in file_metas:
            filename = meta['filename']
            filepath = os.path.join(session_id_path, filename)
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
            self.write(json.dumps({"code": 0, "msg": "返回成功"}))


    def del_file(self,path):

        if os.path.exists(path):
            for i in os.listdir(path):
                path_file = os.path.join(path, i)
                if os.path.isfile(path_file):
                    os.remove(path_file)
                else:
                    self.del_file(path_file)


class MergeHandler(tornado.web.RequestHandler):

    def get(self):

        cookie = self.get_secure_cookie("sessionid")
        report_path = './report/' + cookie
        report_csv_list = glob.glob(report_path +'/*.csv')
        report_csv_list.sort()
        # print(report_csv_list)
        if len(report_csv_list):
            download_file_path = report_csv_list[-1]
            print('开始下载' + download_file_path)
            download_file_name = os.path.basename(download_file_path)
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=' + download_file_name)
            # 读取的模式需要根据实际情况进行修改
            with open(download_file_path, 'rb') as f:
                while True:
                    data = f.read(1024*1024)
                    if not data:
                        break
                    self.write(data)
            self.finish()
        else:
            self.write(json.dumps({"code": 0, "msg": "当前没有可下载文件"}))


    def post(self):

        email = self.get_argument('email','')
        print(email)

        cookie = self.get_secure_cookie("sessionid")
        session_id_path = upload_path + '/' + cookie
        report_path = './report/' + cookie

        csv_list = glob.glob(session_id_path +'/*.csv')

        if len(csv_list):
            print('共发现%s个CSV文件' % len(csv_list))
            print('正在处理............')
            now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
            report_path = './report/' + cookie

            if not os.path.exists(report_path):
                os.makedirs(report_path)

            file_name = report_path + '/' + now + r"_report.csv"
            print(file_name)
            for i in csv_list:
                file = open(i, 'r').read()
                with open(file_name, 'a') as f:
                    f.write(file)
            print('合并完毕！')
            if len(email):
                mailto_list = [email]
                if Mail.send_mail_part(mailto_list, "数据已合并完毕", "你好，数据已处理完毕，请查收。", file_name):
                    self.write(json.dumps({"code": 1, "msg": "正在发送至您的邮箱"}))
                else:
                    self.write(json.dumps({"code": 0, "msg": "发送邮箱失败，请直接下载"}))
            else:
                self.write(json.dumps({"code": 1, "msg": "开始下载"}))
        else:
            print('没有可合并的文件! ')
            self.write(json.dumps({"code": 0, "msg": "当前没有可合并的文件"}))


