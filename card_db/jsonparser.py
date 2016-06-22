import django
django.setup()
import sys
import json
from django.utils import timezone
from qie_cards.models import *

#file name of report
fileName = sys.argv[1]

#open file and load it into dict
infile = open(fileName, "r")

data = infile

cardData = json.load(data)

#dict for plane location
geo_loc_set = {"RM1": {"0x19": "J2", "0x1a": "J3", "0x1b": "J4", "0x1c": "J5"},
               "RM2": {"0x19": "J7", "0x1a": "J8", "0x1b": "J9", "0x1c": "J10"},
               "RM3": {"0x19": "J18", "0x1a": "J19", "0x1b": "J20", "0x1c": "J21"},
               "RM4": {"0x19": "J23", "0x1a": "J24", "0x1b": "J25", "0x1c": "J26"},}

#find or create tester account
try:
    tester = Tester.objects.get(username=data["Tester"])
except:
    print 'Tester "%(name)"  not valid' % {'name': data["Tester"]}
    sys.exit('Tester "%(name)"  not valid' % {'name': data["Tester"]}) 

#load time of test
test_time = data["DateRun"]

#find or create qie card for database
try:
    qie = QieCard.objects.get(uid=data["Unique_ID"])
except:
    print 'QIE card with UID "%(uid)" not in database' % {'uid': data["Unique_ID"]}
    sys.exit('QIE card with UID "%(uid)" not in database' % {'uid': data["Unique_ID"]})

#load in all test results
for test in bridgeData.keys():
    try:
        temp_test = Test.objects.get(name=test)
    except:
        print 'Test "%(name)" not in database' % {'name': test}
        sys.exit('Test "%(name)" not in database' % {'name': test})
    
    prev_attempts = Attempt.objects.filter(card=qie, test_type=temp_test)
    attempt_num = len(prev_attempts) + 1
    temp_attempt = Attempt(card=qie,
                           test_type=temp_test,
                           attempt_number=attempt_num,
                           tester=tester,
                           date_tested=test_time,
                           num_passed=data[test][0],
                           num_failed=data[test][1],
                           temperature=data["temperature"],
                           humidity=data["humidity"]
                           )
    temp_attempt.save()


