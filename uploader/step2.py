import sys
import os
import json
import django
from shutil import copyfile

sys.path.insert(0, '/home/django/testing_database/card_db')
django.setup()

from django.utils import timezone
from qie_cards.models import Test, Tester, Attempt, Location, QieCard
from card_db.settings import MEDIA_ROOT



def getUID(raw):
    """ Parses the raw UID into a pretty-print format """
    raw = raw[4:]
    refined = ""
    for i in range(6):
        refined += raw[2*i : 2*(i + 1)]
        refined += ':'
    return refined[:17]

def loadCard(cardData, qie):
    """ Loads in QIE card information """
    qie.uid =       getUID(cardData["Unique_ID"])
    qie.bridge_major_ver = cardData["FirmwareMaj"]
    qie.bridge_minor_ver = cardData["FirmwareMin"]
    qie.bridge_other_ver = cardData["FirmwareOth"]
    qie.igloo_major_ver = cardData["IglooMajVer"]
    qie.igloo_minor_ver = cardData["IglooMinVer"]
    
def moveJsonFile(qie, fileName):
    """ Moves the json for this upload to permanent storage """
    url = os.path.join("uploads/", qie.barcode)
    path = os.path.join(MEDIA_ROOT, url)
    if not os.path.exists(path):
        exit("Database does not contain this card's log folder")
        
    newPath = os.path.join(path, os.path.basename(fileName))
    copyfile(fileName, newPath)
    return os.path.join(url, os.path.basename(fileName))

# Load the .json into a dictionary
fileName = sys.argv[1]

infile = open(fileName, "r")
cardData = json.load(infile)

# Upload data to the database

barcode = cardData["Barcode"]

try:    
    qie = QieCard.objects.get(barcode=barcode)
except:
    sys.exit('QIE card with barcode "%s" is not in the database' % cardData["Barcode"])

loadCard(cardData, qie)

newPath = moveJsonFile(qie, fileName)
qie.save()
