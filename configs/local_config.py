from .config import BasicConfig


class LocalConfig(BasicConfig):
    LOG_PATH = 'local_logs'
    MONGO_USER = 'rayest'
    MONGO_PASSWORD = '000000'
    MQ_HOST = '127.0.0.1'
    MQ_PORT = '5672'
    MQ_USER = 'rayest'
    MQ_PASSWORD = '000000'
    pass
