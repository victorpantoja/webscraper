# coding: utf-8
#!/usr/bin/env python

import os, sys, getopt, logging


def usage():
    print "\WebScraper Beanstalk daemon consummer:"
    print "usage: beanstalk_consumer.py [--env=ENV_RUN][--tube=context][--help] COMMAND"
    print "     start       start consummer"
    print "     stop        stop consummer"
    print "     restart     restart consummer"
    print "     help        show this help message\n"
    
def main():

    try:
        optlists, command = getopt.getopt(sys.argv[1:], "het", ["help", "env=", "tube="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    env = "PROD"
    tube = "context"
    
    for opt, value in optlists:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-e", "--env"):
            env = value
        elif opt in ("-t", "--tube"):
            tube = value
    
    pidfile = "/opt/logs/webscrapper/beanstalkd-%s.pid" % tube
    
    if not command or command[0] not in ["start", "stop", "restart"]:
        usage()
        sys.exit()

    project_root = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.abspath("%s/.." % project_root))
    
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)s %(levelname)s %(message)s',
        filename = "/opt/logs/webscrapper/beanstalkd.log",
        filemode = 'a'
    )

    # settings
    from webscraper import core
    from webscraper import settings
    
    core.settings = settings

    from webscraper.core.beanstalk import WebScraperBeanstalk
    beanstalk_consumer = WebScraperBeanstalk(pidfile=pidfile, host=settings.BEANSTALK, tube=tube)

    #uncomment to not run as a deamon
    #beanstalk_consumer.run()

    if command[0] == "start":
        beanstalk_consumer.start()

    elif command[0] == "stop":
        beanstalk_consumer.stop()

    elif command[0] == "restart":
        beanstalk_consumer.restart()
    
if __name__ == "__main__":
    main()
