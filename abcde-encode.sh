#!/bin/sh

DIRS=`find . -type d -name 'abcde.*'`

for d in $DIRS; do
    status=`tail -1 $d/status`
    if [ "$status" == "encode-output=loud" ]; then
	echo '[[[[ Encoding '$d' ]]]]'
	discid=`cat $d/discid | awk '{print $1}'`
	abcde -C $discid -a encode,tag,move,clean
    else
	echo '[[[[ Skipping '$d' ]]]]'
    fi
done

