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

#file name of report
fileName = sys.argv[1]

#open file and load it into dict
infile = open(fileName, "r")

cardData = json.load(infile)

#dict for plane location
geo_loc_set = {"RM1": {"0x19": "J2", "0x1a": "J3", "0x1b": "J4", "0x1c": "J5"},
               "RM2": {"0x19": "J7", "0x1a": "J8", "0x1b": "J9", "0x1c": "J10"},
               "RM3": {"0x19": "J18", "0x1a": "J19", "0x1b": "J20", "0x1c": "J21"},
               "RM4": {"0x19": "J23", "0x1a": "J24", "0x1b": "J25", "0x1c": "J26"},}

#find or create tester account
try:
    tester = Tester.objects.get(username=cardData["User"])
except:
    print("Tester %s not valid" % cardData["User"])
    sys.exit("Invalid Tester") 

#load time of test
test_time = cardData["DateRun"]

#find or create qie card for database
try:
    qie = QieCard.objects.get(uid=getUID(cardData["Unique_ID"]))
except:
    print 'QIE card with UID %s not in database' % getUID(cardData["Unique_ID"])
    sys.exit("Invalid QIE card UID")

#load in all test results
for test in cardData.keys():
    if(test != "DateRun" and test != "Unique_ID" and test != "Barcode" and test != "User"):
        try:
            temp_test = Test.objects.get(name=test)
        except:
            print 'Test "%s" not in database' % test
            sys.exit('Test "%s" not in database' % test)
    
        prev_attempts = Attempt.objects.filter(card=qie, test_type=temp_test)
        attempt_num = len(prev_attempts) + 1
        if(cardData[test][0] == 0 and cardData[test][1] == 0): 
            temp_attempt = Attempt(card=qie,
                                   test_type=temp_test,
                                   attempt_number=attempt_num,
                                   tester=tester,
                                   date_tested=test_time,
                                   num_passed=0,
                                   num_failed=0,
                                   temperature=float(cardData["Temperature"]),
                                   humidity=float(cardData["Humidity"]),
                                   revoked=True,
                                   comments="This test returned no testing data"
                                   )
        else:
            temp_attempt = Attempt(card=qie,
                                   test_type=temp_test,
                                   attempt_number=attempt_num,
                                   tester=tester,
                                   date_tested=test_time,
                                   num_passed=cardData[test][0],
                                   num_failed=cardData[test][1],
                                   temperature=float(cardData["Temperature"]),
                                   humidity=float(cardData["Humidity"])
                                   )
            
        temp_attempt.save()
