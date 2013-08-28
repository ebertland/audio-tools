#!/usr/bin/python -tt

import glob
import os
import sys
import time
import tempfile
from multiprocessing import Process, active_children

DRYRUN = False
CDROM_DEVICE = '/dev/dvdrw1'
#CDPARANOIA = 'nice -n 5 cdparanoia'
#CDPARANOIA = 'nice -n 5 cdparanoia -Y'
CDPARANOIA = 'nice -n 5 cdparanoia -Z'
LAME = 'nice -n 10 lame'
EJECT = 'eject'
RUN_IN_TERMINAL = ('gnome-terminal -t "%s" --disable-factory --zoom=0.5 '
                   '--hide-menubar -x')
                   
def sh(cmd, echo=True, dryrun=False):
    if isinstance(cmd, list) or isinstance(cmd, tuple):
        cmd = ' '.join(cmd)
    if echo:
        sys.stdout.write('# ' + cmd + '\n')
    if not dryrun:
        os.system(cmd)

def mkdir_and_chdir(d):
    try:
        os.mkdir(d)
    except OSError, e:
        if e.errno != os.errno.EEXIST:
            raise
    os.chdir(d)

def rip_cd():
    sh([CDPARANOIA, '-d', CDROM_DEVICE, '-B'])
    
def encode_all_wav(disc_num, artist, album, year, genre='Spoken Word'):
    # Make a script, and then run _that_ in a terminal. Less pop-ups.
    # This is such a hack. :-P
    script = tempfile.NamedTemporaryFile()
    
    for wav in sorted(glob.glob('*.wav')):
        track_num = wav.split('.')[0][5:7]
        #print wav, track_num
        
        cmd = []
        cmd.append(LAME)
        cmd.append('--preset fast medium --add-id3v2')
        cmd.append('--tt "%s - Disc%s Track%s"' %
                   (album, disc_num, track_num))
        cmd.append('--ta "%s" --tl "%s"' %
                   (artist, album))
        cmd.append('--ty "%s" --tn "%s" --tg "%s" ' %
                   (year, track_num, genre))
        cmd.append(wav)
        cmd.append('%s.%s.mp3' % (disc_num, track_num))
        
        script.write(' '.join(cmd) + '\n')
    
    script.flush()
    os.fsync(script.fileno())
    
    titlebar = 'lame: %s D%s' % (album, disc_num)
    sh([(RUN_IN_TERMINAL % (titlebar)), '/bin/sh', script.name])
    
    script.close()
    cleanup_wav()

def cleanup_wav():
    for wav in glob.glob('*.wav'):
        os.remove(wav)

def wait_all():
    while active_children():
        time.sleep(1.0)

def main():
    if len(sys.argv) == 1:
        artist = raw_input('Author: ')
        album = raw_input('Book: ')
        year = raw_input('Year: ')
        num_discs = raw_input('Number of Discs: ')
    else:
        assert len(sys.argv) == 5
        artist = sys.argv[1]
        album = sys.argv[2]
        year = sys.argv[3]
        num_discs = sys.argv[4]
        
        print('Author: ' + artist)
        print('Book: ' + album)
        print('Year: ' + year)
        print('Number of Discs: ' + num_discs)
    
    raw_input('If this looks good, please press enter to begin.')
    
    mkdir_and_chdir(artist)
    mkdir_and_chdir('%s (%s)' % (album, year))
    
    num_discs = int(num_discs)
    for i in range(num_discs):
        disc_num = '%02d' % (i + 1)
        mkdir_and_chdir('d' + disc_num)
        raw_input('Insert Disc %s and press the enter key to continue.' %
                  (disc_num))
        rip_cd()
        encoder = Process(
            target=encode_all_wav, args=(disc_num, artist, album, year))
        encoder.start()
        os.chdir('..')
        
        sh(['eject', CDROM_DEVICE])
        
    # Wait for child processes to complete.
    wait_all()
    
if __name__ == '__main__':
    main()
