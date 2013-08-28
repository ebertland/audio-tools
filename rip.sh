#!/bin/bash

DEV_CDROM=$(grep CDROM= $HOME/.abcde.conf | cut -d= -f2)

for i in {1..1000}; do
    DIR=$(printf "Disc %02d\n" $i)
    echo "Ripping: " $DIR
    wait-cd ${DEV_CDROM}
    mkdir "$DIR" && EJECTCD=y OUTPUTDIR="${DIR}" abcde -N -n
done
