# coding: utf-8
from tornado.web import RequestHandler
from webscraper.utils.profile import ProfileQueue


class ProfileHandler(RequestHandler):

    def get(self, **kw):
        ProfileQueue().add()

        return "OK"
