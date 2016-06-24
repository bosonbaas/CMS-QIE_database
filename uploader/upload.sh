#!/bin/bash

###################################################
#               Set Initial Data                  #
###################################################
echo "Setting initial data"

scriptLoc=$(readlink -f $(dirname $0) )
jsonStore=$scriptLoc/temp_json

remoteHost=cmshcal12
remoteLoc=/home/hep/tempJsonResults
mkdir $jsonStore

echo "Initial data set"
###################################################
#            Retrieve Remote Files                #
###################################################
echo "Retrieving remote files"

rsync -a $remoteHost:$remoteLoc/ $jsonStore
ssh $remoteHost rm $remoteLoc/*.json

echo "Remote files retrieved"
###################################################
#           Register New QIE Cards                #
###################################################
echo "Uploading new QIE cards"

fileList=$(ls $jsonStore/*_step1_raw.json )
for file in $fileList
do
    python $scriptLoc/card_upload.py $file
    rm $file
done

echo "New QIE cards uploaded"
###################################################
#           Register QIE Tests                    #
###################################################
echo "Uploading QIE tests"

fileList=$(ls $jsonStore/*raw.json )
for file in $fileList
do
    python $scriptLoc/test_upload.py $file
done

echo "QIE tests uploaded"

rm -r $jsonStore
echo "Finished"
