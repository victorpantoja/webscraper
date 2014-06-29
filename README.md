[![Travis CI](https://travis-ci.org/victorpantoja/webscraper.svg?branch=master)](victorpantoja/webscraper)

webscraper
==========

A Web Application that uses webscrap to scrap for content in web


ARCHITECTURE
------------
WebScraper is implemented in Python. Each component in the software architecture of WebScraper was chosen in order to achieve high performance and scale to thousands of simultaneous requests.

WebScraper uses the nginx HTTP server which is known to be very fast and use few resources such as CPU and memory. Unlike traditional servers, nginx does not use threads to make connections but uses an asynchronous, event-driven architecture (Asynchronous non- blocking I/O), that makes it more scalable than other HTTP servers, and enables nginx to serve thousands of concurrent clients.

Another important component is Tornado, a lean Python framework. Its main features are: simplicity, high performance, open source code, non-blocking I/O and low resource consumption.

WebScraper has a offline component based on consumer / producer paradigm. A profile request sent by a client is queued by the Tornado application with additional information needed. Then, a standalone process (scraper) processes this queue and, for each entry, get the information (article) from the source desired. This producer-consumer pattern could lead to complex concurrency situations (race conditions) but fortunately, Beanstalkd efficiently handles all these concerns.

Job statuses (created, executing and finished), as well as article itself, are stored in mongodb.

SCALING
-------
WebScraper has a modular design and a scalable architecture suited to execute in a cloud or cluster environment: an instance of nginx distributes the load to multiple instances of Tornado using upstream nginx module. The number of instances depends on the server settings and is proportional to the number of processor cores.


BOTTLENECKS
-----------
- current implementation connects synchronously with mongodb using pymongo. It's recommended changing this library for one asynchronously, like asynmongo.
- Tornado also has a asynchronously mode that was not used.


DEPENDENCIES
------------

After instaling, please make sure you have the following dependencies:
- Python 2.7+
- beanstalkd: http://kr.github.io/beanstalkd/download.html
- mongodb
- webscraper-core: this python module contains abstractions for handling with different data sources and with mongodb.


INSTALING
---------
Is strongly recommended using virtualenv and virtualenvwrapper:

  mkvirtualenv webscraper

  make setup


RUNNING
------------
- start beanstalkd (queue manager):

  make start-beanstalkd

- start scraper (consumer):

  make start-beanstalk-consumer

- start application on port 9085:

  make start


TESTING
-------
$ make tests


Deploying
----------

WebScraper uses Amazon EC2. So, before deploying, make sure you have your AWS credentials and nginx.conf properly configured.

If so, you can configure environment:

  fab -i <your-.pem-file> prod setup

and deploy your code:

  fab -i <your-.pem-file> prod deploy


TODO
----
Implement cache layers using nginx and memcached.
