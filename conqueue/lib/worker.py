import multiprocessing
import logging

try:
    import json
except ImportError:
    import simplejson as json

from task import Task
from exceptions import ConqueueException

def _execute_task(task, function):
    logging.debug('<Task-%s> started.' % task.id)

    try:
        function(task.data)
        logging.debug('<Task-%s> finished with result: %s' % (task.id, task.data))
    except Exception, error:
        logging.error(error)
        Worker.requeue(task)

class Worker(object):

    def __init__(self, queue_name):
        self.queue_name  = queue_name
        self.worker_pool = None

    def set_redis_connection(self, redis_connection):
        self.redis_connection = redis_connection

        return self

    def set_config(self, config):
        self.config = config

        if self.config.USE_MULTI_PROCESSING:
            self.worker_pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())

        self.queue_name = self.config.PREFIX + ':' + self.queue_name

        return self

    def __repr__(self):
        return "<Worker: %s>" % self.queue_name

    def listen_tasks(self, function, blocking_pop = False):
        logging.debug('worker started, listening: %s' % self.queue_name)
        while True:
            for task in self._task_generator(blocking_pop):
                if self.config.USE_MULTI_PROCESSING:
                    self.worker_pool.apply_async(_execute_task, (task, function))
                else:
                    _execute_task(task, function)

    @staticmethod
    def requeue(task):
        pass

    def _task_generator(self, blocking_pop = False):
        try:
            while True:
                task_data = self._get_from_queue(blocking_pop)
                if task_data is None:
                    break
                task_data = Task().getFromJson(task_data)
                yield task_data
        except KeyboardInterrupt:
            raise ConqueueException('%s exited.' % self.__repr__())

    def _get_from_queue(self, blocking_pop = False):
        if blocking_pop:
            task_data = self.redis_connection.blpop(self.queue_name)
        else:
            task_data = self.redis_connection.lpop(self.queue_name)

        return task_data
