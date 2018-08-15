#!/bin/bash

# The updates table uses UTF-8 chars for the cell borders.
# Should be available or even already in use on most distros. 
export LC_ALL="en_US.UTF-8"
# see https://stackoverflow.com/questions/492483/setting-the-correct-encoding-when-piping-stdout-in-python
export PYTHONIOENCODING="utf-8"

# Set the receiving email address. May be a mailing list too. 
# Your server should be able to deliver to this address (directly or by relay)
MAIL_TO="root@example.com"

# Adapt this to the path where you installed the app.
CHECK_APT_APP="/opt/check_apt_updates/check_updates.py"

# Select a python interpreter. Use python3 if available.
PY_EXEC="/usr/bin/python2"

# Adapt the command to your need/preference !
$PY_EXEC $CHECK_APT_APP mail --headers --to $MAIL_TO --html | /usr/sbin/sendmail -t -i
