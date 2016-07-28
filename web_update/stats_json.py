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

attempts = []
tests = list(Test.objects.filter(required=True))

for test in tests:
    attempts.extend(list(test.attempt_set.all())) 
        
cards = list(QieCard.objects.all().order_by("barcode"))

testFailedStats = filters.getFailedCardStats(cards, tests, attempts)
testPassedStats = filters.getPassedCardStats(cards, tests, attempts)
testRemStats = filters.getRemCardStates(cards, tests, attempts)

testStats = {'passed': testPassedStats,
             'failed': testFailedStats,
             'remaining': testRemStats,
            }

# Dump the json into the proper location
with open("/home/django/testing_database/media/cached_data/stats.json", 'w') as f:
    json.dump(testStats, f)
f.close()
