#!/usr/bin/env bash

powerTV=$(echo 'pow 0' | cec-client -s -d 1)
echo "$powerTV"

if [[ "$powerTV" == *"standby"* ]]; then
	echo 'on 0' | cec-client -s -d 1
	echo 'as' | cec-client -s -d 1
else
	echo 'as' | cec-client -s -d 1
fi

#exec $SHELL
