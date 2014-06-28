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
            username = self.get_argument('username')
        except HTTPError, e:
            self.set_status(400)
            self.finish('{}')

        profile_db = Profile().find_one({'username': username})

        #user exists in database
        if not profile_db:
            ProfileQueue().add(data=simplejson.dumps({'username': username}))
            self.set_status(202)
            self.finish(simplejson.dumps({"msg": "processing request"}))
        else:
            profile = Profile.create(profile_db)
            self.finish(simplejson.dumps(profile.as_dict(), default=date_handler))
