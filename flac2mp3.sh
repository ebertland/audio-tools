#!/bin/sh

set -e
set -x

in_fn=$1
out_fn=${in_fn%.*}.mp3

flac -c -d "$in_fn" | lame -h -f --preset extreme - "$out_fn"
copy-tags "$in_fn" "$out_fn"
