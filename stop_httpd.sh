#!/bin/sh

period=10

if [ $# -gt 0 ]
then
	period=$1
fi

echo "Stops apache2 httpd for $period seconds!"
sudo service apache2 stop
sleep $period
sudo service apache2 start
echo "Starts apache2 httpd again after it has been stopped for $period seconds!"
