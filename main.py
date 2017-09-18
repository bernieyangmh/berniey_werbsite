# -*- coding: utf-8 -*-

import sys
import concurrent.futures
import tornado.ioloop
import tornado.web
from config import handlers, settings, mysql_config, web_config, redis_cache_config
import torndb
import tornado.httpserver
import pymysql

class Application(tornado.web.Application):
    def __init__(self):
        settings.update(ui_modules={"Article": ArticleModule})
        super(Application, self).__init__(handlers, **settings)
        self.thread_executor = concurrent.futures.ThreadPoolExecutor(4)



        self.db = torndb.Connection(
            host=mysql_config["mysql_host"], database=mysql_config["mysql_database"],
            user=mysql_config["mysql_user"], password=mysql_config["mysql_password"], time_zone="+8:00")



class ArticleModule(tornado.web.UIModule):
    def render(self, article):

        return self.render_string("modules/article.html", article=article)


def main():
    http_server = tornado.httpserver.HTTPServer(Application(), max_body_size=150*1024*1024)
    http_server.listen(web_config["port"])
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'upgradedb':

            from alembic.config import main
            main("upgrade head".split(' '), 'alembic')
            exit(0)

    main()
