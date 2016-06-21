#!/bin/bash

commonPath=/home/hep/abaas/testing_database
dbPath=$commonPath/card_db/
backupPath=$commonPath/backup/daily_backup/
mediaPath=$commonPath

remoteBackup=/home/hep/abaas/testing_database/backup/daily_backup/
remoteSSH=hep@cmshcal12

###################################################
#                  Local Backup                   #
###################################################

dtFormat="%F_%H%M"
database=db.sqlite3
media=media
dest=$backupPath$(date +$dtFormat)

# Compress current version of database and media files
tar -zcf $dest.tar.gz -C $mediaPath $media -C $commonPath card_db --exclude .git --exclude .gitignore

###################################################
#                  Network Backup                 #
###################################################

rsync -a --delete $backupPath $remoteSSH:$remoteBackup
