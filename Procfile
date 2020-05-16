release: python manage.py migrate && python manage.py collectstatic
web: gunicorn ctb.wsgi --log-file -
