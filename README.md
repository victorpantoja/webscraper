[![Travis CI](https://travis-ci.org/victorpantoja/webscraper.svg?branch=master)](victorpantoja/webscraper)

webscraper
==========

Just an easy way to get Facebook and Twitter Profiles

DEPENDENCIES
------------

After instaling, please make sure you have the following dependencies:
- Python 2.7+
- beanstalkd: http://kr.github.io/beanstalkd/download.html
- mongodb


INSTALING
---------
$ mkvirtualenv webscraper
$ make setup


RUNNING
------------
$ make start


TESTING
----------
$ make tests


Deploying
----------

WebScraper uses Amazon EC2. So, before deploying, make sure you have your AWS credentials and nginx.conf properly configured.

If so, you can configure environment:
$ fab -i <your-.pem-file> prod setup

and deploy your code:
$ fab -i <your-.pem-file> prod deploy

