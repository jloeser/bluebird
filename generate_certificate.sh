#!/bin/bash
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
openssl genrsa 1024 > server.key
chmod 400 server.key
openssl req -new -x509 -nodes -sha1 -days 365 -key server.key > server.crt

