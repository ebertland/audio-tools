#!/bin/sh

######################################
#	Usage:		verifycd CDROM_DEVICE ISO_IMAGE
# 	example:	verifycd /dev/cdrom image.iso
#
# References: http://www.troubleshooters.com/linux/coasterless.htm
#   http://howto.wikia.com/wiki/Howto_verify_a_burned_CD_or_DVD_image_on_Linux


# Inputs
DEVICE=$1
IMAGE_FILE=$2

# temp files
MD5SUM_ISO='md5sum-file.txt'
MD5SUM_CD='md5sum-cdrom.txt'

# Checking cd's blocksize and count
echo "Checking CD's block size, and count..."
blocksize=`isoinfo -d -i $DEVICE | grep "^Logical block size is:" | cut -d " " -f 5`
if test "$blocksize" = ""; then
	echo catdevice FATAL ERROR: Blank blocksize >&2
	exit
fi

blockcount=`isoinfo -d -i $DEVICE | grep "^Volume size is:" | cut -d " " -f 4`
if test "$blockcount" = ""; then
	echo catdevice FATAL ERROR: Blank blockcount >&2
	exit
fi

echo "block size: $blocksize"
echo "block count: $blockcount"

#Command for reading disk
raw_read_command="dd if=$DEVICE bs=$blocksize count=$blockcount conv=notrunc,noerror"

#Getting checksums
echo "Reading CD and creating check sum..."
$raw_read_command | md5sum > $MD5SUM_CD
echo "Reading ISO and creating check sum..."
md5sum $IMAGE_FILE > $MD5SUM_ISO

# Comparing md5 checksums
echo "Comparing check sums..."
cat $MD5SUM_ISO | while read CODE NAME; do
     if [ -n "`cat $MD5SUM_CD | grep $CODE`" ]; then
          echo "Success: $NAME"
     else
          echo "Failure: $NAME"
     fi
done

#Cleaning up
rm -f $MD5SUM_CD $MD5SUM_ISO 
