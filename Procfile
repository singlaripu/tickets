web: gunicorn Tickets.wsgi --log-file -
worker: celery -A Tickets worker -B -E --loglevel=info