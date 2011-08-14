# -*- coding: utf-8 -*-

try:
    import json
except ImportError:
    import simplejson as json

import uuid

class Task(object):

    def __init__(self, data = None, queue_name = None):
        self.id         = uuid.uuid4()
        self.data       = data
        self.queue_name = queue_name

    def toJson(self):
        return json.dumps({
            'id'         : str(self.id),
            'data'       : self.data,
            'queue_name' : self.queue_name,
        })

    def getFromJson(self, json_data):
        entity    = json.loads(json_data)
        self.id   = entity.get("id")
        self.data = entity.get("data")

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
        return self.id

    def get_data(self):
        return self.data

    def get_queue_name(self):
        return self.queue_name
