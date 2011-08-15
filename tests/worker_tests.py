# -*- coding: utf-8 -*-

import unittest

from conqueue.conqueue import Conqueue
from conqueue.lib.exceptions import ConqueueEmptyException
from base import Configuration, success_function, failure_function

Configuration.USE_MULTI_PROCESSING = False

class TestWorkerFunctions(unittest.TestCase):

    def setUp(self):
        self.worker = Conqueue(Configuration).worker()
        self.client = Conqueue(Configuration).client()

    def test_register_task(self):
        self.worker.register_task('feeds', success_function)
        self.assertEqual([{"queue": "conqueue:feeds", "function": success_function}], self.worker.registered_tasks)

    def test_process_task(self):
        self.client.add_task('feeds', 'http://www.reddit.com/.rss')
        self.worker.register_task('feeds', success_function)
        self.assertRaises(ConqueueEmptyException, self.worker.listen_tasks, True)

    def test_process_multi_queue(self):
        self.client.add_task('feeds', 'http://www.reddit.com/.rss')
        self.client.add_task('messages', 'hi!')
        self.worker.register_task('feeds', success_function)
        self.worker.register_task('messages', success_function)
        self.assertRaises(ConqueueEmptyException, self.worker.listen_tasks, True)

    def test_queue_empty(self):
        self.worker.register_task('feeds', success_function)
        self.assertRaises(ConqueueEmptyException, self.worker.listen_tasks, True)

    def test_failure_task(self):
        self.client.add_task('feeds', 'http://www.reddit.com/.rss')
        self.worker.register_task('feeds', failure_function)
        self.assertRaises(ConqueueEmptyException, self.worker.listen_tasks, True)
        assert self.worker.redis_connection.llen('%s:feeds:failed' % self.worker.config.PREFIX) > 0

    def test_clear_failed_tasks(self):
        self.worker.register_task('feeds', success_function)
        self.assertRaises(ConqueueEmptyException, self.worker.listen_tasks, True)

if __name__ == '__main__':
    unittest.main()