
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

tests: clean
	@echo "Running tests..."
	@export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/webscraper  &&  \
		cd webscraper && \
	    nosetests -s --verbose --with-coverage --cover-package=webscraper tests/handler/*

start-beanstalkd:
	@echo "Starting beanstalkd..."
	@beanstalkd -l 0.0.0.0 -p 11300

stop-beanstalkd:
	@echo "Stopping beanstalkd..."
#   -ps -ef | egrep 'beanstalkd -d' | egrep -v egrep | tr -s ' ' | cut -f 3 -d ' ' | xargs kill
	@killall beanstalkd 2> /dev/null; true
