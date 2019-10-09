#!/bin/bash

apt install -y build-essential libssl-dev libffi-dev python3-dev libatlas-base-dev supervisor libapache2-mod-wsgi-py3 libapache2-mod-proxy-html libxml2-dev

a2enmod proxy
a2enmod proxy_http
a2enmod proxy_balancer
a2enmod lbmethod_byrequests
a2enmod headers
a2enmod rewrite
a2enmod ssl

service apache2 start