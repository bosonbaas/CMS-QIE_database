#!/bin/bash

# step12.sh: This script manages the caching of database files.
#
# Author:   Andrew Baas
# Credits:  Shaun Hogan, Mason Dorseth, John Lawrence, Jordan Potarf,
#                Andrew Baas
# 
# Version:  1.0
# Maintainer:   Caleb Smith
# Email:    caleb_smith2@baylor.edu
# Status:   Live

###################################################
#               Run Caching scripts               #
###################################################

python summary_json.py
python plots_json.py
python stats_json.py
