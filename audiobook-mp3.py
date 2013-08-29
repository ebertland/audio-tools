#!/usr/bin/python -tt

import glob
import os
import sys
import time
import tempfile
from multiprocessing import Process, active_children
import dbus

DRYRUN = False
CDROM_DEVICE = '/dev/disk/by-id/ata-TSSTcorp_CDDVDW_SH-S223L_Q9896GCZ314625'
#CDPARANOIA = 'nice -n 5 cdparanoia'
#CDPARANOIA = 'nice -n 5 cdparanoia -Y'
CDPARANOIA = 'nice -n 5 cdparanoia -Z'
LAME = 'nice -n 10 lame'
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

class Cd_device(object):
    def __init__(self, cdrom_device_path):
        self._cdrom_device_path = cdrom_device_path
        
        bus = dbus.SystemBus()
        udisks = bus.get_object(
            "org.freedesktop.UDisks", 
            "/org/freedesktop/UDisks")
        self._cd_dbus_obj = bus.get_object(
            "org.freedesktop.UDisks", 
            udisks.FindDeviceByDeviceFile(CDROM_DEVICE))
    
    def wait_for_media(self):
        while not self._cd_dbus_obj.Get('', 'DeviceIsMediaAvailable'):
            time.sleep(1.0)

    def eject(self):
        self._cd_dbus_obj.DriveEject(
            '', 
            dbus_interface='org.freedesktop.UDisks.Device')
        #XXX Needed?
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
    
    cd_dev = Cd_device(CDROM_DEVICE)

    num_discs = int(num_discs)
    for i in range(num_discs):
        disc_num = '%02d' % (i + 1)
        mkdir_and_chdir('d' + disc_num)
        print('Insert Disc %s.' % (disc_num))
        cd_dev.wait_for_media()
        rip_cd()
        encoder = Process(
            target=encode_all_wav, args=(disc_num, artist, album, year))
        encoder.start()
        os.chdir('..')
        
        cd_dev.eject()
        
    # Wait for child processes to complete.
    wait_all()
    
if __name__ == '__main__':
    main()
