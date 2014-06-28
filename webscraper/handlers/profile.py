# coding: utf-8
import logging
import simplejson
from tornado.web import RequestHandler
from tornado.web import HTTPError
from scraper.models.profile import Facebook
from scraper.models.profile import Twitter
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

        try:
            profile_fb = Facebook().find_one({'username': fb_username})
            profile_tw = Twitter().find_one({'username': tw_username})

            #user exists in database
            if not profile_fb or not profile_tw:
                self.set_status(202)

                if not profile_fb:
                    ProfileQueue().add(data=simplejson.dumps({'type': 'Facebook', 'username': fb_username}))

                if not profile_tw:
                    ProfileQueue().add(data=simplejson.dumps({'type': 'Twitter', 'username': tw_username}))

                self.finish(simplejson.dumps({"msg": "processing request"}))
            else:
                profile = Facebook.create(profile_fb)
                self.finish(simplejson.dumps(profile.as_dict(), default=date_handler))
        except Exception:
            logging.exception("Could not process request")
            self.set_status(500)
            self.finish({"msg": "internal server error"})
