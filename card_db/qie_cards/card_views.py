import sqlite3
from django.shortcuts import render
from django.views import generic
import datetime
from os import listdir, path
import json
from sets import Set

from .models import QieCard, Tester, Test, Attempt, Location, QieShuntParams 
import custom.filters as filters

# Create your views here.

from django.utils import timezone
from django.http import HttpResponse, Http404
from card_db.settings import MEDIA_ROOT, CACHE_DATA 


class CatalogView(generic.ListView):
    """ This displays a list of all QIE cards """
    
    template_name = 'qie_cards/catalog.html'
    context_object_name = 'barcode_list'
    cards = QieCard.objects.all().order_by('barcode')
    num_cards = len(cards)
    def get_queryset(self):
        return self.cards
#    def length(self):
#        return len(self.cards)

def catalog(request):
    """ This displays a list of all QIE cards """
    cards = QieCard.objects.all().order_by('barcode')
    count = len(cards)

    return render(request, 'qie_cards/catalog.html', {'barcode_list': cards,
                                                      'total_count': count})

def summary(request):
    """ This displays a summary of the cards """
    if CACHE_DATA:
        cache = path.join(MEDIA_ROOT, "cached_data/summary.json")
        print "opening JSON"
        infile = open(cache, "r")
        print "opened JSON"
        print "Loading JSON"
        cardStat = json.load(infile)
        print "JSON Loaded"
    else:
        print "Loading Cards"
        cards = list(QieCard.objects.all().order_by('barcode'))
        print "Loaded Cards"
        print "Loading Tests"
        tests = list(Test.objects.all())
        print "Loaded Tests"
        print "Loading Attempts"
        attempts = list(Attempt.objects.all())
        print "Loaded Attempts"
        print "Getting States!"
        cardStat = filters.getCardTestStates(cards, tests, attempts)
        print "Got 'em!"
    
    return render(request, 'qie_cards/summary.html', {'cards': cardStat})


def calibration(request, card):
    """ This displays the calibration overview for a card """
    if len(card) > 7:
        try:
            p = QieCard.objects.get(uid__endswith=card)
        except QieCard.DoesNotExist:
            raise Http404("QIE card with unique id " + str(card) + " does not exist")
    else:
        try:
            p = QieCard.objects.get(barcode__endswith=card)
        except QieCard.DoesNotExist:
            raise Http404("QIE card with barcode " + str(card) + " does not exist")

    calibrations = p.qieshuntparams_set.all().order_by("group")

    return render(request, 'qie_cards/calibration.html', {'card': p, 'cals': list(calibrations)})

def calResults(request, card, group):
    """ This displays the calibration results for a card """
    if len(card) > 7:
        try:
            p = QieCard.objects.get(uid__endswith=card)
        except QieCard.DoesNotExist:
            raise Http404("QIE card with unique id " + str(card) + " does not exist")
    else:
        try:
            p = QieCard.objects.get(barcode__endswith=card)
        except QieCard.DoesNotExist:
            raise Http404("QIE card with barcode " + str(card) + " does not exist")
    calibration = p.qieshuntparams_set.get(group=group)

    if str(calibration.results) != "default.png":
        conn = sqlite3.connect(path.join(MEDIA_ROOT, str(calibration.results)))
        c = conn.cursor()
        c.execute("select * from qieshuntparams")
        data = []
        for item in c:
            temp = { "id":str(item[0]),
                     "serial":str(p.barcode),
                     "qie":str(item[2]),
                     "capID":str(item[3]),
                     "range":str(item[4]),
                     "shunt":str(item[5]),
                     "date":str(item[7]),
                     "slope":str(item[8]),
                     "offset":str(item[9]),
                    }
            data.append(temp)
    return render(request, 'qie_cards/cal_results.html', {'card': p,
                                                          'data': data,
                                                         })

