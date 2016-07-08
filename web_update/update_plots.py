import sys
import os
import django
import matplotlib.pyplot as plt
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "card_db.settings")
os.environ.setdefault("DISPLAY", ":0")
sys.path.insert(0, '/home/django/testing_database/card_db')
django.setup()

from django.utils import timezone
from qie_cards.models import Test, Tester, Attempt, Location, QieCard
import qie_cards.custom.filters as filters

################################################
#     Upload specific tests and attempts       #
################################################
tests = [Test.objects.get(abbreviation="Res_1"),
         Test.objects.get(abbreviation="Res_2"),
         Test.objects.get(abbreviation="Res_3"),
         Test.objects.get(abbreviation="Res_4"),
         Test.objects.get(abbreviation="Res_5"),
         Test.objects.get(abbreviation="Res_6"),
         Test.objects.get(abbreviation="Res_7"),
         Test.objects.get(abbreviation="Res_8"),
         Test.objects.get(abbreviation="Res_9"),
         Test.objects.get(abbreviation="Res_10"),
         Test.objects.get(abbreviation="Res_11"),
         Test.objects.get(abbreviation="Res_12"),
         Test.objects.get(abbreviation="Res_13"),
         Test.objects.get(abbreviation="Res_14"),
         Test.objects.get(abbreviation="Res_15"),
         Test.objects.get(abbreviation="Program"),
         Test.objects.get(abbreviation="Vis"),
         Test.objects.get(abbreviation="SuplCur"),
        ]
attempts = []
for test in tests:
    attempts.extend(Attempt.objects.filter(test_type=test.pk))
cards = QieCard.objects.all()


################################################
#        Upload passed and failed cards        #
################################################
passed = filters.getPassedDates(cards, tests, attempts)
failed = filters.getFailedDates(cards, tests, attempts)

################################################
#          Initialize plot values              #
################################################

import matplotlib.patches as mpatches
import datetime
import numpy as np

currentTime = datetime.datetime.now().month * 30 + datetime.datetime.now().day + (datetime.datetime.now().hour + 6)/24.0

"""
# Initialize positive values
posDateDict = {}
for date in passed:
    dateKey = date.month * 30 + date.day + date.hour/24.0
    if dateKey in posDateDict:
        posDateDict[dateKey] += 1
    else:
        posDateDict[dateKey] = 1

posDates = sorted(posDateDict.keys())
posCardsOnly = []
posRunningTotal = []
for count,val in enumerate(posDates):
    posCardsOnly.append(posDateDict[val])
    if count == 0: posRunningTotal.append(posDateDict[val])
    else: posRunningTotal.append(posRunningTotal[-1] + posDateDict[val])
posDates.append(currentTime)
posRunningTotal.append(posRunningTotal[-1])
print passed
print "posDateDict: ", posDateDict

# Initialize negative values
negDateDict = {}
for date in failed:
    dateKey = date.month * 30 + date.day + date.hour/24.0
    if dateKey in negDateDict:
        negDateDict[dateKey] += 1
    else:
        negDateDict[dateKey] = 1
negDates = sorted(negDateDict.keys())
negCardsOnly = []
negRunningTotal = []
for count,val in enumerate(negDates):
    negCardsOnly.append(negDateDict[val])
    if count == 0: negRunningTotal.append(negDateDict[val])
    else: negRunningTotal.append(negRunningTotal[-1] + negDateDict[val])
negDates.append(currentTime)
negRunningTotal.append(negRunningTotal[-1])
print passed
print "negDateDict: ", negDateDict"""

# General values
xRange = [date for date in xrange(210, int(currentTime) + 2)]
labels = [(((date - 1) % 30) + 1) for date in xRange]


################################################
#                Make plots                    #
################################################

"""plt.figure(1)
plt.xticks(xRange, labels, rotation='horizontal')
plt.plot(posDates, posRunningTotal, marker='.', color='g', linewidth=2, label="Passed Cards")
plt.plot(negDates, negRunningTotal, marker='.', color='r', linewidth=2, label="Failed Cards")
plt.fill_between(posDates, posRunningTotal, facecolor='green',alpha=0.5)
plt.fill_between(negDates, 0, negRunningTotal, facecolor='red',alpha=0.5)

plt.title('QIE Cards Preliminary Tests', fontsize=16, color='black')
plt.xlabel('Date Tested (in July 2016)', fontsize=14, color='black')
plt.ylabel('# of Cards Tested', fontsize=14, color='black')

legend = plt.legend(loc='upper center', shadow=True)

# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90') 

plt.figure(2)"""
plt.xticks(xRange, labels, rotation='horizontal')
plt.xlim([xRange[0], currentTime])
negHist = list(date.month * 30 + date.day + date.hour/24.0 for date in failed)
posHist = list(date.month * 30 + date.day + date.hour/24.0 for date in passed)
plt.hist(posHist, bins=len(set(passed)), histtype='stepfilled', cumulative=1, linewidth=2, range=[xRange[0], currentTime], color="green", alpha=0.5, label="Passed Cards")
plt.hist(negHist, bins=len(set(failed)), histtype='stepfilled', cumulative=1, linewidth=2,  range=[xRange[0], currentTime], color="red", alpha=0.5, label="Failed Cards")

#plt.ylim([0,100])
plt.title('QIE Cards Preliminary Tests', fontsize=16, color='black')
plt.xlabel('Date Tested (in July 2016)', fontsize=14, color='black')
plt.ylabel('# of Cards Tested', fontsize=14, color='black')
plt.ylim([0, len(posHist) + 10])
legend = plt.legend(loc='upper center', shadow=True)

# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90') 
#plt.show()
plt.savefig("/home/django/testing_database/media/plots/plot.png")
