from django.shortcuts import render
from django.views import generic

from .models import QieCard, Tester, Test, Attempt, Location

# Create your views here.

from django.http import HttpResponse


class CatalogView(generic.ListView):
    """ This displays a list of all QIE cards """
    
    template_name = 'qie_cards/catalog.html'
    context_object_name = 'barcode_list'
    def get_queryset(self):
        return QieCard.objects.all().order_by('barcode')


class SummaryView(generic.ListView):
    """ This displays the states of tests for each QIE card """

    template_name = 'qie_cards/summary.html'
    context_object_name = 'card_list'
    def get_queryset(self):
        return QieCard.objects.all().order_by('barcode')


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
