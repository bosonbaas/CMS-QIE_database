from django.shortcuts import render
from django.views import generic
import datetime

from .models import QieCard, Tester, Test, Attempt, Location
import custom.filters as filters

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


class SetupView(generic.ListView):
    """ This displays the tests and their descriptions """

    template_name = 'qie_cards/setup.html'
    context_object_name = 'test_list'
    def get_queryset(self):
        return Test.objects.all().order_by('name')


def stats(request):
    """ This displays a summary of the cards """
    
    attempts = list(Attempt.objects.all())   
    cards = list(QieCard.objects.all().order_by("barcode"))
    tests = list(Test.objects.all()) 
 
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
    attempts = {}
    
    for test in tests:
        attempts[test.name] = Attempt.objects.filter(card=p.pk, test_type=test.pk)
        
    return render(request, 'qie_cards/detail.html', {'card': p, 'attempts':attempts, 'locations':locations})

class PlotView(generic.ListView):
    """ This displays various plots of data """
    
    template_name = 'qie_cards/plots.html'
