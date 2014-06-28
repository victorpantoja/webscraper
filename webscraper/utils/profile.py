# coding: utf-8
#!/usr/bin/env python

import logging

from webscraper.utils import Singleton
from webscraper.utils.beanstalkhelper import BeanstalkHelper


class ProfileQueue(Singleton):

    def add(self, data=None):
        try:
            queue = BeanstalkHelper().getHostLocal()
            logging.debug("[ProfileQueue] message=%s" % data)

            queue.use("context")
            logging.debug("[ProfileQueue] use=context OK")
            queue.put(data)
        except Exception:
            logging.exception("[ProfileQueue] Could not send job to queue")
