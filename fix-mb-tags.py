#!/usr/bin/env python
# Copyright 2009 by Jeff Ebert
# License: GNU GPL v2

import sys
import mutagen.flac
import os.path as path

# Tip from:
# http://stackoverflow.com/questions/492483/setting-the-correct-encoding-when-piping-stdout-in-python
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def fix_mb_tags(flac_file):
    for tag in flac_file:
        if tag.startswith('musicbrainz_'):
            # The value of each tag is a list, so I must iterate even though
            # there is only 1 for these cases.
            values = flac_file[tag]
            for i in range(len(values)):
                # Extract UUID value from URL.
                base = path.basename(values[i])
                base = path.splitext(base)[0]
                values[i] = base
            flac_file[tag] = values


def main(argv):
    if len(argv) == 1:
        print "Usage: {0} <flac file>+\n".format(path.basename(argv[0]))
        sys.exit(0)

    for fn in argv[1:]:
        flac_file = mutagen.flac.Open(fn)
        fix_mb_tags(flac_file)
        print flac_file.pprint()
        flac_file.save()


if __name__ == '__main__':
    main(sys.argv)

