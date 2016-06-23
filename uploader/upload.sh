#!/bin/bash

scriptLoc=$(readlink -f $(dirname $0) )
jsonStore=$scriptLoc/temp_json

remoteHost=cmshcal12
remoteLoc=/home/hep/abaas/json_storage

fileList=$(ssh $remoteHost ls $remoteLoc)

echo $fileList
mkdir $jsonStore

rsync -av $remoteHost:$remoteLoc/ $jsonStore

ssh $remoteHost rm $remoteLoc/*.json

for file in $fileList
do
    localFile=$jsonStore/$file
    remoteFile=$remoteLoc/$file

#    python $scriptLoc/jsonparser.py $localFile
done

#rm -r $jsonStore
