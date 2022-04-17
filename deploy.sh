#!/bin/bash
echo "Running deploy script"

echo "Installing virtual environment"
pip3 install virtualenv -q -q -q

DIR="env"
if [ ! -d "$DIR" ]; then
    echo "Creating virtual environment"
    virtualenv env -q

    source env/bin/activate
    cd src/

    echo "Installing requirments"
    pip3 install -r requirements.txt
fi

source env/bin/activate
cd src/

echo "Starting the server"
gunicorn --workers 1 --bind 127.0.0.1:5000 wsgi:app