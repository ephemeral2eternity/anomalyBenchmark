#!/bin/sh

period=300
bw=100Kbps
ipPrefix=131.179.150.0/24

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
	bw=$3
fi

echo "Starts throttling bandwidth to $bw for all packets from $ipPrefix for $period seconds!"
sudo tc qdisc add dev eth0 root handle 1: htb
sudo tc class add dev eth0 parent 1:1 classid 1:11 htb rate 100Kbps
sudo tc filter add dev eth0 protocol ip prio 1 u32 match ip dst 131.179.150.0/24 flowid 1:11
echo "Show the added rules"
sudo tc -s -d qdisc ls
sleep $period
echo "Finishes injecting anomalies!"
sudo tc qdisc del dev eth0 root
