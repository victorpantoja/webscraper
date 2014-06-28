# coding: utf-8
import simplejson
from tornado.web import RequestHandler
from tornado.web import HTTPError
from webscraper.models.profile import Profile
from webscraper.utils.profile import ProfileQueue


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


class ProfileHandler(RequestHandler):

    def get(self, **kw):
        try:
            fb_username = self.get_argument('facebook_username')
            tw_username = self.get_argument('twitter_username')
        except HTTPError, e:
            self.set_status(400)
            self.finish('{}')

        profile_fb = Profile().find_one({'username': fb_username})
        profile_tw = Profile().find_one({'username': fb_username})

        #user exists in database
        if not profile_fb:
            ProfileQueue().add(data=simplejson.dumps({'username': fb_username}))
            self.set_status(202)
            self.finish(simplejson.dumps({"msg": "processing request"}))
        else:
            profile = Profile.create(profile_fb)
            self.finish(simplejson.dumps(profile.as_dict(), default=date_handler))
