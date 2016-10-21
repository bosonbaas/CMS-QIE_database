#!/usr/local/bin/python
# Update Firmware Versions and Verify Readout Modules

import sqlite3
import os
import sys
import time
from shutil import copyfile
import django
import json
from pprint import pprint

sys.path.insert(0, '/home/django/testing_database/card_db')
django.setup()

from qie_cards.models import QieCard, ReadoutModule, Location, RmLocation

def printRMFW(rm):
    output = "{0} - {1} {2} {3} - {4} {5}"
    print output.format(rm.card_1, rm.card_1.bridge_major_ver, rm.card_1.bridge_minor_ver, rm.card_1.bridge_other_ver,
                        rm.card_1.igloo_major_ver, rm.card_1.igloo_minor_ver)
    print output.format(rm.card_2, rm.card_2.bridge_major_ver, rm.card_2.bridge_minor_ver, rm.card_2.bridge_other_ver,
                        rm.card_2.igloo_major_ver, rm.card_2.igloo_minor_ver)
    print output.format(rm.card_3, rm.card_3.bridge_major_ver, rm.card_3.bridge_minor_ver, rm.card_3.bridge_other_ver,
                        rm.card_3.igloo_major_ver, rm.card_3.igloo_minor_ver)
    print output.format(rm.card_4, rm.card_4.bridge_major_ver, rm.card_4.bridge_minor_ver, rm.card_4.bridge_other_ver,
                        rm.card_4.igloo_major_ver, rm.card_4.igloo_minor_ver)

# Update QIE Card Bridge Firmware in database
def updateBridge(card, fw):
    b_fw = fw.split(' ')
    card.bridge_major_ver = "0x" + b_fw[0][-1:].zfill(2)
    card.bridge_minor_ver = "0x" + b_fw[1][-1:].zfill(2)
    card.bridge_other_ver = "0x" + b_fw[2][-4:].zfill(2)
    card.save()

# Update QIE Card Igloo Firmware in database
def updateIgloo(card, fw):
    i_fw = fw.split(' ')
    card.igloo_major_ver = "0x" + i_fw[0][-1:].zfill(2)
    card.igloo_minor_ver = "0x" + i_fw[1][-1:].zfill(2)
    card.save()

def main():
    # Enter an rbx run file to process 
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
        rbx = fileName[-2:]
        rbx = str(int(rbx))
        print "File: {0}".format(fileName)
        print "RBX: {0}".format(rbx)
        with open(fileName) as dataFile:
            data = json.load(dataFile)
        #pprint(data)
        
        # Get RM Unique IDs from File and RM Objects from Database
        readMods = ReadoutModule.objects.all()
        qieCards = QieCard.objects.all()
        rm_uid_list = []
        rm_list = []
        rm_slot_list = []
        bridge_fw_list = []
        igloo_fw_list = []
        rm_count = 0
        for i in xrange(1,5):
            b_fw = []
            i_fw = []
            try:
                uid = data["{0}_{1}_RMID".format(rbx,i)]
                try:
                    rm = readMods.get(rm_uid=uid)
                    rm_uid_list.append(uid)
                    rm_list.append(rm)
                    rm_slot_list.append(i)
                    print "RM_{0}: {1} --- {2}".format(i, uid, rm)
                    for j in xrange(4):
                        b_fw.append(data["{0}_{1}_BRIDGE_FW_{2}".format(rbx,i,j)])
                        i_fw.append(data["{0}_{1}_IGLOO_FW_{2}".format(rbx,i,j)])
                    bridge_fw_list.append(b_fw)
                    igloo_fw_list.append(i_fw)
                except ReadoutModule.DoesNotExist:
                    print "RM_{0}: {1} does not exist in database".format(i, uid)
            except KeyError:
                print "RM_{0}: Not found in rbx run file".format(i)
        for i, rm in enumerate(rm_list):
            # Initial Location and Firmware 
            current_location = RmLocation.objects.filter(rm=rm).order_by("date_received").reverse()[0].geo_loc
            installed = current_location.split(" ")[0] == "Installed"
            print "\nRM {0}".format(rm)
            print "RM Location: {0}".format(current_location)
            print "Previous Firmware"
            printRMFW(rm)
            card_list = [rm.card_1, rm.card_2, rm.card_3, rm.card_4]
            for j, card in enumerate(card_list):
                b_fw = bridge_fw_list[i][j]
                i_fw = igloo_fw_list[i][j]
                updateBridge(card, b_fw)
                updateIgloo(card, i_fw)
            
            if not installed:
                RmLocation.objects.create(geo_loc="Installed in RBX {0} RM-Slot {1} for B904 Burn-In".format(rbx, rm_slot_list[i]), rm=rm)
            
            # Updated Location and Firmware 
            current_location = RmLocation.objects.filter(rm=rm).order_by("date_received").reverse()[0].geo_loc
            print "RM Location: {0}".format(current_location)
            print "Updated Firmware"
            printRMFW(rm)
            rm_count += 1
        return rm_count
    
    else:
        print "Please provide file name."
        return 0

if __name__ == "__main__":
    result = main()
    print "\nFirmware Updated for {0} Readout Modules\n".format(result)


