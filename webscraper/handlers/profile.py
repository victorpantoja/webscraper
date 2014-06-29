# coding: utf-8
import logging
from uuid import uuid1
import simplejson
from bson.objectid import ObjectId
from datetime import datetime
from tornado.web import RequestHandler
from tornado.web import HTTPError
from scraper.models.profile import Facebook
from scraper.models.profile import Twitter
from webscraper.models.job import Job
from webscraper.models.job import STATUS_CREATED
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

                #Gonna create 2 jobs to gain performance as each job can execute separetely
                if not profile_fb:
                    job = Job()
                    job._id = ObjectId()
                    job.global_id = uuid1().get_hex()
                    job.status = STATUS_CREATED
                    job.started_at = datetime.now()
                    job.save()

                    ProfileQueue().add(data=simplejson.dumps({'job': job.global_id,
                                                              'type': 'Facebook',
                                                              'username': fb_username}))

                if not profile_tw:
                    job = Job()
                    job._id = ObjectId()
                    job.global_id = uuid1().get_hex()
                    job.status = STATUS_CREATED
                    job.started_at = datetime.now()
                    job.save()

                    ProfileQueue().add(data=simplejson.dumps({'job': job.global_id,
                                                              'type': 'Twitter',
                                                              'username': tw_username}))

                self.finish(simplejson.dumps({"msg": "processing request"}))
            else:
                profile = Facebook.create(profile_fb)
                self.finish(simplejson.dumps(profile.as_dict(), default=date_handler))
        except Exception:
            logging.exception("Could not process request")
            self.set_status(500)
            self.finish({"msg": "internal server error"})
