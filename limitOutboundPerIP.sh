#!/bin/sh

period=300
bw=100Kbps
ipPrefix=128.2.57.0/24

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

echo "Clear all existing filters!"
sudo tc qdisc del dev eth0 root
echo "Starts throttling bandwidth to $bw for all packets from $ipPrefix for $period seconds!"
sudo tc qdisc add dev eth0 root handle 1: htb
sudo tc class add dev eth0 parent 1:1 classid 1:11 htb rate $bw
sudo tc filter add dev eth0 protocol ip prio 1 u32 match ip dst $ipPrefix flowid 1:11
echo "Show the added rules"
sudo tc -s -d qdisc ls
sleep $period
echo "Finishes injecting anomalies!"
sudo tc qdisc del dev eth0 root
