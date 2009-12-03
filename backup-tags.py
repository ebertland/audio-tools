#!/usr/bin/env python

import sys
import os
from stat import *
import os.path as path
import pickle

import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

import quodlibet.config
import quodlibet.formats
quodlibet.config.init()
MusicFile = quodlibet.formats.MusicFile

def clear_tags(metadata):
    for tag in metadata.realkeys():
        del metadata[tag]

def get_file_mode(fn):
    return S_IMODE(os.stat(fn).st_mode)

def chmod_read_only(fn):
    current_mode = get_file_mode(fn)
    new_mode = current_mode & (~(S_IWUSR | S_IWGRP | S_IWOTH))
    os.chmod(fn, new_mode)

def backup_tags(fn):
    metadata = MusicFile(fn)
    
    backup_fn = fn + '.tags'
    with open(backup_fn, 'w') as backup:
        pickle.dump(dict(metadata), backup)
    chmod_read_only(backup_fn)

def restore_tags(fn):
    backup_fn = fn + '.tags'
    with open(backup_fn, 'r') as backup:
        saved_tags = pickle.load(backup)
    
    metadata = MusicFile(fn)
    clear_tags(metadata)
    metadata.update(saved_tags)
    metadata.write()

def main(argv):
    restore_mode = False
    app_name = path.basename(argv[0])
    if app_name.startswith('restore'):
        restore_mode = True

    if len(argv) == 1:
        print "Usage: {0} <audio file>+\n".format(app_name)
        sys.exit(0)
    
    for fn in argv[1:]:
        if restore_mode:
            restore_tags(fn)
        else:
            backup_tags(fn)


if __name__ == '__main__':
    main(sys.argv)

