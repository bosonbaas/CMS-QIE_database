scriptLoc=$(readlink -f $(dirname $0) )
tempDir=$scriptLoc/temp
mapping=calibrationParams.txt
fileName=${1%/}
plotLoc=$1/shunt/plots
calibration=$scriptLoc/../media/calibration

###################################################
#            Clear Temp directory                 #
###################################################
if [ ! -e $fileName -o ! -d $fileName ]
then
    echo "$fileName is not a folder"
    exit 1
fi 

folderLoc=$calibration/$(date +epochSec%s)
cp -rv $fileName/ $folderLoc/

tar -cvzf $folderLoc/$(basename $fileName).tar.gz -C $(dirname $fileName) $(basename $fileName)

echo "calling python script"
python $scriptLoc/calibration_uploader.py $folderLoc
