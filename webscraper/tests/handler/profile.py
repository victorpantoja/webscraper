# coding: utf-8
import tornado
import simplejson
from tornado.httpclient import HTTPRequest
from tornado.testing import AsyncHTTPTestCase
from webscraper.handlers.profile import ProfileHandler
from webscraper.models.profile import Profile


class ProfileHandlerTest(AsyncHTTPTestCase):

    def get_app(self):

        routes = [
            (r"/profile", ProfileHandler)
        ]

        return tornado.web.Application(routes)

    def setUp(self):
        self.username = "victor.pantoja.77"
        super(ProfileHandlerTest, self).setUp()

    def tearDown(self):
        super(ProfileHandlerTest, self).tearDown()
        Profile().remove({'username': self.username})

    def test_get_profile(self):
        '''Getting a profile'''

        request = HTTPRequest(url=self.get_url('/profile?username={0}'.format(self.username)), method='GET')

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        content = simplejson.loads(response.body)
        #first time that user profile is required
        self.assertEqual(content['msg'], 'processing request')

        #second time that user profile is required
        self.http_client.fetch(request, self.stop)
        response = self.wait()
        content = simplejson.loads(response.body)

        self.assertIn("name", content)
        self.assertIn("short_description", content)
        self.assertIn("image", content)
        self.assertIn("popularity", content)
        self.assertEqual(content['username'], self.username)
