#!/bin/bash

# remote.sh: This script manages the upload of Test Stand 2 json files.
#
# Author:   Andrew Baas
# Credits:  Shaun Hogan, Mason Dorseth, John Lawrence, Jordan Potarf,
#                Joe Pastika, Andrew Baas
# 
# Version:  2.0
# Maintainer:   Caleb Smith
# Email:    caleb_smith2@baylor.edu
# Status:   Live

###################################################
#               Set Initial Data                  #
###################################################
echo -e "\e[1;34mSetting initial data"

# local locations
scriptLoc=$(readlink -f $(dirname $0) ) # location of this script
jsonStore=$scriptLoc/temp_json          # location of json files
logLoc=$scriptLoc/log_files             # location of error logs
hrLogLoc=$scriptLoc/../media/human_readable_logs    # location of HR logs
uhtrLoc=$scriptLoc/uhtr_results         # location of uhtr plots

# remote locations
remoteHost=hep@cmshcal12                # the host which is submitting
remoteArchive=$1                        # location of the results
remoteLoc=$remoteArchive/jsonResults    # location of the json files
remoteHRLog=$remoteArchive/logResults   # location of the HR logs
remoteUHTR=$remoteArchive/uhtrResults   # location of the uhtr results

STATUS="\e[1;34m"   # color of status statements
ACTION="\e[1;33m"   # color of action statements
SUCCESS="\e[1;92m"  # color of success statements
FAIL="\e[1;91m"     # color of failure statements
DEF="\e[39;0m"      # default colors of text

# remove old error logs
rm -f $logLoc/*.log

echo -e "${STATUS}Initial data set"
echo ""

###################################################
#            Retrieve Remote Files                #
###################################################
echo -e "${STATUS}Retrieving remote files"

# copy json files from the remote location
if rsync -aq $remoteHost:$remoteLoc/*.json $jsonStore 2> /dev/null
then
    echo -e "    ${STATUS}Retrieving .json"
else
    echo -e "    ${SUCCESS}No remote json files"
fi

# copy HR log files from the remote location
if rsync -aq $remoteHost:$remoteHRLog/*.log $hrLogLoc 2> /dev/null
then
    echo -e "    ${STATUS}Retrieving HR log files"
else
    echo -e "    ${SUCCESS}No HR Log files"
fi

# copy uhtr plots from the remote location
if rsync -aq --delete $remoteHost:$remoteUHTR/ $uhtrLoc 2> /dev/null
then
    echo -e "    ${STATUS} Retrieving uHTR plots"
else
    echo -e "    ${SUCCESS}No uHTR files"
fi

echo -e "${STATUS}Remote files retrieved"
echo ""
###################################################
#             Make Folders for uHTR               #
###################################################
echo -e "${STATUS}Copying uHTR Folders"

# make a ci_plots directory for each card
folderList=$(ls $uhtrLoc/ci_plots)  # list of directories in ci_plots
for file in $folderList
do
    echo -e "    ${ACTION}Processing${DEF} ci_$(basename $file)"
    cp -r $uhtrLoc/ci_plots/$file $jsonStore/ci_plot$(basename $file)
done

# make a ped_plots directory for each card
folderList=$(ls $uhtrLoc/ped_plots) # list of directories in ped_plots
for file in $folderList
do
    echo -e "    ${ACTION}Processing${DEF} ped_$(basename $file)"
    cp -r $uhtrLoc/ped_plots/$file $jsonStore/ped_plot$(basename $file)
done

# make a phase_plots directory for each card
folderList=$(ls $uhtrLoc/phase_plots)   # list of directories in phase_plots
for file in $folderList
do
    echo -e "    ${ACTION}Processing${DEF} phase_$(basename $file)"
    cp -r $uhtrLoc/phase_plots/$file $jsonStore/phase_plot$(basename $file)
done

# make a shunt_plots directory for each card
folderList=$(ls $uhtrLoc/shunt_plots)   # list of directories in shunt_plots
for file in $folderList
do
    echo -e "    ${ACTION}Processing${DEF} shunt_$(basename $file)"
    cp -r $uhtrLoc/shunt_plots/$file $jsonStore/shunt_plot$(basename $file)
done

echo -e "${STATUS}uHTR Folders Copied"
echo ""
###################################################
#             Register QIE Tests                  #
###################################################
echo -e "${STATUS}Uploading QIE tests"

# detemine if there are test_raw.json files
if ls $jsonStore/*test_raw.json &> /dev/null
then
    # upload each test_raw.json file to the database
    fileList=$(ls $jsonStore/*test_raw.json )   # list of test_raw.json
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
###################################################
#           Register uHTR Tests                   #
###################################################
echo -e "${STATUS}Uploading uHTR tests"

# detemine if there are test_uhtr.json files
if ls $jsonStore/*test_uhtr.json &> /dev/null
then
    # upload each test_uhtr.json file to the database
    fileList=$(ls $jsonStore/*test_uhtr.json )  # list of test_uhtr.json
    for file in $fileList
    do
        echo -e "    ${ACTION}Processing${DEF} $(basename $file)"
        python $scriptLoc/uhtr_upload.py $file 2> $file.log

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

echo -e "${STATUS}uHTR tests uploaded"
echo ""

# Move log files to proper folder
mv $jsonStore/*.log $logLoc 2> /dev/null

# Remove any remaining folders in the json area
rm -r $jsonStore/phase_plot*
rm -r $jsonStore/ped_plot*
rm -r $jsonStore/shunt_plot*
rm -r $jsonStore/ci_plot*
rm -r $jsonStore/*.json
rm -r $jsonStore/*.log

echo -e "${STATUS}Finished${DEF}"
