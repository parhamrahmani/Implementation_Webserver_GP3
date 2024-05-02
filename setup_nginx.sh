#!/usr/bin/env bash
# script for setting up the nginx server

# create file and populate it
touch /etc/nginx/sites-available/myflaskapp
echo "server {
    listen 80;
    server_name _;  # wildcard

    location / {
        proxy_pass http://127.0.0.1:5000;  # Point to where Flask is running
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}" > /etc/nginx/sites-available/myflaskapp

# link file
ln -s /etc/nginx/sites-available/myflaskapp /etc/nginx/sites-enabled

