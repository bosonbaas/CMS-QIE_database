#!/usr/local/bin/python

# Update Readout Module information for QIE Cards every hour.
import sys
import time
import django
import json

sys.path.insert(0, '/home/django/testing_database/card_db')
django.setup()

from qie_cards.models import ReadoutModule, RmLocation

# Update Readout Module Unique IDs and QIE Cards in database
start_time = time.time()
noLoc = 0
assembly = "CERN B904 Clean Room"
for r in ReadoutModule.objects.all():
    l = RmLocation.objects.filter(rm=r).order_by("date_received")
    if len(l) == 0:
        RmLocation.objects.create(geo_loc=assembly, rm=r)
        noLoc += 1
        print "Add location RM {0}".format(r)
    print "RM {0}: {1}".format(r, l.reverse()[0].geo_loc)
        
print "Number of RMs with no location: {0}".format(noLoc)
end_time = time.time()

# Log RM Update
with open('/home/django/testing_database/location_update/location.log', 'a') as log:
    log.write("updated readout module locations %s\n" % time.strftime("%c"))
log.close()

print "Update run time: {0}".format(end_time - start_time)

