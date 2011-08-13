
from task import Task

class Client(object):

    def __init__(self, queue_name):
        self.queue_name        = queue_name
        self.redis_connection  = None

    def set_redis_connection(self, redis_connection):
        self.redis_connection = redis_connection

    def get_redis_connection(self):
        return self.redis_connection

    def add_task(self, data):
        task = Task(data)
        self.get_redis_connection().rpush(self.queue_name, task.toJson())

    def set_config(self, config):
        self.config     = config
        self.queue_name = self.config.PREFIX + ':' + self.queue_name

        return self
