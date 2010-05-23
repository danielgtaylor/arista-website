#!/bin/bash

#
# Initialize Arista Website
#

if [ -f arista.db ]; then
    rm arista.db
fi

cp settings.py.default settings.py
./manage.py syncdb --noinput
#./manage.py loaddata fixtures/dev.json

echo
echo 'Arista website is ready for development, please run:'
echo './manage.py runserver [HOST[:PORT]]'
echo
