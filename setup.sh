#!/bin/sh

# Install virtualenv if it doesn't exist
if [ $(pip list | grep virtualenv | wc -l) -eq 0 ]
then
  pip install virtualenv
fi

# Create virtualenv with python3.7 interpreter if it doesn't exist
if [ ! -d "/path/to/dir" ]
then
  virtualenv -p python3.7 venv
fi

./venv/bin/pip install -r requirements.txt
./venv/bin/python main.py initdb
./venv/bin/python main.py migratedb
