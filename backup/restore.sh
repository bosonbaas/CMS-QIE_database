#!/bin/bash

commonPath=/home/hep/abaas/testing_database

dbPath=$commonPath
dbName=card_db

backupPath=$commonPath/backup

mediaPath=$commonPath

file=$1
filePath=$backupPath/$file
tempPath=$backupPath/temp_dir

extension=${file#*.}

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

tar -xz -C $tempPath -f $filePath

cp -r $dbPath/$dbName/.git/ $tempPath/$dbName/.git/
cp $dbPath/$dbName/.gitignore $tempPath/$dbName/.gitignore

###################################################
#            Sync to Database                     #
###################################################

rsync -a $tempPath/$dbName/ $dbPath/$dbName
rsync -a --delete $tempPath/media/ $mediaPath/media

###################################################
#              Delete Temp Data                   #
###################################################

rm -rf $tempPath
