#!/bin/bash

# Flatten multi-disk albums.

declare OUTPUT_DIR
declare ALBUM_TITLE

function usage() {
    echo "Usage: $0 -t album_title -o output_directory DIRECTORY..."
}

while getopts "t:o:h" OPTION; do
    case $OPTION in
        t)
            ALBUM_TITLE="${OPTARG}"
            ;;
        o)
            OUTPUT_DIR="${OPTARG}"
            ;;
        h)
            usage
            exit 1
            ;;
        \?)
            usage
            exit 1
            ;;
    esac
done
shift $(($OPTIND-1))

function required() {
    if [[ -z "$1" ]]; then
        usage
        exit 1
    fi
}

function confirm() {
    echo ${@} "[Y/n]"
    read CONFIRM_INPUT
    CONFIRM_INPUT=$(echo ${CONFIRM_INPUT} | tr '[:lower:]' '[:upper:]')
    if [[ ( ${CONFIRM_INPUT} != "Y" ) && ( -n ${CONFIRM_INPUT} ) ]]; then
        echo "Aborting."
        exit
    fi
}


required "${ALBUM_TITLE}"
required "${OUTPUT_DIR}"

echo "Album title: ${ALBUM_TITLE}"
echo "Output directory: ${OUTPUT_DIR}"

mkdir -p "${OUTPUT_DIR}"

I=1
for a in "${@}"; do
    echo "${I}    ${a}"
    I=$((${I} + 1))
done

confirm "Confirm order:"

CD=1
TRACK=1
for D in "${@}"; do
    for F in "${D}"/*.mp3; do
        NEW_NAME=$(printf "Track %03d\n" ${TRACK})
        NEW_FILENAME="${OUTPUT_DIR}/${NEW_NAME}.mp3"
        echo "${F} → ${NEW_FILENAME}"

        cp "${F}" "${NEW_FILENAME}"
        id3v2 -A "${ALBUM_TITLE}" -t "${NEW_NAME}" -T "${TRACK}" "${NEW_FILENAME}"
        TRACK=$((${TRACK} + 1))
    done
done
