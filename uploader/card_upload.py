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

def loadCard(cardData):
    # Load in QIE card information
    uid =       getUID(cardData["Unique_ID"])
    comments =  cardData["TestComment"]
    barcode =   cardData["Barcode"]

    #find or create qie card for database
    qie = QieCard.objects.filter(uid=getUID(cardData["Unique_ID"]))

    if qie:
        print 'QIE card with UID "%s" is already in the database' % getUID(cardData["Unique_ID"])
        sys.exit('QIE card with UID "%s" is already in the database' % getUID(cardData["Unique_ID"]))
    else:
        card = QieCard.objects.create(uid=uid, barcode=barcode, comments=comments, plane_loc="default")
    return card

def loadTests(qie, tester, date, testData):

    #load in all test results
    for test in testData.keys():
        try:
            temp_test = Test.objects.get(name=test)
        except:
            print 'Test "%s" not in database' % test
            sys.exit('Test "%s" not in database' % test)
    
        prev_attempts = Attempt.objects.filter(card=qie, test_type=temp_test)
        attempt_num = len(prev_attempts) + 1
        if(testData[test]): 
            temp_attempt = Attempt(card=qie,
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
                                   test_type=temp_test,
                                   attempt_number=attempt_num,
                                   tester=tester,
                                   date_tested=date,
                                   num_passed=0,
                                   num_failed=1,
                                   temperature=-999,
                                   humidity=-999
                                   )
            
        temp_attempt.save()

# Load the .json into a dictionary
fileName = sys.argv[1]

infile = open(fileName, "r")
cardData = json.load(infile)

# Upload data to the database
qie = loadCard(cardData)

#find tester account
try:
    tester = Tester.objects.get(username=cardData["User"])
except:
    print("Tester %s not valid" % cardData["User"])
    sys.exit("Invalid Tester") 

#load time of test
date = cardData["DateRun"]

loadTests(qie, tester, date, cardData["testResults"])
