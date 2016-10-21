import sqlite3
import os
import sys
import time
from shutil import copyfile
import django

sys.path.insert(0, '/home/django/testing_database/card_db')
django.setup()

from qie_cards.models import SipmControlCard, ReadoutModule
from card_db.settings import MEDIA_ROOT

def get_scc_number(file_name):
    return file_name[12:][:-4]

def get_rm(scc_number):
    for rm in ReadoutModule.objects.all():
        if rm.sipm_control_card == int(scc_number):
            return rm.rm_number
    return -1


# Please provide the data directory of SiPM Control Cards you wish to add to the database.
folder = sys.argv[1]

for file_name in os.listdir(sys.argv[1]):
    scc_number = get_scc_number(file_name)
    #print "SiPM Control Card Number: %s"%scc_number
    try:
        s = SipmControlCard.objects.get(sipm_control_card=scc_number)
        print "SiPM Control Card %s already exists"%scc_number
    except SipmControlCard.DoesNotExist:
        
        copyfile(os.path.join(folder, file_name), os.path.join(MEDIA_ROOT, 'sipm_control_card', file_name))
        
        rm_number = get_rm(scc_number)
        upload = "sipm_control_card/%s"%file_name
        SipmControlCard.objects.create(sipm_control_card=scc_number,
                                       bv_converter_card=-1,
                                       rm_number=rm_number,
                                       comments="",
                                       upload=upload,
                                       )

        print "SiPM Control Card %s created"%scc_number


