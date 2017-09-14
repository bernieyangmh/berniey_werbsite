# -*- coding: utf-8 -*-
from .base import BaseHandler
import tornado.web
import concurrent.futures
import bcrypt
from tornado import gen, escape




class AuthCreateHandler(BaseHandler):

    def get(self):
        print 'AuthCreateHandler_get'
        self.render("create_author.html", error='what')

    @gen.coroutine
    def post(self):
        print 'AuthCreateHandler_post'

        hash_password = yield self.submit(
            bcrypt.hashpw, tornado.escape.utf8(self.get_argument("password")),
            bcrypt.gensalt())
        author_id = self.db.execute(
            "INSERT INTO users (email, username, hash_password, phone, created_time) "
            "VALUES (%s, %s, %s, %s, now())",
            self.get_argument("email"), self.get_argument("username"),
            hash_password, self.get_arguments("phone"))
        self.set_secure_cookie("user_cookies", str(author_id))
        self.redirect(self.get_argument("next", "/"))


class AuthLoginHandler(BaseHandler):
    def get(self):
        print 'AuthLoginHandler_get'
        if not self.any_author_exists():
            self.redirect("/auth/create")
        else:
            self.render("login2.html", error=None)

    @gen.coroutine
    def post(self):
        print 'AuthLoginHandler_post'
        user = self.db.get("SELECT hash_password, id FROM users WHERE email = %s",
                             self.get_argument("email"))
        if not user:
            self.render("login.html", error="hi,email not found")
            return
        hash_password = yield self.submit(
            bcrypt.hashpw, escape.utf8(self.get_argument("password")),
            escape.utf8(user.hash_password))
        if hash_password == user.hash_password:
            self.set_secure_cookie("user_cookies", str(user.id))
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render("login.html", error="incorrect password")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        print 'AuthLogoutHandler_get'
        self.clear_cookie("user_cookies")
        self.redirect(self.get_argument("next", "/"))
