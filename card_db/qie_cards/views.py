from django.shortcuts import render
from django.views import generic
import datetime

from .models import QieCard, Tester, Test, Attempt, Location

# Create your views here.

from django.http import HttpResponse


class CatalogView(generic.ListView):
    """ This displays a list of all QIE cards """
    
    template_name = 'qie_cards/catalog.html'
    context_object_name = 'barcode_list'
    def get_queryset(self):
        return QieCard.objects.all().order_by('barcode')


def summary(request):
    """ This displays a summary of the cards """
    print datetime.datetime.now().time()
    cards = list(QieCard.objects.all().order_by('barcode'))
    print "Cards loaded: " + str(datetime.datetime.now().time())
    tests = list(Test.objects.all())
    print "Tests loaded: " + str(datetime.datetime.now().time())
    attempts = list(Attempt.objects.all())
    print "Attempts loaded: " + str(datetime.datetime.now().time())
    
    numTests = len(tests)
    testsToInd = {}

    for i in xrange(numTests):
        testsToInd[tests[i].pk] = i

    state = {}

    for card in cards:
        state[card.pk] = [0] * numTests
    
    print "State initialized: " + str(datetime.datetime.now().time())
    
    for attempt in attempts:
        if not attempt.revoked:
            testInd = testsToInd[attempt.test_type_id];
            if not attempt.num_failed == 0:
                state[attempt.card_id][testInd] = 2
            elif not attempt.num_passed == 0 and state[attempt.card_id][testInd] == 0:
                state[attempt.card_id][testInd] = 1

    print "State computed: " + str(datetime.datetime.now().time())

    cardStat = []

    for i in xrange(len(cards)):
        card = cards[i]
        curFail = []
        curPass = []
        curRem = []
        tempDict = {}
        curState = state[card.pk]

        for i in xrange(numTests):
            if curState[i] == 0:
                curRem.append(tests[i].name)
            elif curState[i] == 1:
                curPass.append(tests[i].name)
            elif curState[i] == 2:
                curFail.append(tests[i].name)
        
        tempDict['barcode'] = card.barcode
        tempDict['failed'] = curFail
        tempDict['passed'] = curPass
        tempDict['remaining'] = curRem
        cardStat.append(tempDict)
    print datetime.datetime.now().time()
        
    return render(request, 'qie_cards/summary.html', {'cards': cardStat})

class TestersView(generic.ListView):
    """ This displays the users and email addresses """
    
    template_name = 'qie_cards/testers.html'
    context_object_name = 'tester_list'
    def get_queryset(self):
        return Tester.objects.all().order_by('username')


class SetupView(generic.ListView):
    """ This displays the tests and their descriptions """

    template_name = 'qie_cards/setup.html'
    context_object_name = 'test_list'
    def get_queryset(self):
        return Test.objects.all().order_by('name')


class StatsView(generic.ListView):
    """ This displays statistics of passed/failed tests """    
    
    template_name = 'qie_cards/stats.html'
    context_object_name = 'c'
    
    def get_queryset(self, **kwargs):
        """ This defines what context is passed to the webpage """
        context = {}
        test_list = Test.objects.all().order_by('name')
        context['test_list'] = test_list
        if test_list:
            context['test_inst'] = test_list[0]
        return context

def stats(request):
    """ This displays a summary of the cards """
    
    attempts = list(Attempt.objects.all())   
    cards = list(QieCard.objects.all().order_by("barcode"))
    tests = list(Test.objects.all()) 
 
    numCards = len(cards)
    cardsToInd = {}

    for i in xrange(numCards):
        cardsToInd[cards[i].pk] = i

    failed = {}

    for test in tests:
        failed[test.pk] = [False] * numCards
    
    for attempt in attempts:
        if not attempt.revoked:
            cardInd = cardsToInd[attempt.card_id]
            if not attempt.num_failed == 0:
                failed[attempt.test_type_id][cardInd] = True

    testStat = []

    for i in xrange(len(tests)):
        tempStat = {"name": tests[i].name}
        failCards = []
        for j in xrange(len(cards)):
            if failed[tests[i].pk][j]:
                failCards.append(cards[j].barcode)
        tempStat["cards"] = failCards
        tempStat["number"] = len(failCards)
        tempStat["percentage"] = round( float(len(failCards))/len(cards) * 100, 1)
        testStat.append(tempStat)
    
    sortedTest = sorted(testStat, key=lambda k: k['percentage'], reverse=True)
    return render(request, 'qie_cards/stats.html', {'tests': sortedTest})
        
def detail(request, card):
    """ This displays details about tests on a card """
    try:
        p = QieCard.objects.get(barcode=card)
    except QieCard.DoesNotExist:
        raise Http404("QIE card does not exist")

    tests = Test.objects.all()
    locations = Location.objects.filter(card=p)
    attempts = {}
    
    for test in tests:
        attempts[test.name] = Attempt.objects.filter(card=p.pk, test_type=test.pk)
        
    return render(request, 'qie_cards/detail.html', {'card': p, 'attempts':attempts, 'locations':locations})
