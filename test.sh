#!/bin/bash

# script to repeatedly run AI vs Random and display total score

if [ $# -lt 1 ]; then
	echo "usage: ./test.sh <mode>"
	exit
fi

my_total=0
opp_total=0
option=$1
while :; do
	output=$(python simulator.py $option | tail -n 2)
	my_score=$(echo $output | awk '{ print $4 }')
	opp_score=$(echo $output | awk '{ print $8 }')
	my_total=$((my_total + my_score))
	opp_total=$((opp_total + opp_score))
	echo $my_total $opp_total
done
