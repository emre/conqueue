
class BaseConfig(object):
    REDIS_SERVER_INFO = {
        'host'     : None,
        'port'     : None,
        'db'       : None,
    }

    SERIALIZER           = 'JsonSerializer'
    LOG_LEVEL            = 'ERROR'
    USE_MULTI_PROCESSING = True
    PREFIX               = 'conqueue'
    LOG_FILENAME         = '/var/log/conqueue/conqueue.log'


