# coding: utf-8
#!/usr/bin/env python

from webscraper.handlers.profile import ProfileHandler

from tornado.testing import AsyncHTTPTestCase
from tornado.httpclient import HTTPRequest

import tornado
import simplejson


class ProfileHandlerTest(AsyncHTTPTestCase):

    def get_app(self):

        routes = [
            (r"/profile", ProfileHandler)
        ]

        return tornado.web.Application(routes)

    def test_get_profile(self):
        '''Getting a profile'''

        request = HTTPRequest(url=self.get_url('/profile?username=victor.pantoja.77'), method='GET')

        self.http_client.fetch(request, self.stop)

        response = self.wait()

        self.failIf(response.error)

        content = simplejson.loads(response.body)

        #tests response structure
        self.assertIn("name", content)
        self.assertIn("short_description", content)
        self.assertIn("image", content)
        self.assertIn("popularity", content)

        #testar a resposta "processando" caso o usuario nao esteja no banco