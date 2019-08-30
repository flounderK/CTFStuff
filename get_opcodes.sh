#!/bin/bash

if [[ -z "$1" ]]
then
	exit
fi

objdump -d $1 | grep -Poi "^( )*\d+:\t+([0-9a-f ]+)" | cut -f2- | xargs
