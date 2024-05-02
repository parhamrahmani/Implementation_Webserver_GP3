#!/usr/bin/env/bash
# script for setting up python environment and installing required packages
python3 -m venv ./flaskapp
source ./flaskapp/bin/activate
pip install flask flask-cors pymysql

