from celery.signals import worker_ready
import pyEX

from iexCloudConfig import iexCloudConfig as CCG
from redisconfig import RedisConfig as RCG

from app import make_celery
celery = make_celery()


@celery.task
def get_company(symbol):
    c = pyEX.Client(api_token=CCG.API_TOKEN, version=CCG.VERSION)
    return c.quote(symbol)


@worker_ready.connect
def api_data(*args, **kwargs):
    from app import RedisClient

    c = pyEX.Client(api_token=CCG.API_TOKEN, version=CCG.VERSION)
    results = c.symbolsDF()['name'].to_dict()

    with RedisClient(db=RCG.DB_DATA) as r:
        r.mset(results)
