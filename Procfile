web: gunicorn alx_travel_app_0x03.wsgi:application --bind 0.0.0.0:$PORT --workers 2
worker: celery -A alx_travel_app_0x03 worker --loglevel=info --pool=solo