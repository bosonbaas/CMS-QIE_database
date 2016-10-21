from django.shortcuts import render
from django.views import generic

from .models import ReadoutModule, RmLocation

# Create your views here.

from django.utils import timezone
from django.http import HttpResponse, Http404
from card_db.settings import MEDIA_ROOT 


class CatalogView(generic.ListView):
    """ This displays a list of all readout modules """
    
    template_name = 'readout_modules/catalog.html'
    context_object_name = 'rm_list'
    def get_queryset(self):
        return ReadoutModule.objects.all().order_by('rm_number')

def catalog(request):
    """ This displays a list of all readout modules """
    rms = ReadoutModule.objects.all().order_by('rm_number')
    count = len(rms)

    return render(request, 'readout_modules/catalog.html', {'rm_list': rms,
                                                            'total_count': count})
def detail(request, rm):
    """ This displays details about a readout module """
    if len(rm) > 4:
        try:
            readoutMod = ReadoutModule.objects.get(rm_uid__endswith=rm)
        except ReadoutModule.DoesNotExist:
            #raise Http404("Readout Module uid " + str(rm) + " does not exist")
            return render(request, 'readout_modules/error.html')
    else:
        try:
            readoutMod = ReadoutModule.objects.get(rm_number=rm)
        except ReadoutModule.DoesNotExist:
            #raise Http404("Readout Module number " + str(rm) + " does not exist")
            return render(request, 'readout_modules/error.html')

    if(request.POST.get('comment_add')):
        comment = ""
        if not readoutMod.comments == "":
            comment += "\n"
        comment += str(timezone.now().date()) + " " + str(timezone.now().hour) + "." + str(timezone.now().minute) + ": " + request.POST.get('comment')
        readoutMod.comments += comment
        readoutMod.save()

    if(request.POST.get('location_add')):
        if len(RmLocation.objects.filter(rm=readoutMod)) < 10:
            RmLocation.objects.create(geo_loc=request.POST.get("location"), rm=readoutMod)

    """ Hopefully a script will update Readout Modules every hour. """
    readoutMod.update()

    locations = RmLocation.objects.filter(rm=readoutMod)

    return render(request, 'readout_modules/detail.html', {'rm': readoutMod,
                                                           'locations': locations
                                                          })


def error(request): 
    """ This displays an error for incorrect barcode or unique id """
    return render(request, 'readout_modules/error.html')

