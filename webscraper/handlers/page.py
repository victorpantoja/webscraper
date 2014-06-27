# coding: utf-8
from tornado.web import RequestHandler


class PageHandler(RequestHandler):

    def get(self, **kwargs):
        self.render("index.html")
