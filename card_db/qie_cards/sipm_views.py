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

def catalog(request):
    """ This displays a list of all SiPM control cards """

    sipms = SipmControlCard.objects.all().order_by('sipm_control_card')
    count = len(sipms)

    return render(request, 'sipm_cards/catalog.html', {'sipm_list': sipms,
                                                       'total_count': count})


def detail(request, sipm_control_card):
    """ This displays details about a calibration unit """
    try:
        sipmCard = SipmControlCard.objects.get(sipm_control_card=sipm_control_card)
    except SipmControlCard.DoesNotExist:
        raise Http404("SiPM Control Card number " + str(sipm_control_card) + " does not exist")

    calibration = sipmCard.get_calibration_data()
    data = []
    for item in calibration:
        temp = { "id"            : str(item[0]),
                 "channel"       : str(item[1]),
                 "V_30"          : str(item[2]),
                 "V_60"          : str(item[3]),
                 "V_70"          : str(item[4]),
                 "slope"         : str(item[5]),
                 "slope_error"   : str(item[6]),
                 "offset"        : str(item[7]),
                 "offset_error"  : str(item[8]),
                 "chi_squared"   : str(item[9])
                 }
        data.append(temp)
    return render(request, 'sipm_cards/detail.html', {'sipm' : sipmCard,
                                                      'data' : data})
