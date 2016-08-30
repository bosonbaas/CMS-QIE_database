#!/bin/bash

# hour_backup.sh: This script backs up the current contents of the folders
#       card_db and media at the o'clock of each even hour 
#       (see /etc/crontab) and stores the backup both locally and at a
#       remote location
#
# Author:   Andrew Baas
# Credits:  Jay Dittmann, Andrew Baas
# 
# Version:  1.02
# Maintainer:   Caleb Smith
# Email:    caleb_smith2@baylor.edu
# Status:   Live

scriptLoc=$(readlink -f $(dirname $0) )    # location of this script
commonPath=${scriptLoc%/*}                 # location of the common DB folder
dbPath=$commonPath/card_db/                # location of the database folder
backupPath=$commonPath/backup/temp_backup/ # location to store backup files
mediaPath=$commonPath                      # location of DB media files

remoteBackup=$backupPath    # location of backup folder on the remote backup
remoteSSH=hep@cmshcal12     # host of the remote backup

###################################################
#                  Local Backup                   #
###################################################

dtFormat="%F_%H%M"      # date format for backup file name
database=db.sqlite3     # name of the database file
media=media             # name of the media folder
dest=$backupPath$(date +$dtFormat)  # name of the compressed backup file

# Compress current version of database and media files
tar -zcf $dest.tar.gz -C $mediaPath $media --exclude media/callibration -C $commonPath card_db --exclude .git --exclude .gitignore

###################################################
#            Delete old DB backups                #
###################################################

numBack=$(($(ls -l $backupPath | wc -l) - 1))   # number of backups
expTime=2820                                    # expiration time (seconds)
findOpt="-mmin +$expTime -delete"               # options for find command
if (( $numBack > 24 ))
  then
    # Delete any files which have expired
    find $backupPath $findOpt
fi

###################################################
#                  Network Backup                 #
###################################################

# Backup local files exactly to remote backup location
# Note: This deletes any extra DB backups on the remote location
rsync -a --delete $backupPath $remoteSSH:$remoteBackup
