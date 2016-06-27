#!/bin/bash

###################################################
#               Set Initial Data                  #
###################################################
echo "vvvvSetting initial data"

scriptLoc=$(readlink -f $(dirname $0) )
jsonStore=$scriptLoc/temp_json
logLoc=$scriptLoc/log_files

remoteHost=cmshcal12
remoteLoc=/home/hep/jsonResults

echo "^^^^Initial data set"
echo ""
###################################################
#            Retrieve Remote Files                #
###################################################
echo "vvvvRetrieving remote files"

rsync -a $remoteHost:$remoteLoc/ $jsonStore
#ssh $remoteHost rm -f $remoteLoc/*step1_raw.json
#ssh $remoteHost rm -f $remoteLoc/*test_raw.json

echo "^^^^Remote files retrieved"
echo ""
echo ""
###################################################
#           Register New QIE Cards                #
###################################################
echo "vvvvUploading new QIE cards"
echo ""

if ls $jsonStore/*step1_raw.json &> error.log
then
    fileList=$(ls $jsonStore/*step1_raw.json)
    for file in $fileList
    do
        echo "--------Processing $(basename $file)"
        python $scriptLoc/card_upload.py $file 2> $file.log

        if [ $? -eq 0 ]
        then
            echo "------------Removing $(basename $file)"
            #rm $file*
        else
            echo "!-!-!-!-!-!-ERROR (see $(basename $file).log)"
        fi
    done
else
    echo "--------No QIE cards to upload"
fi

echo ""
echo "^^^^New QIE cards uploaded"
echo ""
echo ""
###################################################
#           Register QIE Tests                    #
###################################################
echo "vvvvUploading QIE tests"
echo ""

if ls $jsonStore/*test_raw.json &> error.log
then
    fileList=$(ls $jsonStore/*test_raw.json )
    for file in $fileList
    do
        echo "--------Processing $(basename $file)"
        python $scriptLoc/test_upload.py $file &> $file.log

        if [ $? -eq 0 ]
        then
            echo "------------Removing $(basename $file)"
            rm $file*
        else
            echo "!-!-!-!-!-!-ERROR (see $(basename $file).log)"
        fi
        echo ""
    done
else
    echo "--------No tests to upload"
    echo ""
fi

echo "^^^^QIE tests uploaded"
echo ""
echo ""

# Move log files to proper folder
mv $jsonStore/*.log $logLoc

echo "Finished"
