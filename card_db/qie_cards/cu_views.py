from django.shortcuts import render
from django.views import generic

from .models import CalibrationUnit

# Create your views here.

from django.http import HttpResponse, Http404
from card_db.settings import MEDIA_ROOT 


class CatalogView(generic.ListView):
    """ This displays a list of all calibration units """
    
    template_name = 'calibration_units/catalog.html'
    context_object_name = 'cu_list'
    def get_queryset(self):
        return CalibrationUnit.objects.all().order_by('cu_number')

def detail(request, cu_number):
    """ This displays details about a calibration unit """
    try:
        calUnit = CalibrationUnit.objects.get(cu_number=cu_number)
    except CalibrationUnit.DoesNotExist:
        raise Http404("Calibration Unit number " + str(cu_number) + " does not exist")

    return render(request, 'calibration_units/detail.html', {'cu': calUnit})
