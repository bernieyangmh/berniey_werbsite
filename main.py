# coding=utf-8

import tornado.ioloop
import tornado.web
from config import handlers, settings, db_config, web_config
import torndb
import tornado.httpserver
import sys


class Application(tornado.web.Application):
    def __init__(self):
        settings.update(ui_modules={"Article": ArticleModule})
        super(Application, self).__init__(handlers, **settings)

        self.db = torndb.Connection(
            host=db_config["mysql_host"], database=db_config["mysql_database"],
            user=db_config["mysql_user"], password=db_config["mysql_password"], time_zone="+8:00")


class ArticleModule(tornado.web.UIModule):
    def render(self, article):
        print "article render"
        return self.render_string("modules/article.html", article=article)


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    # http_server = tornado.httpserver.HTTPServer(Application(), max_body_size=150*1024*1024)
    http_server.listen(web_config["port"])
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'upgradedb':

            from alembic.config import main
            main("upgrade head".split(' '), 'alembic')
            exit(0)

    main()
