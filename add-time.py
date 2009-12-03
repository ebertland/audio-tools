#!/usr/bin/python

import fileinput
import string

total = 0
for line in fileinput.input():
    label, time = string.split(line)
    min, sec = string.split(time, ':')
    total += int(min) * 60 + int(sec)

print 'Length: %d:%02d' %(total/60, total%60)
