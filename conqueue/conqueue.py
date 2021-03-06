# -*- coding: utf-8 -*-
import redis

from lib.worker import Worker
from lib.client import Client

class Conqueue(object):

    def __init__(self, config):
        self.config            = config
        self._redis_connection = None

    def client(self):
        client_instance = Client()
        client_instance.set_config(self.config)
        client_instance.set_redis_connection(self.get_redis_connection())

        return client_instance
    
    def worker(self):
        worker_instance = Worker()
        worker_instance.set_config(self.config)
        worker_instance.set_redis_connection(self.get_redis_connection())

        return worker_instance

    def get_redis_connection(self):
        if not self._redis_connection:
            self._redis_connection = redis.Redis(host = self.config.REDIS_SERVER_INFO['host'],
                                                 port = self.config.REDIS_SERVER_INFO['port'],
                                                 db   = self.config.REDIS_SERVER_INFO['db'])

        return self._redis_connection

    




