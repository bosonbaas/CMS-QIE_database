import django
djange.setup()

from qie_cards.models import Test, Tester, Attempt, QieCard

file_name = "something for now"

infile = open(file_name, "r")
s = infile.read()

l = s.split("\n\n")

for i in xrange(0, len(imm)):
    l[i] = l[i].split("\n")

geo_loc_set = ["RM1": ["0x19": "J2", "0x1a": "J3", "0x1b": "J4", "0x1c": "J5"],
               "RM2": ["0x19": "J7", "0x1a": "J8", "0x1b": "J9", "0x1c": "J10"],
               "RM3": ["0x19": "J18", "0x1a": "J19", "0x1b": "J20", "0x1c": "J21"],
               "RM4": ["0x19": "J23", "0x1a": "J24", "0x1b": "J25", "0x1c": "J26"],]

data = ["Tester": l[0][0]
