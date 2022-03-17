#!/bin/bash
echo "Running deploy script"

echo "Installing virtual environment"
pip3 install virtualenv -q -q -q

echo "Creating virtual environment"
virtualenv env -q
source env/bin/activate

echo "Installing requirments"
cd src
pip3 install -r requirements.txt

echo "Starting the server"
gunicorn --workers 1 --bind 127.0.0.1:5000 wsgi:app