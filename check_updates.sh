#!/bin/bash
MAIL_TO=jojo@terhaak.de
CHECK_APT_APP=/opt/check_apt_updates/app.py

/usr/bin/apt-get -qq --assume-no update
$CHECK_APT_APP --headers --to $MAIL_TO | /usr/sbin/sendmail -t -i