#!/usr/local/bin/python

# Update Readout Module information for QIE Cards every hour.
import sys
import time
import django
import json

sys.path.insert(0, '/home/django/testing_database/card_db')
django.setup()

from qie_cards.models import ReadoutModule

# Update Readout Module Unique IDs and QIE Cards in database
start_time = time.time()
rm_dict = {}
for rm in ReadoutModule.objects.all():
    rm.update()
    rm_dict[rm.rm_number] = rm.rm_uid
end_time = time.time()

# Log RM Update
with open('/home/django/testing_database/rm_update/rmUpdateLog.txt', 'a') as log:
    log.write("updated readout modules %s\n" % time.strftime("%c"))
log.close()

# Output Readout Module json file
with open('/home/django/testing_database/rm_update/rm.json', 'w') as j:
    json.dump(rm_dict, j)
j.close()

print "Update run time: {0}".format(end_time - start_time)

