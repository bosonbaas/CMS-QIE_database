import django
django.setup()
import sys
import json
from django.utils import timezone
from qie_cards.models import *

#file name of report
file_name = "Something for now"

#open file and load it into dict
infile = open(file_name, "r")
data = json.load(infile)

#dict for plane location
geo_loc_set = {"RM1": {"0x19": "J2", "0x1a": "J3", "0x1b": "J4", "0x1c": "J5"},
               "RM2": {"0x19": "J7", "0x1a": "J8", "0x1b": "J9", "0x1c": "J10"},
               "RM3": {"0x19": "J18", "0x1a": "J19", "0x1b": "J20", "0x1c": "J21"},
               "RM4": {"0x19": "J23", "0x1a": "J24", "0x1b": "J25", "0x1c": "J26"},}

#find or create tester account
try:
    tester = Tester.objects.get(username=data["tester"])
except:
    tester = Tester(username=data["tester"], email=noemail@email.com)
    tester.save()
del data["tester"]

#load time of test
test_time = data["timeOfTest"]
del data["timeOfTest"]

#find or create qie card for database
try:
    qie = Qie_Card.objects.get(uid=data["uniqueID"])
    qie.set_temperature(data["temperature"])
    qie.set_humidity(data["humidity"])
except:
    qie = Qie_Card(uid=data["uniqueID"], geo_loc="14 floor Wilson Hall",
                   plane_loc=geo_loc_set["RM1"][data["i2cAddress"]],
                   temperature=data["temperature"],
                   humidity=data["humidity"])
    qie.save()
del data["uniqueID"]
del data["i2cAdress"]
del data["temperature"]


#load in all test results
for test in data.keys():
    temp_test = Test.objects.get(name=test)
    prev_attempts = Attempt.objects.filter(card=qie, test_type=temp_test)
    attempt_num = len(prev_attempts) + 1
    temp_attempt = Attempt(card=qie, test_type=temp_test, attempt_number=attempt_num,
                    tester=tester, date_tester=test_time, passed=data[test])
    temp_attempt.save()
