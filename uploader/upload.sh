#!/bin/bash

scriptLoc=$(readlink -f $(dirname $0) )
jsonStore=$scriptLoc/temp_json

remoteHost=cmshcal12
remoteLoc=/home/hep/tempJsonResults

fileList=$(ssh $remoteHost ls $remoteLoc)

mkdir $jsonStore

rsync -av $remoteHost:$remoteLoc/ $jsonStore

ssh $remoteHost rm $remoteLoc/*.json

for file in $fileList
do
    filePath=$jsonStore/$file
    echo $filePath   

    python $scriptLoc/jsonparser.py $filePath
done

rm -r $jsonStore
