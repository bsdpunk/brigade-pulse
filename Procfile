web: gunicorn wsgi --log-file -
worker: celery worker --app=settings.celery.app
beat: celery beat --app=settings.celery.app