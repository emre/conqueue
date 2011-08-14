# -*- coding: utf-8 -*-

from conqueue.conqueue import Conqueue
from conqueue.lib import config

class Configuration(config.BaseConfig):
	REDIS_SERVER_INFO = {
		'host'     : 'localhost',
		'port'     : 6379,
		'db'       : 0,
	}


client  = Conqueue(Configuration, 'feeds').client()
client.add_task('http://news.ycombinator.com/rss')
