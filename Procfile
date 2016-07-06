web: gunicorn wsgi --log-file -
worker: celery worker --app=settings.celery_settings.app
beat: celery beat --app=settings.celery_settings.app