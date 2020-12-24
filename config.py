from redisconfig import RedisConfig as RCG


class BaseConfig:
    broker_url = f'redis://{RCG.HOST}:{RCG.PORT}/{RCG.DB_SELERY}'
    result_backend = f'redis://{RCG.HOST}:{RCG.PORT}/{RCG.DB_SELERY}'
    accept_content = ['application/json']
    result_serializer = 'json'
    task_serializer = 'json'


class DevConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
