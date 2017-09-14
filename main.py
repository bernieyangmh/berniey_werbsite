# coding=utf-8

import concurrent.futures
import tornado.ioloop
import tornado.web
import tornadoredis
import tornadis
from config import handlers, settings, mysql_config, web_config, redis_cache_config
import torndb
import tornado.httpserver
import sys


class Application(tornado.web.Application):
    def __init__(self):
        settings.update(ui_modules={"Article": ArticleModule})
        super(Application, self).__init__(handlers, **settings)
        self.thread_executor = concurrent.futures.ThreadPoolExecutor()

        self.db = torndb.Connection(
            host=mysql_config["mysql_host"], database=mysql_config["mysql_database"],
            user=mysql_config["mysql_user"], password=mysql_config["mysql_password"], time_zone="+8:00")

        self.redis_cache = tornadis.Connection(
            host=redis_cache_config['host'], port=redis_cache_config['port'],
            stop_after=redis_cache_config['stop_after'])

        self.redis_cache = tornadoredis.Connection(
            host=redis_cache_config['host'], port=redis_cache_config['port'],
            stop_after=redis_cache_config['stop_after'])


class ArticleModule(tornado.web.UIModule):
    def render(self, article):
        print "article render"
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
