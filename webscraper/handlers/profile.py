# coding: utf-8
import simplejson
from tornado.web import RequestHandler
from tornado.web import HTTPError
from webscraper.models.profile import Profile
from webscraper.utils.profile import ProfileQueue


class ProfileHandler(RequestHandler):

    def get(self, **kw):
        try:
            username = self.get_argument('username')
        except HTTPError, e:
            self.set_status(400)
            self.finish('{}')

        profile = Profile().find_one({'username': username})

        #user exists in database
        if not profile:
            ProfileQueue().add(data=simplejson.dumps({'username': username}))
            self.finish(simplejson.dumps({"msg": "processing request"}))
        else:
            profile_dict = {'name': 'Victor Pantoja',
                            'short_description': 'A web developer at globo.com', #if available!
                            'image': "should-be-image",
                            'popularity': 10,
                            'username': 'victor.pantoja.77'}

            self.finish(simplejson.dumps(profile_dict))
