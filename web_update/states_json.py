"""
#   update_json.py:
#       This script collects the necessary data into a json. This json
#       is then used in the website to generate the stats page.
"""

__author__  = "Andrew Baas"
__credits__ = ["Joe Pastika", "Josh Hiltbrand", "Andrew Baas"]

__version__     = "1.0"
__maintainer__  = "Caleb Smith"
__email__       = "caleb_smith2@baylor.edu"
__status__      = "Live"

import sys
import os
import json
import calendar
from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "card_db.settings")
sys.path.insert(0, '/home/django/testing_database/card_db')
setup()

import qie_cards.custom.filters as filters
from qie_cards.models import Test, Attempt, QieCard

tests = Test.objects.filter(required=True)
cards = QieCard.objects.all()
attempts = []

totalTests = len(tests)

cardStat = {}

for card in cards:
    print card.barcode
    status = {}
    failedAny = False
    forcedAny = False
    passed = 0
    
    print "**Starting test analysis"
    for test in tests:
        attemptList = Attempt.objects.filter(card=card.pk, test_type=test.pk).order_by("attempt_number")
        attResults = filters.attemptTotalState(attemptList)
        if attResults[0] == "failed":
            failedAny = True
        elif attResults[0] == "passed":
            passed += 1

        if attResults[1]:
            forcedAny = True
    print "**Finished test analysis"
    
    if totalTests == passed:
        if forcedAny:
            status["banner"] = "GOOD (FORCED)"
            status["css"] = "forced"
        else:
            status["banner"] = "GOOD"
            status["css"] = "okay"
    elif failedAny:
        status["banner"] = "FAILED"
        status["css"] = "bad"
    else:
        status["banner"] = "INCOMPLETE"
        status["css"] = "warn"
    status["ratio"] = (passed, totalTests)
    cardStat[card.pk] = status

# Dump the json into the proper location
with open("/home/django/testing_database/media/cached_data/card_states.json", 'w') as f:
    json.dump(cardStat, f)
f.close()
