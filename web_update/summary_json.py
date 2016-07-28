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

cards = list(QieCard.objects.all().order_by('barcode'))
tests = list(Test.objects.all())
attempts = list(Attempt.objects.all())
cardStat = filters.getCardTestStates(cards, tests, attempts)

# Dump the json into the proper location
with open("/home/django/testing_database/media/cached_data/summary.json", 'w') as f:
    json.dump(cardStat, f)
f.close()
