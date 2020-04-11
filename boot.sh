#!/bin/sh
source venv/bin/activate
flask db upgrade
python app/util/create_user.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - homedash:app