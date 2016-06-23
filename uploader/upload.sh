#!/bin/bash

###################################################
#               Set Initial Data                  #
###################################################

scriptLoc=$(readlink -f $(dirname $0) )
jsonStore=$scriptLoc/temp_json

remoteHost=cmshcal12
remoteLoc=/home/hep/tempJsonResults
mkdir $jsonStore

###################################################
#            Retrieve Remote Files                #
###################################################

rsync -av $remoteHost:$remoteLoc/ $jsonStore
ssh $remoteHost rm $remoteLoc/*.json

###################################################
#           Register New QIE Cards                #
###################################################

fileList=$(find $jsonStore -name *_step1_raw.json )
for file in $fileList
do
    #filePath=$jsonStore/$file
    echo $file  

    #python $scriptLoc/jsonparser.py $filePath
done

###################################################
#           Register QIE Tests                    #
###################################################

rm -r $jsonStore
