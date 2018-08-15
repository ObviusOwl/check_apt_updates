updates_mail
=========

Installs and sets up check_apt_updates script for weekly updates mail.
The script is scheduled weekly by crontab on a configurable day of week and hour and a randomized minute.

Requirements
------------

APT-based dist: Debian, Ubuntu or Linux Mint.

Role Variables
--------------

Role variables with default values:

```yaml
check_apt_updates_git_url: "https://gitlab.terhaak.de/jojo/check_apt_updates.git"
check_apt_updates_dir: "/opt/check_apt_updates"
mail_to: "jojo@terhaak.de"

cron_hour: 4
cron_weekday: 6
```

Dependencies
------------

None

Example Playbook
----------------

```yaml
- hosts: updates_mail
  gather_facts: True
  remote_user: root
  roles:
    - updates_mail
```

License
-------

BSD