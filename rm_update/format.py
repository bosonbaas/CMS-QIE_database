#!/usr/local/bin/python

# Print readout module unique ids
import json

# Load json file
with open('/home/django/testing_database/rm_update/rm.json', 'r') as f:
    rm_dict = json.load(f)
f.close()

int_rm_dict = {int(rm) : uid for rm, uid in rm_dict.items()}
rmZeros = []
rmCount = 0

# Print RMs
with open('/home/django/testing_database/rm_update/table.txt','w') as t:
    for rm,uid in sorted(int_rm_dict.items()):
        rmCount += 1
        look = ""
        if "000000" in uid:
            look = "<<<"
            rmZeros.append(rm)
        line = "RM_No. {:5d} RM_UID {:27s} {:3s}".format(rm, uid, look)
        t.write(line + '\n')
        #print line
t.close()

# List RMs with zeros
print "Number of Readout Modules {0}".format(rmCount)
print "Readout Modules with '000000' in Unique ID: {0}".format(rmZeros)

