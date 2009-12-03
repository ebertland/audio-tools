#!/bin/sh

cat "$1" | tr '\n' '\0' |\
  xargs -0 -n 1 -t $(dirname $0)/flac2mp3 2>&1 | tee -i "$2"
