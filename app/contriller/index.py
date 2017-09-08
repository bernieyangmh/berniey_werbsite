# coding=utf-8

from .base import BaseHandler
import tornado.web
import markdown
import unicodedata
import re
from tornado.queues import Queue
d={}

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


class Test1Handler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("test.html")
