
all: clean

clean:
	find . -name '*.pyc' | xargs rm -f
	rm -rf build

deploy-prod:
	fab -i ~/Documents/victorpantoja.pem prod deploy

setup:
	@echo "Installing dependencies..."
	@pip install -r requirements-dev.txt

start:
	PYTHONPATH=`pwd`:`pwd`/webscraper python webscraper/server.py ${PORT}

tests: clean stop-beanstalkd stop-beanstalk-consumer start-beanstalkd start-beanstalk-consumer
	@echo "Running tests..."
	@export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/webscraper  &&  \
		cd webscraper && \
	    nosetests -s --verbose --with-coverage --cover-package=webscraper tests/handler/*

start-beanstalkd:
	@echo "Starting beanstalkd..."
	@beanstalkd -l 0.0.0.0 -p 11300  > /dev/null 2>&1 &

stop-beanstalkd:
	@echo "Stopping beanstalkd..."
	@killall beanstalkd 2> /dev/null; true

start-beanstalk-consumer:
	@echo "Starting beanstalk-consumer..."
	@python beanstalk_consumer.py start

stop-beanstalk-consumer:
	@echo "Stopping beanstalk-consumer..."
	@python beanstalk_consumer.py stop