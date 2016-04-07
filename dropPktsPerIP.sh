#!/bin/sh

period=30
percent="25%"
ipPrefix="128.2.57.0/24"

if [ $# -gt 0 ]
then
	period=$1
fi

if [ $# -gt 1 ]
then
	ipPrefix=$2
fi

if [ $# -gt 2 ]
then
	percent=$3
fi

echo "Clear previous filters!"
sudo tc qdisc del dev eth0 root
echo "Starts dropping ${percent} packets for $period seconds in flows to ${ipPrefix}"
sudo tc qdisc add dev eth0 root handle 1: htb
sudo tc class add dev eth0 parent 1:1 classid 1:11 htb rate 1000Mbps
sudo tc qdisc add dev eth0 parent 1:11 handle 10: netem loss ${percent}
sudo tc filter add dev eth0 protocol ip prio 1 u32 match ip dst ${ipPrefix} flowid 1:11
sleep $period
echo "Finishes injecting anomalies!"
sudo tc qdisc del dev eth0 root
