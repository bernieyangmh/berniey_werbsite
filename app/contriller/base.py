# coding=utf-8

import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user_cookies")
        if not user_id:
            return None
        a = self.db.get("SELECT username, id FROM users WHERE id = %s", int(user_id))
        return a

    def any_author_exists(self):
        return bool(self.db.get("SELECT * FROM users LIMIT 1"))

    def write_error(self, status_code, **kwargs):
        print "write_error"
        if status_code == 403:
            self.render("403.html")
        elif status_code == 404:
            self.render("404.html")
        elif status_code == 405:
            self.render("405.html")
        elif status_code == 500:
            self.render("500.html")
        if not self._finished:
            super(BaseHandler, self).write_error(status_code, **kwargs)


class HomeHandler(BaseHandler):

    def get(self):
        print 'HomeHandler_get'
        articles = self.db.query("""
                                SELECT
                                 users.username, articles.created_time,articles.slug,
                                 articles.title,articles.html
                                 FROM articles  left join users
                                 on articles.users_id = users.id
                                  ORDER BY articles.created_time DESC LIMIT  5""")
        feedback = self.db.query("""
                                Select user_name, content, created_time
                                From feedback
                                ORDER BY created_time DESC
                                limit 20
                                """)
        self.render("home.html", articles=articles, feedback=feedback)


class ArticleHandler(BaseHandler):
    def get(self, slug):
        print 'AntryHandler_get'
        article = self.db.get("SELECT users.username, articles.created_time, articles.title,articles.html, articles.id, articles.users_id, articles.slug  FROM articles   left join users on  articles.users_id = users.id WHERE articles.slug = %s", slug)
        print article
        if not article:
            raise tornado.web.HTTPError(404)
        self.render("article.html", article=article)


class ArchiveHandler(BaseHandler):
    def get(self):
        print 'ArchiveHandler_get'
        articles = self.db.query("SELECT * FROM articles ORDER BY update_time "
                                "DESC")
        self.render("archive.html", articles=articles)


class FeedHandler(BaseHandler):
    def get(self):
        print 'FeedHandler_get'
        self.render(".html")
