import sys
import os
import json
import calendar
from django import setup
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "card_db.settings")
sys.path.insert(0, '/home/django/testing_database/card_db')
setup()

from django.utils import timezone
from qie_cards.models import Test, Tester, Attempt, Location, QieCard

FAILED = 2
PASSED = 1
REMAIN = 0
DEFAULT = -1

tests = list(Test.objects.all())
attempts = list(Attempt.objects.order_by("date_tested"))
cards = list(QieCard.objects.all())

testStates = {}

for test in tests:
    testStates[str(test.pk)] = {}
    for card in cards:
        temp = {"barcode":card.barcode, "date":-1,"state":DEFAULT}
        testStates[str(test.pk)][card.pk] = temp

for attempt in attempts:
    curState = testStates[str(attempt.test_type_id)][attempt.card_id]["state"]
    if not curState == FAILED:
        if attempt.passed_all() and not attempt.revoked:
            testStates[str(attempt.test_type_id)][attempt.card_id]["date"] = calendar.timegm(attempt.date_tested.timetuple())
            testStates[str(attempt.test_type_id)][attempt.card_id]["state"] = PASSED
        elif not attempt.num_failed == 0 and not attempt.revoked:
            testStates[str(attempt.test_type_id)][attempt.card_id]["date"] = calendar.timegm(attempt.date_tested.timetuple())
            testStates[str(attempt.test_type_id)][attempt.card_id]["state"] = FAILED
        elif attempt.revoked and curState == DEFAULT:
            testStates[str(attempt.test_type_id)][attempt.card_id]["date"] = calendar.timegm(attempt.date_tested.timetuple())
            testStates[str(attempt.test_type_id)][attempt.card_id]["state"] = REMAIN

with open("../media/plots/plot.json", 'w') as f:
    json.dump(testStates, f)
f.close()
