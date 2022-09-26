try:
    from flask import Flask
    from celery import Celery
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
app.config['CELERY_TIMEZONE'] = 'UTC'
celery_app = make_celery(app)

@celery_app.task(name='fiveseconds')
def fiveseconds():
    print ('fiveseconds')

@celery_app.task
def tenseconds():
    print ('tenseconds')

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

@celery_app.task
def test(arg):
    print(arg)
