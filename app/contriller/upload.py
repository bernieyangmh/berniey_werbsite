# coding=utf-8

import logging
from urllib import unquote
import os

import tornado.web
from tornado import gen
from concurrent import futures
from base import BaseHandler

from extends.utils import data_analysis

base_path = os.path.dirname(os.path.realpath(__file__))
dir_name = os.path.join(base_path.split("app")[0], 'upload_files')

executor = futures.ThreadPoolExecutor(2)


class UploadPOSTHandler(BaseHandler):

    @gen.coroutine
    def post(self):
        print self.request.arguments.get("user_dir")
        if self.request.arguments.get("user_dir")[0]:
            user_dir = self.request.arguments.get("user_dir")[0]

        else:
            import hashlib
            md = hashlib.md5()
            md.update(self.get_secure_cookie("user_cookies"))
            user_dir = md.hexdigest()
        user_path = os.path.join(dir_name, user_dir)
        if not os.path.isdir(user_path):
            os.mkdir(user_path)

        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info['filename'], info['content_type']
                body = info['body']
                file_path = os.path.join(user_path, filename)
                with open(r'%s' % file_path, "w") as data:
                    data.write(body)
        print "upload finished"
        res = yield executor.submit(data_analysis, user_path, 20)
        print "finished"
        self.render("data_analysis.html", res=res)


class UploadHtmlHandler(BaseHandler):

    def get(self):
        print "UploadHtmlHandler_get"
        self.render("upload.html")

