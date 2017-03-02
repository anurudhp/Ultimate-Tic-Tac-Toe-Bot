#!/bin/bash

# script to repeatedly run AI vs Random and display total score

function pad() {
	if [ $1 -lt 10 ]; then
		echo 0$1
	else
		echo $1
	fi
}

function div() {
	num=$1
	den=$2
	if [ $num -lt 0 ]; then
		num=$((-num))
		echo -n '-'
	fi
	echo $((num/den)).$(pad $((((100*num)/den)%100)))
}

if [ $# -lt 1 ]; then
	echo "usage: ./test.sh <option>"
	exit
fi

my_total=0
opp_total=0
games=0

while :; do
	output=$(python simulator.py $@ | tail -n 4)
	result_message=$(echo $output | awk '{ print $2 }')
	my_score=$(echo $output | awk '{ print $12 }')
	opp_score=$(echo $output | awk '{ print $16 }')
	my_total=$((my_total + my_score))
	opp_total=$((opp_total + opp_score))
	games=$((games + 1))
	diff=$((my_total - opp_total))
	echo -e "$my_total - $opp_total | $games games | average: $(div $my_total $games) - $(div $opp_total $games) | diff: $(div $diff $games) [$@] ($my_score - $opp_score) {$result_message}"
done
