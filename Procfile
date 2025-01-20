release: python shoppinglist/manage.py migrate
web: gunicorn --pythonpath shoppinglist shoppinglist.wsgi --log-file -
