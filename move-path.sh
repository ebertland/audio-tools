#!/bin/sh
# $Id$
#
# move-path <src file path> <dest root dir>
#

src_file_path="$1"
dst_root_dir="$2"

src_subtree_path=$(dirname "$src_file_path")
dst_dir="$dst_root_dir"/"$src_subtree_path"

mkdir -p "$dst_dir"
mv "$src_file_path" "$dst_dir"

