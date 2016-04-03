#!/bin/sh

period=10
lat=1000

if [ $# -gt 0 ]
then
	period=$1
fi

if [ $# -gt 1 ]
then
	lat=$2
fi

echo "Starts adding delay $lat miliseconds to all packets for $period seconds!"
sudo tc qdisc add dev eth0 root netem delay ${lat}ms
sleep $period
echo "Finishes injecting anomalies!"
sudo tc qdisc del dev eth0 root
