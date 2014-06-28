# coding: utf-8
from tornado.web import URLSpec

from webscraper.handlers.page import PageHandler
from webscraper.handlers.profile import ProfileHandler

urls = (
    URLSpec(r'/(?P<page>index.html)?', PageHandler, name='home'),
    URLSpec(r'/?(?P<version>v1.0)?/profile', ProfileHandler, name='profile'),
)
