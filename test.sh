#!/bin/bash

# script to repeatedly run AI vs Random and display total score

function div() {
	num=$1
	den=$2
	echo $((num/den)).$((((100*num)/den)%100))
}

if [ "$1" == "first" ]; then
	option=4
elif [ "$1" == "second" ]; then
	option=5
else
	echo "usage: ./test.sh <first|second>"
	exit
fi

my_total=0
opp_total=0
games=0

while :; do
	output=$(python simulator.py $option | tail -n 2)
	my_score=$(echo $output | awk '{ print $4 }')
	opp_score=$(echo $output | awk '{ print $8 }')
	my_total=$((my_total + my_score))
	opp_total=$((opp_total + opp_score))
	games=$((games + 1))
	echo -e "$my_total - $opp_total | ($games games, average: $(div $my_total $games) - $(div $opp_total $games)) [$1]"
done

