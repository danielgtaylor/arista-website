#!/bin/bash

#
# Initialize Arista Website
#

git submodule init
git submodule update

if [ -f arista.db ]; then
    rm arista.db
fi

cp settings.py.default settings.py
./manage.py syncdb --noinput
./manage.py presetcache

echo
echo 'Arista website is ready for development, please run:'
echo './manage.py runserver [HOST[:PORT]]'
echo

