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

def loadCard(cardData):
    """ Loads in QIE card information """
    comments =  cardData["TestComment"]
    barcode =   cardData["Barcode"]
    print barcode

    #find or create qie card for database
    qie = QieCard.objects.filter(barcode=barcode)

    if qie:
        sys.exit('QIE card with barcode "%s" is already in the database' % cardData["Barcode"])
    else:
        card = QieCard(barcode=barcode,
                       comments=comments
                       )
    return card

def loadTests(qie, tester, date, testData, path):
    """ Loads in all test results """
    attempts = []
    
    for test in testData.keys():
        try:
            temp_test = Test.objects.get(abbreviation=test)
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
                                   log_file=path
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
                                   humidity=-999,
                                   log_file=path
                                   )
            
        attempts.append(temp_attempt)
    return attempts

def setLocation(qie, date):
    """ Sets a location for the card """
    return Location(card=qie,
                    date_received=date,
                    geo_loc="Wilson Hall 14th floor, Fermilab"
                    )

def moveJsonFile(qie, fileName):
    """ Moves the json for this upload to permanent storage """
    url = os.path.join("uploads/", qie.barcode)
    path = os.path.join(MEDIA_ROOT, url)
    if os.path.exists(path):
        exit("Database already contains folder for this card")    
    os.makedirs(path)
        
    newPath = os.path.join(path, os.path.basename(fileName))
    copyfile(fileName, newPath)
    return os.path.join(url, os.path.basename(fileName))

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


newPath = moveJsonFile(qie, fileName)
qie.save()

attempts = loadTests(qie, tester, date, cardData["testResults"], newPath)

location = setLocation(qie, date)
location.save()

for attempt in attempts:
    attempt.save()
