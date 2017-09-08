# coding=utf-8

import os


from app.contriller.base import HomeHandler, ArticleHandler, FeedHandler, ArchiveHandler, BaseHandler
from app.contriller.index import ComposeHandler, CallbackHandler, Test1Handler
from app.contriller.auth import AuthCreateHandler, AuthLoginHandler, AuthLogoutHandler
from app.contriller.upload import UploadPOSTHandler, UploadPUTHandler, UploadHtmlHandler, AnalysisHandler


handlers = [
    (r"/", HomeHandler),
    (r"/archive", ArchiveHandler),
    (r"/hihi", FeedHandler),
    (r"/test", Test1Handler),
    (r"/analysis", AnalysisHandler),
    (r"/article/([^/]+)", ArticleHandler),
    (r"/compose", ComposeHandler),
    (r"/auth/create", AuthCreateHandler),
    (r"/auth/login", AuthLoginHandler),
    (r"/auth/logout", AuthLogoutHandler),
    (r"/callback/([^/]+)", CallbackHandler),
    (r"/upload", UploadHtmlHandler),
    (r"/upload/post", UploadPOSTHandler),
    (r"/upload/put", UploadPUTHandler),

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

