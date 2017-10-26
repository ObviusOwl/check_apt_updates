# Install

```
apt install python3-apt
```

```
cd /opt/
git clone https://gitlab.terhaak.de/jojo/check_apt_updates.git
```

```
vim check_apt_updates/check_updates.sh
```

```
vim /etc/crontab
```

```
13      4       *       *       6       root            /opt/check_apt_updates/check_updates.sh
```

# Usage

```
/opt/check_apt_updates/app.py --help

usage: app.py [-h] {mail,nagios,list} ...

Check apt-get upgrade and format an email.

positional arguments:
  {mail,nagios,list}
    mail              Outputs the update list packed as email
    nagios            Act as a nagios plugin.
    list              List the updates in a terminal friendly way

optional arguments:
  -h, --help          show this help message and exit
```
