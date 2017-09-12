# coding=utf-8

import os


from app.contriller.base import HomeHandler, ArticleHandler, FeedHandler, ArchiveHandler, BaseHandler
from app.contriller.functions import ComposeHandler, CallbackHandler, Test1Handler, FeedBackHandler, ToolsHandler, PythonHandler
from app.contriller.auth import AuthCreateHandler, AuthLoginHandler, AuthLogoutHandler
from app.contriller.upload import UploadPOSTHandler, UploadHtmlHandler


handlers = [
    (r"/", HomeHandler),
    (r"/archive", ArchiveHandler),
    (r"/article/([^/]+)", ArticleHandler),
    (r"/auth/create", AuthCreateHandler),
    (r"/auth/login", AuthLoginHandler),
    (r"/auth/logout", AuthLogoutHandler),
    (r"/compose", ComposeHandler),
    (r"/callback/([^/]+)", CallbackHandler),
    (r"/feedback", FeedBackHandler),
    (r"/hihi", FeedHandler),
    (r"/python", PythonHandler),
    (r"/test", Test1Handler),
    (r"/tools/?(.*)", ToolsHandler),
    (r"/upload", UploadHtmlHandler),
    (r"/upload/post", UploadPOSTHandler),

    (r".*", BaseHandler),

]

settings = dict(
    blog_title=u"berniey website",
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    xsrf_cookies=False,
    cookie_secret="LKb5kvHaWZmyO5UJ1_sQQSLpA4WwH8QR6_6msExU",
    login_url="/auth/login",
    debug=True,
)

web_config = {"port": "8888"}

db_config = {"mysql_host": "127.0.0.1:3306", "mysql_database": "website",
             "mysql_user": "work", "mysql_password": "123"
             }

