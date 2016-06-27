import sys
import json
import django

sys.path.insert(0, '/home/hep/abaas/testing_database/card_db')
django.setup()

from django.utils import timezone
from qie_cards.models import *



def getUID(raw):
    raw = raw[4:]
    refined = ""
    for i in range(6):
        refined += raw[2*i : 2*(i + 1)]
        refined += ':'
    return refined[:17]

def moveJsonFile(qie, fileName):
    url = os.path.join("uploads/", qie.uid)
    path = os.path.join(MEDIA_ROOT, url)
    if not os.path.exists(path):
        exit("Database does not contain this card's log folder")
        
    newPath = os.path.join(path, os.path.basename(fileName))
    os.rename(fileName, newPath)
    return url

#file name of report
fileName = sys.argv[1]

#open file and load it into dict
infile = open(fileName, "r")

cardData = json.load(infile)

#find or create tester account
try:
    tester = Tester.objects.get(username=cardData["User"])
except:
    sys.exit("Tester %s not valid" % cardData["User"]) 

#load time of test
test_time = cardData["DateRun"] + "-06:00"

#find or create qie card for database
try:
    qie = QieCard.objects.get(uid=getUID(cardData["Unique_ID"]))
except:
    sys.exit('QIE card with UID %s not in database' % getUID(cardData["Unique_ID"]))

url = moveJsonFile(qie, fileName)

attemptArr = []

#load in all test results
for test in cardData["Tests"].keys():
    if(test != "TestType"):
        try:
            temp_test = Test.objects.get(name=test)
        except:
            sys.exit('Test "%s" not in database' % test)

        data = cardData["Tests"][test]

        prev_attempts = Attempt.objects.filter(card=qie, test_type=temp_test)
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
                                   log_file=url
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
                                   log_file=url
                                   )
            
        attemptArr.append(temp_attempt)
        
for attempt in attemptArr:
    attempt.save()
