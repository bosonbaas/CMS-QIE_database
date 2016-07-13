import sys
import os
import django
import matplotlib.pyplot as plt

import matplotlib.patches as mpatches
import datetime
import numpy as np

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "card_db.settings")
os.environ.setdefault("DISPLAY", ":0")
sys.path.insert(0, '/home/django/testing_database/card_db')
django.setup()

from django.utils import timezone
from qie_cards.models import Test, Tester, Attempt, Location, QieCard
import qie_cards.custom.filters as filters
import importlib

plots = importlib.import_module("plots");

REG_PLOT = ["PrelimPlots",
            "ZeroesPlots",
           ]

__import__('plots',globals(), locals(), REG_PLOT, -1)

for plotName in REG_PLOT:
    
    plotClass = getattr(plots, plotName)
    curPlot = plotClass()

    ################################################
    #     Upload specific tests and attempts       #
    ################################################
    tests = curPlot.getTests() 
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
    
    
    currentTime = datetime.datetime.now().month * 30 + datetime.datetime.now().day + (datetime.datetime.now().hour + 6)/24.0
    
    # General values
    xRange = [date for date in xrange(210, int(currentTime) + 2)]
    labels = [(((date - 1) % 30) + 1) for date in xRange]
    
    
    ################################################
    #                Make plots                    #
    ################################################
    
    plt.xticks(xRange, labels, rotation='horizontal')
    plt.xlim([xRange[0], currentTime])
    
    negHist = list(date.month * 30 + date.day + date.hour/24.0 for date in failed)
    posHist = list(date.month * 30 + date.day + date.hour/24.0 for date in passed)
    if passed:
        plt.hist(posHist, bins=len(set(passed)), histtype='stepfilled', cumulative=1, linewidth=2, range=[xRange[0], currentTime], color="green", alpha=0.5, label="Passed Cards")
    if failed:
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
    plt.savefig("/home/django/testing_database/media/plots/" + curPlot.filename)
    plt.clf()
