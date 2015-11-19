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

echo "Starts throttling outbound bandwidth to $bw Kbps!"
sudo wondershaper eth0 10485760 $bw
sleep $period
echo "Finishes outbound bandwidth throttling for $period seconds!"
sudo wondershaper eth0 10485760 10485760 
