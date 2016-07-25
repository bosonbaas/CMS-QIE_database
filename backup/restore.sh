#!/bin/bash

# restore.sh: This script restores the state of the card_db and media
#       folders from a given backup file.
# 
#   Ex: restore.sh daily_backup/2016-06-21_0100.tar.gz
#       This command restores the state of the database from
#       June 21, 2016 at 1:00 AM
#
# Author:   Andrew Baas
# Credits:  Jay Dittmann, Andrew Baas
# 
# Version:  1.01
# Maintainer:   Caleb Smith
# Email:    caleb_smith2@baylor.edu
# Status:   Live

scriptLoc=$(readlink -f $(dirname $0) )     # location of this script
commonPath=${scriptLoc%/*}                  # location of the common DB folder
dbName=card_db                              # location of the database folder
backupPath=$commonPath/backup               # location of backup files

mediaPath=$commonPath                       # location of the DB media folder

file=$1                         # backup file to restore from
filePath=$backupPath/$file      # complete path to the file
tempPath=$backupPath/temp_dir   # file to decompress backup into

extension=${file#*.}    # extension of the backup file

###################################################
#            Validate File Name                   #
###################################################

if [ ! -e $filePath -o -d $filePath -o $extension != "tar.gz" ]
then
    echo "$1 is not a database file"
    exit 1
fi

###################################################
#         Copy to Temp Directory                  #
###################################################

mkdir $tempPath

# extract backup file to the temp folder
tar -xz -C $tempPath -f $filePath

###################################################
#            Sync to Database                     #
###################################################

# copy the database file
rsync -a $tempPath/$dbName/ $commonPath/$dbName

# copy the media file
rsync -a --delete $tempPath/media/ $mediaPath/media

###################################################
#              Delete Temp Data                   #
###################################################

# remove the temporary folder
rm -rf $tempPath
