# -*- coding: utf-8 -*-

import time
import logging

from conqueue.conqueue import Conqueue
from conqueue.lib.config import BaseConfig

class Configuration(BaseConfig):
   REDIS_SERVER_INFO = {
      'host'     : 'localhost',
      'port'     : 6379,
      'db'       : 0,
   }

   USE_MULTI_PROCESSING = True

# set logging level as debug in development
# logging.basicConfig(level=logging.DEBUG)

def parse_feed(data):
    time.sleep(2)
    print data

def receive_message(data):
    print "i got the message: %s" % data

# listens two queues: ['feeds', 'messages']
worker = Conqueue(Configuration).worker()
worker.register_task('feeds', parse_feed)
worker.register_task('messages', receive_message)

worker.listen_tasks()



