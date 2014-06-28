# coding: utf-8
#!/usr/bin/env python

import logging

from webscraper.utils import Singleton
from webscraper.utils.beanstalkhelper import BeanstalkHelper


class ProfileQueue(Singleton):

    def add(self):
        try:
            queue = BeanstalkHelper().getHostLocal()

            data = "alooo"

            logging.debug("[ContextQueue] message=%s" % data)

            queue.use("context")
            logging.debug("[ContextQueue] use=context OK")
            queue.put(data)

            logging.debug("[ContextQueue] - PUT OK %s" % data)
        except Exception:
            logging.exception("[ContextQueue] Nao foi possivel realizar o put agora")