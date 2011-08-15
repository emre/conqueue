
from task import Task

class Client(object):

    def __init__(self):
        self.redis_connection  = None

    def set_redis_connection(self, redis_connection):
        self.redis_connection = redis_connection

    def get_redis_connection(self):
        return self.redis_connection

    def add_task(self, queue, data):
        queue = self.config.PREFIX + ':' + queue
        task  = Task(data, queue)
        self.get_redis_connection().rpush(task.get_queue_name(), task.toJson())

        return True


    def set_config(self, config):
        self.config     = config

        return self
