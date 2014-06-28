import os
from functools import partial
import logging


get_path_to = partial(os.path.join, os.path.dirname(__file__))

DEBUG = False

PORT = 9085

TEMPLATE_PATH = get_path_to("templates")
STATIC_PATH = get_path_to("static")

BEANSTALK_BOXES = ["localhost"]
BEANSTALK = "localhost:11300"
BEANSTALK_HOSTS = ["%s:11300" % box for box in BEANSTALK_BOXES]

database_url = "localhost"
database_port = 27017
database_user = "usr_newsfeed"
database_pwd = "usr_newsfeed"

logging.basicConfig(
    level = getattr(logging, "DEBUG"),
    format = '%(asctime)s %(levelname)s %(message)s',
#    filename = "/opt/logs/webscrapper/webscrapper.log",
#    filemode = 'a'
)

MEMCACHE = {
    'servers': ('localhost:11211',),
    'socket_timeout': 1,
}

