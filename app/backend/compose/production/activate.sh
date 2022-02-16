#!/bin/bash

cd mydarknet
make clean
make
cd ..
python3 manage.py migrate
python3 manage.py collectstatic --no-input

exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 counting_vertebrae.wsgi:application
