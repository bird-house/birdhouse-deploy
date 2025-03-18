#!/bin/sh

################################################################
# Deletes old files as determined by the CLEAN_OLD_FILES_OPTIONS
# environment variable.
#
# This variable contains space delimited fields, each
# representing a group of files to be deleted.
# The format of these fields are as follows:
#
# <docker-volume-mounts>|<find-location>|<age-in-days>
#
# - docker-volume-mounts is not used by this script
# - find-location is an argument passed to `find` which will
#   recursively search for files to delete based on that argument
# - age-in-days is an integer that represents a number of days,
#   all files found by `find` that were modified more than this
#   number of days ago will be deleted
#
# Example call to delete all files in /tmp older than 20 days and
# all files in /var/log older than 90 days:
#
# $ export CLEAN_OLD_FILES_OPTIONS='xxx|/tmp|20 yyy|/var/log|90' 
# $ sh clean-old-files.sh
##################################################################


for opt in ${CLEAN_OLD_FILES_OPTIONS}; do
    loc="$(echo $opt | cut -d\| -f 2)"
    age="$(echo $opt | cut -d\| -f 3)"
    echo "Removing files in ${loc} that have not been modified in ${age} days"
    [ -n "$loc" ] && [ -n "$age" ] && find ${loc} -type f -mtime +"${age}" -print -delete
done