def calPlots(request, card, group):
    """ This displays the calibration plots for a card """
    if len(card) > 7:
        try:
            p = QieCard.objects.get(uid__endswith=card)
        except QieCard.DoesNotExist:
            raise Http404("QIE card with unique id " + str(card) + " does not exist")
    else:
        try:
            p = QieCard.objects.get(barcode__endswith=card)
        except QieCard.DoesNotExist:
            raise Http404("QIE card with barcode " + str(card) + " does not exist")
    calibration = p.qieshuntparams_set.get(group=group)

    files = []

    if str(calibration.plots) != "default.png" and path.isdir(path.join(MEDIA_ROOT, str(calibration.plots))):
        for f in listdir(path.join(MEDIA_ROOT, str(calibration.plots))):
            files.append(path.join(calibration.plots.url, path.basename(f)))
    else:
        files.append("No Data!")
    return render(request, 'qie_cards/cal_plots.html', {'card': p,
                                                        'plots': files,
                                                         })
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
   
    # Get required attempts and tests
    if CACHE_DATA:
        cache = path.join(MEDIA_ROOT, "cached_data/stats.json")
        infile = open(cache, "r")
        statistics = json.load(infile)
    else:
        attempts = []
        tests = list(Test.objects.filter(required=True))
        
        for test in tests:
            attempts.extend(list(test.attempt_set.all())) 
                
        cards = list(QieCard.objects.all().order_by("barcode"))

        testFailedStats = filters.getFailedCardStats(cards, tests, attempts)
        testPassedStats = filters.getPassedCardStats(cards, tests, attempts)
        testRemStats = filters.getRemCardStates(cards, tests, attempts)
        statistics = {'passed': testPassedStats,
                      'failed': testFailedStats,
                      'remaining': testRemStats,
                     }

    return render(request, 'qie_cards/stats.html', statistics)

def detail(request, card):
    """ This displays the overview of tests for a card """
    if len(card) > 7:
        try:
            p = QieCard.objects.get(uid__endswith=card)
        except QieCard.DoesNotExist:
            #raise Http404("QIE card with unique id " + str(card) + " does not exist")
            return render(request, 'qie_cards/error.html')
    else:
        try:
            p = QieCard.objects.get(barcode__endswith=card)
        except QieCard.DoesNotExist:
            #raise Http404("QIE card with barcode " + str(card) + " does not exist")
            return render(request, 'qie_cards/error.html')

    """ A script will update Readout Modules every hour. """
    p.update_readout_module()
    if p.readout_module < 0:
        rm = "Not Installed"
    else:
        rm = p.readout_module
    
    if p.readout_module_slot < 0:
        rm_slot = "Not Installed"
    else:
        rm_slot = p.readout_module_slot

    tests = Test.objects.all()
    locations = Location.objects.filter(card=p)
    attempts = []
    status = {}    

    status["total"] = len(tests.filter(required=True))
    status["passed"] = 0
    failedAny = False
    forcedAny = False

    for test in tests:
        attemptList = Attempt.objects.filter(card=p.pk, test_type=test.pk).order_by("attempt_number")
        if attemptList:
            last = attemptList[len(attemptList)-1]
            if not last.revoked and test.required:
                if last.overwrite_pass:
                    status["passed"] += 1
                    forcedAny = True
                elif last.passed_all():
                    status["passed"] += 1
                else:
                    failedAny = True
            attempts.append({"attempt":last, "valid": True, "required": test.required})
        else:
            attempts.append({"attempt":test.name, "valid": False, "required": test.required})
 
    if status["total"] == status["passed"]:
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

    if(request.POST.get('comment_add')):
        comment = ""
        if not p.comments == "":
            comment += "\n"
        comment += str(timezone.now().date()) + " " + str(timezone.now().hour) + "." + str(timezone.now().minute) + ": " + request.POST.get('comment')
        p.comments += comment
        p.save()

    if(request.POST.get('location_add')):
        if len(Location.objects.filter(card=p)) < 10:
            Location.objects.create(geo_loc=request.POST.get("location"), card=p)

    return render(request, 'qie_cards/detail.html', {'card': p,
                                                     'rm' : rm,
                                                     'rm_slot' : rm_slot,
                                                     'attempts':attempts,
                                                     'locations':locations,
                                                     'status':status,
                                                    })

#class CatalogView(generic.ListView):
#    """ This displays a list of all QIE cards """
#    
#    template_name = 'qie_cards/catalog.html'
#    context_object_name = 'barcode_list'
#    def get_queryset(self):
#        return QieCard.objects.all().order_by('barcode')
#
def error(request): 
    """ This displays an error for incorrect barcode or unique id """
    return render(request, 'qie_cards/error.html')

class PlotView(generic.ListView):
    """ This displays various plots of data """
    
    template_name = 'qie_cards/plots.html'
    context_object_name= 'tests'
    def get_queryset(self):
        return list(Test.objects.all())

