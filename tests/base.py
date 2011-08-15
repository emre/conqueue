from conqueue.lib.config import BaseConfig

class Configuration(BaseConfig):
   REDIS_SERVER_INFO = {
      'host'     : 'localhost',
      'port'     : 6379,
      'db'       : 0,
   }

def success_function(data):
    return data

def failure_function(data):
    import time
    return time.sleep(one)