from celery.schedules import crontab


CELERY_IMPORTS = ('src.tasks.units')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'daily-stuff': {
        'task': 'src.tasks.units.grab_coupons',
        # Every minute
        'schedule': crontab(hour="10", minute="25"),
    }
}
