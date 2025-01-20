release: python shoppinglist/manage.py migrate
web: gunicorn shoppinglist.wsgi:application --log-file -
