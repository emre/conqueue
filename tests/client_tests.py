# -*- coding: utf-8 -*-

import unittest
import random

from conqueue.conqueue import Conqueue
from conqueue.lib.exceptions import ConqueueBadQueueNameException
from base import Configuration, success_function, failure_function

class TestClientFunctions(unittest.TestCase):

    def setUp(self):
        self.worker = Conqueue(Configuration).worker()
        self.client = Conqueue(Configuration).client()

    def test_add_valid_task(self):
        task_name = str(random.random())
        self.assertEqual(True, self.client.add_task(task_name, 'data'))
        assert self.client.redis_connection.llen(self.client.config.PREFIX + ":" + task_name) > 0

    def test_add_invalid_task(self):
        task_name = str(random.random())
        self.assertRaises(ConqueueBadQueueNameException, self.client.add_task, '*-*', 'data')
        assert self.client.redis_connection.llen(self.client.config.PREFIX + ":" + task_name) == 0


if __name__ == '__main__':
    unittest.main()