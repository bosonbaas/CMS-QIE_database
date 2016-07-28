from django.shortcuts import render
from django.views import generic

from .models import ReadoutModule

# Create your views here.

from django.http import HttpResponse, Http404
from card_db.settings import MEDIA_ROOT 


class CatalogView(generic.ListView):
    """ This displays a list of all readout modules """
    
    template_name = 'readout_modules/catalog.html'
    context_object_name = 'rm_list'
    def get_queryset(self):
        return ReadoutModule.objects.all().order_by('rm_number')

def detail(request, rm_number):
    """ This displays details about a readout module """
    try:
        readoutMod = ReadoutModule.objects.get(rm_number=rm_number)
    except ReadoutModule.DoesNotExist:
        raise Http404("Readout Module number " + str(rm_number) + " does not exist")

    return render(request, 'readout_modules/detail.html', {'rm': readoutMod})
