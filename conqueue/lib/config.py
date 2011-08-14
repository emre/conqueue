
class BaseConfig(object):
    REDIS_SERVER_INFO = {
        'host'     : None,
        'port'     : None,
        'db'       : None,
    }

    USE_MULTI_PROCESSING = True
    PREFIX               = 'conqueue'
    RETRY_BEHAVIOUR      = (True, 100)


