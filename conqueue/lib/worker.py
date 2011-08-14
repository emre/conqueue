import multiprocessing
import logging

try:
    import json
except ImportError:
    import simplejson as json

from task import Task
from exceptions import ConqueueException

def _execute_task(task, function):
    """
    simple wrapper for the worker function.
    @todo: add time tracking
    """
    logging.debug('<Task-%s> started.' % task.get_id())
    try:
        function(task.get_data())
        logging.debug('<Task-%s> finished with result: %s' % (task.get_id(), task.get_data()))
    except Exception, error:
        logging.error(error)
        Worker.mark_as_failed(task)

class Worker(object):
    """
    base worker object.
        listens and executes jobs in a infinite loop based on it's queue name.
    """
    def __init__(self, queue_name):
        self.queue_name  = queue_name
        self.worker_pool = None

    def set_redis_connection(self, redis_connection):
        self.redis_connection = redis_connection

        return self

    def set_config(self, config):
        self.config = config

        if self.config.USE_MULTI_PROCESSING:
            # if USE_MULTI_PROCESSING set True in the configuration object,
            # worker forks itself by count based on cpu count.
            self.worker_pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())

        self.queue_name = self.config.PREFIX + ':' + self.queue_name

        return self

    def __repr__(self):
        return "<Worker: %s>" % self.queue_name

    def listen_tasks(self, function):
        logging.debug('worker started, listening: %s' % self.queue_name)
        while True:
            for task in self._task_generator():
                if self.config.USE_MULTI_PROCESSING:
                    self.worker_pool.apply_async(_execute_task, (task, function))
                else:
                    _execute_task(task, function)

    @staticmethod
    def mark_as_failed(task):
        pass

    def _task_generator(self):
        try:
            while True:
                task_data = self.redis_connection.lpop(self.queue_name)
                if task_data is None:
                    break
                task_data = Task().getFromJson(task_data)
                yield task_data
        except KeyboardInterrupt:
            raise ConqueueException('%s exited.' % self.__repr__())

