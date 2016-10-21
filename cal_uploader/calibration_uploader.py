import sqlite3
import os
import sys
import time
from shutil import copyfile
import django

sys.path.insert(0, '/home/django/testing_database/card_db')
django.setup()

from qie_cards.models import QieCard, QieShuntParams
from card_db.settings import MEDIA_ROOT

def getUID(uid):
    return uid[2:10] + uid[13:]

folder = sys.argv[1]
download = ""

for file in os.listdir(sys.argv[1]):
    if file.endswith(".tar.gz"):
        download = os.path.join("calibration", os.path.basename(sys.argv[1]), os.path.basename(str(file)))

for file in os.listdir(sys.argv[1]):
    if file.endswith(".db"):
        conn = sqlite3.connect(os.path.join(sys.argv[1], file))
        c = conn.cursor()
        c.execute("select * from qieshuntparams")
        uid = ""
        if c:
            item = c.next()

            uid = getUID(item[0])
            print "Processing card " + uid
            card = QieCard.objects.get(uid=uid)

            # Get the group number
            group = 0
            for i in xrange(100):
                if not QieShuntParams.objects.filter(group=i, card=card):
                    group = i
                    break

            # Store the mapping in the filesystem
            #print "Move " + os.path.join(folder, "calibrationParams_shunt.txt") + " -> " + os.path.join(MEDIA_ROOT, "uploads", card.barcode, str(group) + "calibrationParams_shunt.txt")
            mappings = os.path.join("uploads", card.barcode, str(group) + "calibrationParams_shunt.txt")
            copyfile(os.path.join(folder, "calibrationParams_shunt.txt"), os.path.join(MEDIA_ROOT, "uploads", card.barcode, str(group) + "calibrationParams_shunt.txt"))

            results = os.path.join("calibration", os.path.basename(sys.argv[1]), os.path.basename(file))
            
            plots = os.path.join("calibration", os.path.basename(sys.argv[1]), "shunt/plots", item[0][:10] + "_" + item[0][11:])
            date = item[7] 
            print "Card " + uid + " parameters:"
            print "    barcode     -> " + str(card)
            print "    plotLoc     -> " + str(plots)
            print "    mappingsLoc -> " + mappings
            print "    resultsDB   -> " + results
            print ""
            print "Sample of Callibration values:"
            print "    id     ->" + str(item[0])
            print "    serial ->" + str(item[1])
            print "    qie    ->" + str(item[2])
            print "    capID  ->" + str(item[3])
            print "    range  ->" + str(item[4])
            print "    shunt  ->" + str(item[5])
            print "    date   ->" + str(item[7])
            print "    slope  ->" + str(item[8])
            print "    offset ->" + str(item[9])
            print ""
            print "Looks good (Y/n):"
            response = raw_input()
            failed = response.upper() == "N"

            QieShuntParams.objects.create(card=card,
                                          group=group,
                                          date=date,
                                          plots=plots,
                                          mappings=mappings,
                                          results=results,
                                          download=download,
                                          failed=failed,
                                          )
        conn.close()
