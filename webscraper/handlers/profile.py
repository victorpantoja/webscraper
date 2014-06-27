# coding: utf-8
import simplejson
from tornado.web import RequestHandler
from tornado.web import HTTPError
from webscraper.utils.profile import ProfileQueue


class ProfileHandler(RequestHandler):

    def get(self, **kw):
        try:
            username = self.get_argument('username')
        except HTTPError, e:
            self.set_status(400)
            self.finish('{}')

        #user exists in database
        if False:
            ProfileQueue().add()
            self.finish(simplejson.dumps({"msg": "processing request"}))

        profile_dict = {'name': 'Victor Pantoja',
                        'short_description': 'A web developer at globo.com', #if available!
                        'image': "should-be-image",
                        'popularity': 10}

        self.finish(simplejson.dumps(profile_dict))
