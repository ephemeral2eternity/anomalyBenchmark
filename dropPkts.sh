#!/bin/sh

period=30
percent="25%"

if [ $# -gt 0 ]
then
	period=$1
fi

if [ $# -gt 1 ]
then
	percent=$2
fi

echo "Starts dropping $percent packets for $period seconds!"
sudo tc qdisc add dev eth0 root netem loss ${percent}
sleep $period
echo "Finishes injecting anomalies!"
sudo tc qdisc del dev eth0 root
