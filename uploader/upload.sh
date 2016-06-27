#!/bin/bash

###################################################
#               Set Initial Data                  #
###################################################
echo -e "\e[1;34mSetting initial data"

scriptLoc=$(readlink -f $(dirname $0) )
jsonStore=$scriptLoc/temp_json
logLoc=$scriptLoc/log_files

rm $logLoc/*.log

remoteHost=cmshcal12
remoteLoc=/home/hep/jsonResults

STATUS="\e[1;34m"
ACTION="\e[1;33m"
SUCCESS="\e[1;92m"
FAIL="\e[1;91m"
DEF="\e[39;0m"

echo -e "${STATUS}Initial data set"
echo ""
###################################################
#            Retrieve Remote Files                #
###################################################
echo -e "${STATUS}Retrieving remote files"

rsync -a $remoteHost:$remoteLoc/ $jsonStore
ssh $remoteHost rm -f $remoteLoc/*step1_raw.json
ssh $remoteHost rm -f $remoteLoc/*test_raw.json

echo -e "${STATUS}Remote files retrieved"
echo ""
###################################################
#           Register New QIE Cards                #
###################################################
echo -e "${STATUS}Uploading new QIE cards"

if ls $jsonStore/*step1_raw.json &> error.log
then
    fileList=$(ls $jsonStore/*step1_raw.json)
    for file in $fileList
    do
        echo -e "    ${ACTION}Processing${DEF} $(basename $file)"
        python $scriptLoc/card_upload.py $file 2> $file.log

        if [ $? -eq 0 ]
        then
            echo -e "      ${SUCCESS}Success"
            rm $file.log
        else
            echo -e "      ${FAIL}ERROR${DEF} (see $(basename $file).log)"
        fi
    done
else
    echo -e "    ${SUCCESS}No QIE cards to upload"
fi

echo -e "${STATUS}New QIE cards uploaded"
echo ""
###################################################
#           Register QIE Tests                    #
###################################################
echo -e "${STATUS}Uploading QIE tests"

if ls $jsonStore/*test_raw.json &> error.log
then
    fileList=$(ls $jsonStore/*test_raw.json )
    for file in $fileList
    do
        echo -e "    ${ACTION}Processing${DEF} $(basename $file)"
        python $scriptLoc/test_upload.py $file 2> $file.log

        if [ $? -eq 0 ]
        then
            echo -e "      ${SUCCESS}Success"
            rm $file*
        else
            echo -e "      ${FAIL}ERROR${DEF} (see $(basename $file).log)"
        fi
    done
else
    echo -e "    ${SUCCESS}No tests to upload"
fi

echo -e "${STATUS}QIE tests uploaded"
echo ""

# Move log files to proper folder
mv $jsonStore/*.log $logLoc

echo -e "${STATUS}Finished${DEF}"
