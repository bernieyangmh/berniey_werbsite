# -*- coding: utf-8 -*-

import time
import re
import sys
import json, subprocess
import tempfile

from .base import BaseHandler
import tornado.web
import markdown
import unicodedata
from tornado.queues import Queue
from extends.utils import get_timestamp_date, url_decode_encode, python_script_run


d = {}



class ComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        print 'ComposeHandler_get'
        id = self.get_argument("id", None)
        article = None
        if id:
            article = self.db.get("SELECT * FROM articles WHERE id = %s", int(id))
        self.render("compose.html", article=article)

    @tornado.web.authenticated
    def post(self):
        print 'ComposeHandler_post'
        id = self.get_argument("id", None)
        title = self.get_argument("title")
        text = self.get_argument("markdown")
        html = markdown.markdown(text)
        if id:
            article = self.db.get("SELECT * FROM articles WHERE id = %s", int(id))
            if not article: raise tornado.web.HTTPError(404)
            slug = article.slug
            self.db.execute(
                "UPDATE articles SET title = %s, markdown = %s, html = %s "
                "WHERE id = %s", title, text, html, int(id))
        else:
            slug = unicodedata.normalize("NFKD", title).encode(
                "ascii", "ignore")
            slug = re.sub(r"[^\w]+", " ", slug)
            slug = "-".join(slug.lower().strip().split())
            if not slug:
                slug = "article"
            while True:
                e = self.db.get("SELECT * FROM articles WHERE slug = %s", slug)
                if not e: break
                slug += "-2"
            title = title.encode("utf-8")
            text = text.encode("utf-8")
            html = html.encode("utf-8")
            self.db.execute(
                "INSERT INTO articles (users_id,title,slug,markdown,html,"
                "created_time, update_time) VALUES (%s,%s,%s,%s,%s,now(), now())",
                self.current_user.id, title, slug, text, html)
        self.redirect("/article/" + slug)


class CallbackHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render("callback.html", callback_request=d.get(args, {}))

    def post(self, *args, **kwargs):
        print self.request.__dict__
        print args
        d.update({args: self.request.__dict__})


class FeedBackHandler(BaseHandler):

    def post(self, *args, **kwargs):
        print "FeedBackHandler_post"
        content = self.get_arguments("feedback").pop() if self.get_arguments("feedback") else "null"
        print content
        print type(content)
        content = content.replace('"', '\\"')

        if self.current_user:
            users_id = self.current_user.get("id")
            user_name = self.current_user.get("username")
            self.db.execute(u"""
                            Insert into feedback(users_id, user_name, content, created_time)
                              values
                            ({}, "{}", "{}", now())
                            """.format(users_id, user_name, content))
        else:
            self.db.execute(u"""
                            Insert into feedback(content, created_time)
                              values
                            ("{}", now())
                            """.format(content))




class Test1Handler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("test.html")


class ToolsHandler(BaseHandler):

    def get(self, *args, **kwargs):
        timestamp=None
        self.render("tools.html", timestamp=timestamp)

    def post(self, *args, **kwargs):
        print "ToolsHandler_post"

        if self.get_arguments("timestamp"):
            timestamp_data_res = get_timestamp_date(self.get_arguments("timestamp")[0])
        else:
            timestamp_data_res = None

        if self.get_arguments("urlcode"):
            url = self.get_arguments("urlcode")[0]
            print url
            print type(url)
            url_code = url_decode_encode(url)
        else:
            url_code = None
        self.render("tools.html", timestamp_data_res=timestamp_data_res, url_code=url_code)


class PythonHandler(BaseHandler):

    def get(self):
        print "PythonHandler_get"
        self.render("func/python_script.html")

    def post(self, *args, **kwargs):

        # print self.get_arguments("python_script")
        print self.get_arguments("version")
        python_script_code = "# -*- coding: utf-8 -*- \n\n" + self.get_arguments("python_script")[0]

        res_output = python_script_run(self.get_arguments("version")[0], python_script_code)

        self.write(res_output)

