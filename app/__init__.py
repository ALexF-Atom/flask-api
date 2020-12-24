import os
from celery import Celery
from flask import Flask
import redis

from redisconfig import RedisConfig as RSG
from .index import index


class RedisClient:
    def __init__(self, db, host=RSG.HOST, port=RSG.PORT):
        self.host = host
        self.port = port
        self.db = db

    def __enter__(self):
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db,
                                  encoding='utf-8')
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


blueprints = [index, ]


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevConfig')
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    return app


def make_celery(app=None):
    app = app or create_app()
    celery = Celery('app')
    celery.config_from_object('config.BaseConfig')
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
