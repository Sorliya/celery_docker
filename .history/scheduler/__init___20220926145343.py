try:
    from flask import Flask
    from celery import Celery
    from flask_crontab import Crontab
    from datetime import timedelta
    from celery.schedules import crontab
except Exception as e:
    print("Error : {} ".format(e))

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config['CELERY_BACKEND'] = "redis://redis:6379/0"
app.config['CELERY_BROKER_URL'] = "redis://redis:6379/0"

app.config['CELERYBEAT_SCHEDULE'] = {   
    'say-every-5-seconds': {
        'task': 'fiveseconds',
        'schedule': timedelta(seconds=5)
    },
    'say-every-10-seconds': {
        'task': 'tenseconds',
        'schedule': timedelta(seconds=10)
    }
}

app.config['CELERY_TIMEZONE'] = 'UTC'
celery_app = make_celery(app)

@celery_app.task(name='fiveseconds')
def fiveseconds():
    print ('fiveseconds')

@celery_app.task
def tenseconds():
    print ('tenseconds')

,
    'say-every-day-evening': {
        'task': 'twelve',
        'schedule': crontab(hour='14', minute='0')
    },
    'say-every-day-night': {
        'task': 'one',
        'schedule': crontab(hour='15', minute='0')
    },
    'say-every-monday-morning': {
        'task': 'monday',
        'schedule': crontab(hour='0', minute='30', day_of_week='7')
    }

@celery_app.task
def twelve():
    print ('twelve')

@celery_app.task
def one():
    print ('one')

@celery_app.task
def monday():
    print ('monday')