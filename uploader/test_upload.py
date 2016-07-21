import sys
import os
import json
import django
import time
from shutil import copyfile

sys.path.insert(0, '/home/django/testing_database/card_db')
django.setup()

from django.utils import timezone
from qie_cards.models import Test, Tester, Attempt, Location, QieCard
from card_db.settings import MEDIA_ROOT



def getUID(raw):
    """ Parses the raw UID into a pretty-print format """ 
    return raw[2:18]

def moveJsonFile(qie, fileName):
    """ Moves the json for this upload to permanent storage """
    uniquePre = str(int(time.time()))
    url = os.path.join("uploads/", qie.barcode)
    path = os.path.join(MEDIA_ROOT, url)
    if not os.path.exists(path):
        exit("Database does not contain this card's log folder")
        
    newPath = os.path.join(path, uniquePre + os.path.basename(fileName))
    copyfile(fileName, newPath)
    return os.path.join(url, uniquePre + os.path.basename(fileName))

# Get filename and upload file to dictionary
fileName = sys.argv[1]
infile = open(fileName, "r")
cardData = json.load(infile)

overwrite = cardData["Overwrite"]

# Check if the tester exists
try:
    tester = Tester.objects.get(username=cardData["User"])
except:
    sys.exit("Tester %s not valid" % cardData["User"]) 

# Get the time of the test
test_time = cardData["DateRun"] + "-06:00"

# Check if the QIE card exists
try:
    qie = QieCard.objects.get(uid=getUID(cardData["Unique_ID"]))
except:
    sys.exit('QIE card with UID %s not in database' % getUID(cardData["Unique_ID"]))

# Move the json file
url = moveJsonFile(qie, fileName)

attemptArr = []

# Make URL for HR log file
hrlog = cardData["HumanLogFile"]
hrURL = os.path.join("human_readable_logs/", hrlog + "_tests.log")

#load in all test results
for test in cardData["Tests"].keys():
    if(test != "TestType"):
        try:
            temp_test = Test.objects.get(abbreviation=test)
        except:
            sys.exit('Test "%s" not in database' % test)

        data = cardData["Tests"][test]

        prev_attempts = list(Attempt.objects.filter(card=qie, test_type=temp_test))
        attempt_num = len(prev_attempts) + 1
        if(data[0] == 0 and data[1] == 0):
            temp_attempt = Attempt(card=qie,
                                   plane_loc=cardData["JSlot"],
                                   test_type=temp_test,
                                   attempt_number=attempt_num,
                                   tester=tester,
                                   date_tested=test_time,
                                   num_passed=0,
                                   num_failed=0,
                                   temperature=float(cardData["Temperature"]),
                                   humidity=float(cardData["Humidity"]),
                                   revoked=True,
                                   comments="This test returned no testing data",
                                   log_file=hrURL,
                                   hidden_log_file=url,
                                   )
        else:
            temp_attempt = Attempt(card=qie,
                                   plane_loc="default",
                                   test_type=temp_test,
                                   attempt_number=attempt_num,
                                   tester=tester,
                                   date_tested=test_time,
                                   num_passed=data[0],
                                   num_failed=data[1],
                                   temperature=float(cardData["Temperature"]),
                                   humidity=float(cardData["Humidity"]),
                                   log_file=hrURL,
                                   hidden_log_file=url,
                                   )
        
        if overwrite:
            for prev_att in prev_attempts:
                prev_att.revoked = True
                attemptArr.append(prev_att)

        attemptArr.append(temp_attempt)
        
for attempt in attemptArr:
    attempt.save()
