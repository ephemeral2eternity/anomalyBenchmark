#!/bin/sh

period=10
bw=1024

if [ $# -gt 0 ]
then
	period=$1
fi

if [ $# -gt 1 ]
then
	bw=$2
fi

echo "Starts throttling inbound bandwidth to $bw Kbps!"
sudo wondershaper eth0 $bw inbound
sleep $period
echo "Finishes inbound bandwidth throttling for $period seconds!"
sudo wondershaper eth0 10485760 10485760 
