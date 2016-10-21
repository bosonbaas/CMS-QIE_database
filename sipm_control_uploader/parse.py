#!/usr/local/bin/python
import sys

# Please provide the name of the current data file followed by the name of the directory where parsed files will be written.
script, data_file, data_directory = sys.argv
print "Data file: {0}".format(data_file)

with open(data_file, "r") as data:
    i = 1
    count = 0
    data_string = ""
    for line  in data:
        if data_string == "":
            scb_number = line.split(",")[0][3:]
            upload_file = "%s/calibration_%s.txt"%(data_directory, scb_number)
        data_string += line
        if line == "\n":
            with open(upload_file, 'w') as f:
                f.write(data_string)
                print "Created file: %s"%upload_file
            count += 1
            data_string = ""
        i += 1
    print "Number of SiPM Control Cards: {0}".format(count)

    #with open("uploads/test.txt", "w") as f:
    #    f.write(line)
    #    print "Created file: {0}".format("file name")

