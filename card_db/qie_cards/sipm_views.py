from django.shortcuts import render
from django.views import generic

from .models import SipmControlCard

# Create your views here.

from django.http import HttpResponse, Http404
from card_db.settings import MEDIA_ROOT 


class CatalogView(generic.ListView):
    """ This displays a list of all SiPM control cards """
    
    template_name = 'sipm_cards/catalog.html'
    context_object_name = 'sipm_list'
    def get_queryset(self):
        return SipmControlCard.objects.all().order_by('sipm_control_card')

def detail(request, sipm_control_card):
    """ This displays details about a calibration unit """
    try:
        sipmCard = SipmControlCard.objects.get(sipm_control_card=sipm_control_card)
    except SipmControlCard.DoesNotExist:
        raise Http404("SiPM Control Card number " + str(sipm_control_card) + " does not exist")

    return render(request, 'sipm_cards/detail.html', {'sipm': sipmCard})
