# coding: utf-8
import logging
import time
import beanstalkc
import simplejson
import pybreaker
import requests
from datetime import datetime
from bson.objectid import ObjectId
from webscraper.core.daemon import Daemon
from webscraper.models.profile import Profile, Facebook


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

                facebook_breaker = pybreaker.CircuitBreaker(fail_max=1, reset_timeout=60)
                response = facebook_breaker.call(requests.get,
                                                 Facebook().get_url_profile(**simplejson.loads(job.body)),
                                                 timeout=5)

                Facebook().as_profile_dict(**simplejson.loads(response.content)).save()

                job.delete()
            except beanstalkc.SocketError, se:
                logging.exception("lost connect with beanstalk, trying restablish")
                self.beanstalkServer = None
                self.connect()
