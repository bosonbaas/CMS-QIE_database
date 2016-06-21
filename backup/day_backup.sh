#!/bin/bash

commonPath=$(dirname $0)/..
dbPath=$commonPath/card_db/
backupPath=$commonPath/backup/daily_backup/
mediaPath=$commonPath

remoteBackup=$backupPath
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
