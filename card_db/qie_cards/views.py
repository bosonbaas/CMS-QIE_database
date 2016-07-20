from django.shortcuts import render
from django.views import generic
import datetime
from os import listdir, path
import json

from .models import QieCard, Tester, Test, Attempt, Location
import custom.filters as filters

# Create your views here.

from django.utils import timezone
from django.http import HttpResponse
from card_db.settings import MEDIA_ROOT 


class CatalogView(generic.ListView):
    """ This displays a list of all QIE cards """
    
    template_name = 'qie_cards/catalog.html'
    context_object_name = 'barcode_list'
    def get_queryset(self):
        return QieCard.objects.all().order_by('barcode')


def summary(request):
    """ This displays a summary of the cards """
    cards = list(QieCard.objects.all().order_by('barcode'))
    tests = list(Test.objects.all())
    attempts = list(Attempt.objects.all())
    
    cardStat = filters.getCardTestStates(cards, tests, attempts)
        
    return render(request, 'qie_cards/summary.html', {'cards': cardStat})

class TestersView(generic.ListView):
    """ This displays the users and email addresses """
    
    template_name = 'qie_cards/testers.html'
    context_object_name = 'tester_list'
    def get_queryset(self):
        return Tester.objects.all().order_by('username')


class TestDetailsView(generic.ListView):
    """ This displays the tests and their descriptions """

    template_name = 'qie_cards/test-details.html'
    context_object_name = 'test_list'
    def get_queryset(self):
        return Test.objects.all().order_by('name')


def stats(request):
    """ This displays a summary of the cards """
    
    attempts = list(Attempt.objects.exclude(test_type=Test.objects.get(abbreviation="overall phase scan")))   
    cards = list(QieCard.objects.all().order_by("barcode"))
    tests = list(Test.objects.exclude(abbreviation="overall phase scan")) 
 
    testFailedStats = filters.getFailedCardStats(cards, tests, attempts)
    testPassedStats = filters.getPassedCardStats(cards, tests, attempts)
    
    return render(request, 'qie_cards/stats.html', {'passed': testPassedStats,
                                                    'failed': testFailedStats,
                                                    })
        
def detail(request, card):
    """ This displays details about tests on a card """
    try:
        p = QieCard.objects.get(barcode=card)
    except QieCard.DoesNotExist:
        raise Http404("QIE card does not exist")

    tests = Test.objects.all()
    locations = Location.objects.filter(card=p)
    attempts = []
    status = {}    

    status["total"] = len(tests) - 1
    status["passed"] = 0
    failedAny = False

    for test in tests:
        attemptList = Attempt.objects.filter(card=p.pk, test_type=test.pk).order_by("attempt_number")
        if attemptList:
            last = attemptList[len(attemptList)-1]
            if not last.revoked:
                if last.passed_all():
                    status["passed"] += 1
                else:
                    failedAny = True
            attempts.append((last, True))
        else:
            attempts.append((test.name, False))
 
    if status["total"] == status["passed"]:
        status["banner"] = "GOOD"
        status["css"] = "okay"
    elif failedAny:
        status["banner"] = "FAILED"
        status["css"] = "bad"
    else:
        status["banner"] = "INCOMPLETE"
        status["css"] = "warn"

    if(request.POST.get('mybutton')):
        comment = ""
        if not p.comments == "":
            comment += "\n"
        comment += str(timezone.now().date()) + " " + str(timezone.now().hour) + "." + str(timezone.now().minute) + ": " + request.POST.get('comment')
        p.comments += comment
        p.save()

    return render(request, 'qie_cards/detail.html', {'card': p,
                                                     'attempts':attempts,
                                                     'locations':locations,
                                                     'status':status,
                                                    })


class PlotView(generic.ListView):
    """ This displays various plots of data """
    
    template_name = 'qie_cards/plots.html'
    context_object_name= 'images'
    def get_queryset(self):
        return listdir('/home/django/testing_database/media/plots')

def testDetail(request, card, test):
    try:
        qieCard = QieCard.objects.get(barcode=card)
    except QieCard.DoesNotExist:
        raise Http404("QIE card does not exist")
    try:
        curTest = Test.objects.get(name=test)
    except QieCard.DoesNotExist:
        raise Http404("QIE card does not exist")

    attemptList = list(Attempt.objects.filter(card=qieCard, test_type=curTest).order_by("attempt_number").reverse())
    attemptData = []
    for attempt in attemptList:
        data = ""
        if not str(attempt.hidden_log_file) == "default.png":
            inFile = open(path.join(MEDIA_ROOT, str(attempt.hidden_log_file)), "r")
            tempDict = json.load(inFile)
            if attempt.test_type.abbreviation == "overall pedestal": 
                data = tempDict["TestOutputs"]["pedResults"]
            elif attempt.test_type.abbreviation == "overall charge injection": 
                data = tempDict["TestOutputs"]["ciResults"]
            elif attempt.test_type.abbreviation == "overall phase scan":
                data = tempDict["TestOutputs"]["phaseResults"]
            elif attempt.test_type.abbreviation == "overall shunt scan":
                data = tempDict["TestOutputs"]["shuntResults"]
            elif "ResultStrings" in tempDict:
                data = tempDict["ResultStrings"][attempt.test_type.abbreviation]
        attemptData.append((attempt, data))

    return render(request, 'qie_cards/testDetail.html', {'card': qieCard,
                                                         'test': curTest,
                                                         'attempts': attemptData,
                                                        })


