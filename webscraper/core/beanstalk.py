# coding: utf-8
import logging
import time
import beanstalkc
from bson.objectid import ObjectId
import simplejson
from datetime import datetime
from scraper.models.profile import Facebook
from scraper.models.profile import Twitter
from webscraper.core.daemon import Daemon
from webscraper.models.job import Job
from webscraper.models.job import STATUS_EXECUTING
from webscraper.models.job import STATUS_FINISHED


class WebScraperBeanstalk(Daemon):
    beanstalkServer = None

    def __init__(self, pidfile, host, tube):
        self.host = host.split(":")[0]
        self.port = host.split(":")[1]
        self.tube = tube

        return Daemon.__init__(self, pidfile)

    '''
        loopback to stablish connect with beanstalk
    '''
    def connect(self):
        while not self.beanstalkServer:
            try:
                self.beanstalkServer = beanstalkc.Connection(host=self.host, port=int(self.port))

                if self.tube == 'context':
                    self.beanstalkServer.watch("context")

                logging.info("Can be connect with beanstalk on %s:%s" % (self.host, self.port))
            except beanstalkc.SocketError, se:
                logging.error("Can not connect to beanstalk on %s:%s" % (self.host, self.port))
                time.sleep(10)

    def run(self):
        logging.info("WebScraper Beanstalk Daemon initialized, waiting for job! :D")
        self.connect()

        while True:
            try:
                job = self.beanstalkServer.reserve()

                logging.debug("job: %s" % job.body)

                job_dict = simplejson.loads(job.body)

                job_db = Job().find_one({'global_id': job_dict['job']})
                job_db['status'] = STATUS_EXECUTING

                id_dict = {"_id": job_db['_id']}
                update_dict = job_db

                Job().update(id_dict=id_dict, update_dict=update_dict)

                if job_dict["type"] == "Facebook":
                    profile = Facebook().as_profile_dict(**job_dict)
                    profile.save()
                if job_dict["type"] == "Twitter":
                    profile = Twitter().as_profile_dict(**job_dict)
                    profile.save()

                job_db['profile'] = profile._id
                job_db['status'] = STATUS_FINISHED
                job_db['completed_at'] = datetime.now()
                Job().update(id_dict=id_dict, update_dict=update_dict)

                job.delete()
            except beanstalkc.SocketError, se:
                logging.exception("lost connect with beanstalk, trying restablish")
                self.beanstalkServer = None
                self.connect()
