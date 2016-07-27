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
