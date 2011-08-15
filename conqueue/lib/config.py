
class BaseConfig(object):
    REDIS_SERVER_INFO = {
        'host'     : None,
        'port'     : None,
        'db'       : None,
    }

    USE_MULTI_PROCESSING = True
    POOLSIZE_PER_WORKER  = None
    PREFIX               = 'conqueue'
    RETRY_BEHAVIOUR      = (True, 100)


