#!/bin/bash

virtualenv env -p python3
. env/bin/activate
pip install flask
pip install flask-cors
pip install unidecode
pip install pandas
pip install redis
redis-server &
export FLASK_ENV=development
export FLASK_APP=main.py;
flask run --host localhost;
