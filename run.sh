#!/bin/bash

sudo /etc/init.d/mysql start
sudo /etc/init.d/memcached start
sudo service nginx start
sudo /etc/init.d/sphinxsearch start

