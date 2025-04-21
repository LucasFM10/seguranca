release: python manage.py migrate
web: gunicorn dcrm.wsgi --pythonpath project --log-file=-
