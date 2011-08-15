
import re

from task import Task
from exceptions import ConqueueBadQueueNameException

class Client(object):

    def __init__(self):
        self.redis_connection  = None

    def set_redis_connection(self, redis_connection):
        self.redis_connection = redis_connection

    def get_redis_connection(self):
        return self.redis_connection

    def add_task(self, queue, data):
        queue = self._control_queue_name(queue)
        queue = self.config.PREFIX + ':' + queue
        task  = Task(data, queue)
        self.get_redis_connection().rpush(task.get_queue_name(), task.toJson())

        return True

    def _control_queue_name(self, value):
        if not isinstance(value, str):
            value = str(value)

        pattern = "[^a-zA-Z0-9_\-:]"
        if re.match(pattern, value):
            raise ConqueueBadQueueNameException('queue names must be in: %s', pattern)

        return value

    def set_config(self, config):
        self.config     = config

        return self
