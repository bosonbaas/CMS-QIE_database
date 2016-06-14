import django
django.setup()
import sys
from django.utils import timezone
from qie_cards.models import *

#file name of report
file_name = sys.argv[1]

#open file and read it into string for parsing
infile = open(file_name, "r")
s = infile.read()

#split into header and individual card info
l = s.split("\n\n")

#split into individual info and tests
for i in xrange(0, len(l)):
    l[i] = l[i].split("\n")

#dict for plane location
geo_loc_set = {"RM1": {"0x19": "J2", "0x1a": "J3", "0x1b": "J4", "0x1c": "J5"},
               "RM2": {"0x19": "J7", "0x1a": "J8", "0x1b": "J9", "0x1c": "J10"},
               "RM3": {"0x19": "J18", "0x1a": "J19", "0x1b": "J20", "0x1c": "J21"},
               "RM4": {"0x19": "J23", "0x1a": "J24", "0x1b": "J25", "0x1c": "J26"},}

#initialize data list
data = []

#format data into neatly sorted list of dicts
for i in xrange(1, len(l)):
    temp = {"uid": l[i][2],
            "geo location": "14th floor Wilson Hall",
            "plane location": geo_loc_set[l[i][0]][l[i][1]],
            "Tests": []}
    j = 3
    while j < len(l[i])-1:
        sub = [l[i][j], l[i][j+1]]
        j = j + 2
        temp["Tests"].append(sub)
    data.append(temp)

#retrive tester object to put into attempts
try:
    tester = Tester.objects.get(username=l[0][0])
except:
    sys.exit("tester not valid exiting")

#loop through all elements in data
for i in data:
    #retrive card info but creates a new one if
    #one is not found
    try:
        temp_card = QieCard.objects.get(uid=i["uid"])
    except:
        #if creating new card enter card id for new card
        #this may change in the future the current method
        #is only for testing
        print "Please enter the card id for the card in ", i["plane location"]
        done = False
        while not done:
            try:
                temp_id = raw_input()
                validate_id(temp_id)
                if QieCard.objects.filter(card_id=temp_id):
                    print "ID already in use"
                else:
                    done = True
            except ValidationError, e:
                print "Invalid ID: " + str(e[0])
        #create and save new qie card
        temp_card = QieCard(uid=i["uid"],
                            geo_loc=i["geo location"],
                            plane_loc=i["plane location"],
                            card_id=temp_id)
        temp_card.save()
    
    print i["plane location"] + ": " + temp_card.card_id
    #loops through each test to create an event
    #for each test
    for j in i["Tests"]:
        #retrieve test info for what test was ran
        #in this attempt quits if not found
        try:
            temp_test = Test.objects.get(abbreviation=j[0])
        except:
            sys.exit("test not valid exiting")
        #find out if there were previous attempts
        #and counts them
        prev_attempts = Attempt.objects.filter(card=temp_card, test_type=temp_test)
        attempt_num = len(prev_attempts) + 1
        #creates a bool varible to pass to attempts
        if j[1] == "PASS":
            flag = True
        else:
            flag = False
        #create attempt
        temp_attempt = Attempt(card=temp_card,
                               test_type=temp_test,
                               attempt_number=attempt_num,
                               tester=tester,
                               date_tested=timezone.now(),
                               passed=flag)
        #save attempt into database
        temp_attempt.save()
