# coding: utf-8
#!/usr/bin/env python

import beanstalkc
import logging
from webscraper import settings
from webscraper.utils import Singleton


class BeanstalkHelper(Singleton):
    beanstalk_local = None

    def getHostLocal(self):
        if self.beanstalk_local:
            try:
                self.beanstalk_local.use("path")
            except beanstalkc.SocketError, se:
                self.beanstalk_local = None
                logging.error("[BEANSTALK][TORNADO] could not connect to beanstalkd")
        
        if not self.beanstalk_local:
            host, port = settings.BEANSTALK.split(":")            
            try:
                self.beanstalk_local = beanstalkc.Connection(host=host, port=int(port))
                logging.info("[BEANSTALK][TORNADO][%s] - connected! " % host)
            except beanstalkc.SocketError, se:
                logging.error("[BEANSTALK][TORNADO][%s] - could not connect to beanstalkd" % host)
        
        return self.beanstalk_local