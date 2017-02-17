#!/bin/bash

# script to repeatedly run AI vs Random and display total score

function div() {
	num=$1
	den=$2
	echo $((num/den)).$((((100*num)/den)%100))
}

my_total=0
opp_total=0
games=0

while :; do
	output=$(python simulator.py $@ | tail -n 2)
	my_score=$(echo $output | awk '{ print $4 }')
	opp_score=$(echo $output | awk '{ print $8 }')
	my_total=$((my_total + my_score))
	opp_total=$((opp_total + opp_score))
	games=$((games + 1))
	echo -e "$my_total - $opp_total | ($games games, average: $(div $my_total $games) - $(div $opp_total $games)) [$@]"
done

