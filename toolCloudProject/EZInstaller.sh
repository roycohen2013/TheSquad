#!/bin/bash

echo "This script is the easy installer for ToolCloud, brought to you by the squad."
echo "This script will fail if it is not run using administrator privileges."

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

if [ -f /usr/local/bin/python3 ] && [ -f /usr/bin/python3 ]; then
    echo "Python3 is not installed.  Please install python3 and come back."
    exit 1
fi
echo "Python3 verified."
python3 -c 'import django' | grep "No module" &> /dev/null

if [ $? == 0 ]; then
    echo "Django is not installed.  Please install django and try again."
    exit 1
fi

echo "Django verified.\n"

echo "Starting installation!\n"
mkdir /usr/local/TheSquad

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cp -r $DIR/* /usr/local/TheSquad

SCRIPT="#!/bin/bash \n python3 /usr/local/TheSquad/manage.py \$@"
touch /usr/local/bin/ToolCloud
echo "$SCRIPT" > /usr/local/bin/ToolCloud
chmod +x /usr/local/bin/ToolCloud

echo "Starting newSlate database preparation!\n"
cd /usr/local/TheSquad
python3 /usr/local/TheSquad/newSlate.py >> /dev/null

echo "Done!  Enjoy sharing all your hammers, screwdrivers, hoes, etc!"
echo "Run the server with 'ToolCloud runserver' !  Note that it must be run as root!"
exit 0
