import multiprocessing
import logging

try:
    import json
except ImportError:
    import simplejson as json

import time

from task import Task
from exceptions import ConqueueException

def _execute_task(task, function, config):
    """
    simple wrapper for the worker function.
    """
    logging.debug('<Task-%s> started.' % task.get_id())
    start_time = time.time()
    try:
        function(task.get_data())
        logging.debug('<Task-%s> finished in %2.2f seconds with result: %s' % (task.get_id(),
                                                                            time.time() - start_time,
                                                                            task.get_data()))
        return {
            "status": True,
            "task": task
        }
    except Exception, error:
        logging.error(error)
        return {
            "status": False,
            "task": task
        }

class Worker(object):
    """
    base worker object.
        listens and executes jobs in a infinite loop based on it's queue name.
    """

    def __init__(self, queue_name):
        self.queue_name       = queue_name
        self.worker_pool      = None
        self.redis_connection = None

    def set_redis_connection(self, redis_connection):
        self.redis_connection = redis_connection

        return self

    def get_redis_connection(self):
        return self.redis_connection

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

    def listen_tasks(self, function, queue = None):
        if not queue:
            queue = self.queue_name
        logging.info('worker started, listening: %s' % queue)
        while True:
            for task in self._task_generator(queue):
                if self.config.USE_MULTI_PROCESSING:
                    self.worker_pool.apply_async(_execute_task,
                                                (task, function, self.config, True),
                                                 callback = self.on_complete)
                else:
                    result = _execute_task(task, function, self.config)
                    self.on_complete(result)
            time.sleep(0.1)

    def on_complete(self, data):
        if not data.get("status"):
            if self.config.RETRY_BEHAVIOUR[0]:
                if data.get("task").get_retry_count() < self.config.RETRY_BEHAVIOUR[1]:
                    self.mark_as_failed(data.get("task"))

    def listen_failed_tasks(self, function):
        failed_queue = self.queue_name + ':failed'
        return self.listen_tasks(function, failed_queue)

    def mark_as_failed(self, task):
        task.increment_retry_count()
        logging.error('%s failed, adding data to failed queue.' % task)
        if not task.is_failed:
            failed_queue = task.get_queue_name() + ':failed'
        else:
            failed_queue = task.get_queue_name()

        self.get_redis_connection().rpush(failed_queue, task.toJson())


    def _task_generator(self, queue):
        try:
            while True:
                task_data = self.get_redis_connection().lpop(queue)
                if task_data is None:
                    break
                task_data = Task().getFromJson(task_data)
                yield task_data
        except KeyboardInterrupt:
            raise ConqueueException('%s exited.' % self.__repr__())

