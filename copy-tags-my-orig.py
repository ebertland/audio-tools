#!/usr/bin/env python

import sys

import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

import quodlibet.config
from quodlibet.formats import MusicFile
quodlibet.config.init()

def copy_tags(src_fn, dst_fn):
    src_metadata = MusicFile(src_fn)
    dst_metadata = MusicFile(dst_fn)
    for tag in src_metadata.realkeys():
        dst_metadata[tag] = src_metadata[tag]
    dst_metadata.write()

def main(argv):
    if len(argv) != 3:
        print "Usage: {0} <src audio file> <dst audio file>\n".format(app_name)
        sys.exit(0)
    
    copy_tags(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main(sys.argv)

