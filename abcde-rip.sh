#!/bin/sh

POLL_DELAY=60

while true; do
    if cdparanoia -Q -d /dev/cdrw >& /dev/null; then
	abcde -a cddb,read
    fi
    sleep ${POLL_DELAY}
done
