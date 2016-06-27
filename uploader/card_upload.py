import sys
import json
import django

sys.path.insert(0, '/home/hep/abaas/testing_database/card_db')
django.setup()

from django.utils import timezone
from qie_cards.models import *
from card_db.settings import MEDIA_ROOT



def getUID(raw):
    raw = raw[4:]
    refined = ""
    for i in range(6):
        refined += raw[2*i : 2*(i + 1)]
        refined += ':'
    return refined[:17]

def loadCard(cardData):
    # Load in QIE card information
    uid =       getUID(cardData["Unique_ID"])
    comments =  cardData["TestComment"]
    barcode =   cardData["Barcode"]
    major_ver = cardData["FirmwareMaj"]
    minor_ver = cardData["FirmwareMin"]
    other_ver = cardData["FirmwareOth"]

    #find or create qie card for database
    qie = QieCard.objects.filter(uid=getUID(cardData["Unique_ID"]))

    if qie:
        sys.exit('QIE card with UID "%s" is already in the database' % getUID(cardData["Unique_ID"]))
    else:
        card = QieCard(barcode=barcode,
                       uid=uid,
                       major_ver=major_ver,
                       minor_ver=minor_ver,
                       other_ver=other_ver,
                       comments=comments
                       )
    return card

def loadTests(qie, tester, date, testData):

    attempts = []
    
    #load in all test results
    for test in testData.keys():
        try:
            temp_test = Test.objects.get(name=test)
        except:
            sys.exit('Test "%s" not in database' % test)
    
        prev_attempts = Attempt.objects.filter(card=qie, test_type=temp_test)
        attempt_num = len(prev_attempts) + 1
        if(testData[test]): 
            temp_attempt = Attempt(card=qie,
                                   plane_loc="default",
                                   test_type=temp_test,
                                   attempt_number=attempt_num,
                                   tester=tester,
                                   date_tested=date,
                                   num_passed=1,
                                   num_failed=0,
                                   temperature=-999,
                                   humidity=-999,
                                   )
        else:
            temp_attempt = Attempt(card=qie,
                                   plane_loc="default",
                                   test_type=temp_test,
                                   attempt_number=attempt_num,
                                   tester=tester,
                                   date_tested=date,
                                   num_passed=0,
                                   num_failed=1,
                                   temperature=-999,
                                   humidity=-999
                                   )
            
        attempts.append(temp_attempt)
        return attempts

def setLocation(qie, date):
    return Location(card=qie,
                    date_received=date,
                    geo_loc="Wilson Hall 14th floor, Fermilab"
                    )

def moveJsonFile(qie, fileName):
    path = os.path.join(MEDIA_ROOT, "uploads/", qie.uid)
    print path
    if not os.path.exists(path):
        os.makedirs(path)
        
    newPath = os.path.join(path, os.path.basename(fileName))
    print newPath
    os.rename(fileName, newPath)

# Load the .json into a dictionary
fileName = sys.argv[1]

infile = open(fileName, "r")
cardData = json.load(infile)

# Upload data to the database
qie = loadCard(cardData)

#load time of test
date = cardData["DateRun"] + "-06:00"


#find tester account
try:
    tester = Tester.objects.get(username=cardData["User"])
except:
    sys.exit("Tester %s not valid" % cardData["User"])


qie.save()
attempts = loadTests(qie, tester, date, cardData["testResults"])

location = setLocation(qie, date)
location.save()

for attempt in attempts:
    attempt.save()

moveJsonFile(qie, fileName)