def testDetail(request, card, test):
    """ This displays details about a specific test for a card """
    if len(card) > 7:
        try:
            p = QieCard.objects.get(uid__endswith=card)
        except QieCard.DoesNotExist:
            raise Http404("QIE card with unique id " + str(card) + " does not exist")
    else:
        try:
            p = QieCard.objects.get(barcode__endswith=card)
        except QieCard.DoesNotExist:
            raise Http404("QIE card with barcode " + str(card) + " does not exist")
    try:
        curTest = Test.objects.get(name=test)
    except QieCard.DoesNotExist:
        raise Http404("QIE card does not exist")
    
    if(request.POST.get('overwrite_pass')):
        if(request.POST.get('secret') == "pseudo" or request.POST.get('secret') == "pseudopod"):
            attempt = Attempt.objects.get(pk=request.POST.get('overwrite_pass'))
            attempt.overwrite_pass = not attempt.overwrite_pass
            attempt.save()
    
    attemptList = list(Attempt.objects.filter(card=p, test_type=curTest).order_by("attempt_number").reverse())
    attemptData = []
    for attempt in attemptList:
        data = ""
        if not str(attempt.hidden_log_file) == "default.png":
            inFile = open(path.join(MEDIA_ROOT, str(attempt.hidden_log_file)), "r")
            tempDict = json.load(inFile)
            if attempt.test_type.abbreviation == "overall pedestal" and "pedResults" in tempDict["TestOutputs"]: 
                data = tempDict["TestOutputs"]["pedResults"]
            elif attempt.test_type.abbreviation == "overall charge injection" and "ciResults" in tempDict["TestOutputs"]: 
                data = tempDict["TestOutputs"]["ciResults"]
            elif attempt.test_type.abbreviation == "overall phase scan" and "phaseResults" in tempDict["TestOutputs"]:
                data = tempDict["TestOutputs"]["phaseResults"]
            elif attempt.test_type.abbreviation == "overall shunt scan" and "shuntResults" in tempDict["TestOutputs"]:
                data = tempDict["TestOutputs"]["shuntResults"]
            elif "ResultStrings" in tempDict:
                if attempt.test_type.abbreviation in tempDict["ResultStrings"]:
                    data = tempDict["ResultStrings"][attempt.test_type.abbreviation]
        attemptData.append((attempt, data))

    firstTest = []

    return render(request, 'qie_cards/testDetail.html', {'card': p,
                                                         'test': curTest,
                                                         'attempts': attemptData
                                                         })


def fieldView(request):
    """ This displays details about tests on a card """ 
    options = ["barcode",
               "uid",
               "bridge_major_ver",
               "bridge_minor_ver",
               "bridge_other_ver",
               "igloo_major_ver",
               "igloo_minor_ver",
               "comments",
               "last location",
               "Card Status"]
    
    fields = []
    for i in range(5):
        if(request.POST.get('field' + str(i+1))):
            field = request.POST.get('field' + str(i+1))
            if field in options:
                fields.append(field)


    cards = list(QieCard.objects.all().order_by("barcode"))
    items = []
    # Info for "Card Status"
    cache = path.join(MEDIA_ROOT, "cached_data/summary.json")
    infile = open(cache, "r")
    cardStat = json.load(infile)
    num_required = len(Test.objects.filter(required=True))
    
    for i in xrange(len(cards)):
        card = cards[i]
        item = {}
        item["id"] = card.pk
        item["fields"] = []
        for field in fields:
            if field == "last location":
                loc_list = card.location_set.all()
                if len(loc_list) == 0:
                    item["fields"].append("No Locations Recorded")
                else:
                    #item["fields"].append(len(card.location_set.all()))
                    item["fields"].append(card.location_set.all().order_by("date_received").reverse()[0].geo_loc)
            elif field == "Card Status":
                if cardStat[i]["num_failed"] != 0:
                    item["fields"].append("FAILED")
                elif cardStat[i]["num_passed"] == num_required:
                    if cardStat[i]["forced"]:
                        item["fields"].append("GOOD (FORCED)")
                    else:
                        item["fields"].append("GOOD")
                else:
                    item["fields"].append("INCOMPLETE")
            else:
                item["fields"].append(getattr(card, field))

        items.append(item)

    return render(request, 'qie_cards/fieldView.html', {'fields': fields, "items": items, "options": options})

