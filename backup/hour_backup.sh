#!/bin/bash

scriptLoc=$(readlink -f $(dirname $0) )
commonPath=${scriptLoc%/*}
dbPath=$commonPath/card_db/
backupPath=$commonPath/backup/temp_backup/
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

# Delete old databases
numBack=$(($(ls -l $backupPath | wc -l) - 1))
expTime=2940
findOpt="-cmin +$expTime -delete"
if (( $numBack > 24 ))
  then
    find $backupPath $findOpt
fi

###################################################
#                  Network Backup                 #
###################################################

rsync -a --delete $backupPath $remoteSSH:$remoteBackup
