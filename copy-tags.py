#!/usr/bin/env python

import sys
import os.path as path

import re
import UserDict
from warnings import warn

import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

import quodlibet.config
from quodlibet.formats import MusicFile
quodlibet.config.init()

class AudioFile(UserDict.DictMixin):
    """A simple class just for tag editing.

    No internal mutagen tags are exposed, or filenames or anything. So
    calling clear() won't destroy the filename field or things like
    that. Use it like a dict, then .write() it to commit the changes.

    Optional argument blacklist is a list of regexps matching
    non-transferrable tags. They will effectively be hidden, neither
    settable nor gettable.

    Or grab the actual underlying quodlibet format object from the
    .data field and get your hands dirty."""
    def __init__(self, filename, blacklist=()):
        self.data = MusicFile(filename)
        # Also exclude mutagen's internal tags
        self.blacklist = [ re.compile("^~") ] + blacklist
    def __getitem__(self, item):
        if self.blacklisted(item):
            warn("%s is a blacklisted key." % item)
        else:
            return self.data.__getitem__(item)
    def __setitem__(self, item, value):
        if self.blacklisted(item):
            warn("%s is a blacklisted key." % item)
        else:
            return self.data.__setitem__(item, value)
    def __delitem__(self, item):
        if self.blacklisted(item):
            warn("%s is a blacklisted key." % item)
        else:
            return self.data.__delitem__(item)
    def blacklisted(self, item):
        """Return True if tag is blacklisted.

        Blacklist automatically includes internal mutagen tags (those
        beginning with a tilde)."""
        for regex in self.blacklist:
            if re.search(regex, item):
                return True
        else:
            return False
    def keys(self):
        return [ key for key in self.data.keys() if not self.blacklisted(key) ]
    def write(self):
        return self.data.write()

# A list of regexps matching non-transferrable tags, like file format
# info and replaygain info. This will not be transferred from source,
# nor deleted from destination.
blacklist_regexes = [ re.compile(s) for s in (
        'encoded',
        'replaygain',
        ) ]

def copy_tags(src_fn, dst_fn):
    m_src = AudioFile(src_fn, blacklist=blacklist_regexes)
    m_dst = AudioFile(dst_fn, blacklist=blacklist_regexes)
    m_dst.clear()
    m_dst.update(m_src)
    m_dst.write()

def main(argv):
    app_name = path.basename(sys.argv[0])
    if len(argv) != 3:
        print "Usage: {0} <src audio file> <dst audio file>\n".format(app_name)
        sys.exit(0)
    
    copy_tags(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main(sys.argv)
