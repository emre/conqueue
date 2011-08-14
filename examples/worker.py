

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
import logging
logging.basicConfig(level=logging.DEBUG)

def hello(data):
    import time
    time.sleep(2)
    print data
    return data

# listens two queues: ['feeds', 'messages']
worker = Conqueue(Configuration, ['feeds', 'messages']).worker()
worker.listen_tasks(hello)



