# -*- coding: utf-8 -*-

try:
    import json
except ImportError:
    import simplejson as json

import uuid

class Task(object):

    def __init__(self, data = None, queue_name = None):
        self.id          = uuid.uuid4()
        self.data        = data
        self.queue_name  = queue_name
        self.retry_count = 0

    def toJson(self):
        return json.dumps({
            'id'         : self.get_id(),
            'data'       : self.get_data(),
            'queue_name' : self.get_queue_name(),
            'retry_count': self.get_retry_count(),
        })

    def getFromJson(self, json_data):
        entity           = json.loads(json_data)
        self.id          = entity.get("id")
        self.data        = entity.get("data")
        self.queue_name  = entity.get("queue_name")
        self.retry_count = entity.get("retry_count")

        return self

    def set_id(self, value):
        self.id = value

        return self

    def set_data(self, value):
        self.data = value

        return self

    def set_queue_name(self, value):
        self.queue_name = value

        return self

    def get_id(self):
        return str(self.id)

    def get_data(self):
        return self.data

    def get_queue_name(self):
        return self.queue_name

    def get_retry_count(self):
        return self.retry_count

    def set_retry_count(self, value):
        self.retry_count = value

        return self

    @property
    def is_failed(self):
        if self.queue_name.find('failed') < 0:
            return False
        return True

    def increment_retry_count(self):
        self.retry_count += 1

        return self

    def __repr__(self):
        return "<Task-%s-%s>" % (self.get_id(), self.get_queue_name())
