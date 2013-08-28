#!/bin/bash

while true; do
    if [ "$(udisks --show-info $1 | grep has\ media | awk '{print $3}')" -ne 0 ]; then
	exit 0
    fi
    sleep 1
done
