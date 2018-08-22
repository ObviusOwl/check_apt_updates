updates_mail
=========

Installs and sets up check_apt_updates script for weekly updates mail.
The script is scheduled weekly by crontab on a configurable day of week and hour and a randomized minute.

This role is provided as is. You most certainly want to adapt this role to your needs
or at least carefully study what the role does to your servers before usage.

Requirements
------------

Tested distributions:

- Debian 8, 9
- CentOS 6, 7
- Ubuntu 16.04 LTS, 18.04 LTS
- Linux Mint 18, 19

The servers need to be able to send emails with *sendmail*. This role will not 
install postfix or exim for you!

Role Variables
--------------

### User variables

Role variables with default values:

```yaml
check_updates_git_url: "https://gitlab.terhaak.de/jojo/check_apt_updates.git"
check_updates_app_dir: "/opt/check_apt_updates"
check_updates_launcher_path: "/root/check_updates/cron.sh"
check_updates_important_path: "/root/check_updates/important_packages.list"

check_updates_mail_to: "user@example.com"
check_updates_cron_disable: false
check_updates_cron_minute: "{{ 59 | random}}"
check_updates_cron_hour: 4
check_updates_cron_weekday: 6
check_updates_quiet: false
check_updates_html: true
```

`check_updates_important` is not set by default. This should be a list of 
package names or shell globing patterns matching package names designing 
packages to be considered important and so their updates. 

`check_updates_git_url` is the URL to the GIT repository from where to clone the script.

`check_updates_app_dir` is where the script files are cloned **into**.

`check_updates_launcher_path` path to the shell script file created by the role from the template and which is executed by cron.

`check_updates_important_path` path to the package list file to be considered important.
This file will be created by the role and populated with the content of 
`check_updates_important`

`check_updates_mail_to` email address or space separated list of addresses where to 
send the updates mail to. 

`check_updates_cron_disable` if set to *true*, no crontab entry will be set. Note that 
changing the value to *true* between runs of the role will not remove an existing entry.

`check_updates_cron_minute` the minute when the cron job should run. Defaults to a random number.

`check_updates_cron_hour` hour when the cron job should run.

`check_updates_cron_weekday` weekday when the cronjob should run.

`check_updates_quiet` use quiet mode of the script. No mail wil be send if no updates are 
available. This will also install s-nail or heirloom mailx, because standard sendmail 
will not work with this mode.

`check_updates_html` send html mails. If set to false, a plain text mail containing 
a UTF-8 table will be send.

### Internal tunables

Make sure to understand the complete role before changing these:

```yaml
check_updates_python_executable: "/usr/bin/python3"
check_updates_mailer_quiet_pkg: "s-nail"
check_updates_mailer_quiet_cmd: "/usr/bin/s-nail -# -t -S skipemptybody"
check_updates_mailer_cmd: "/usr/sbin/sendmail -t -i"
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
  vars:
    check_updates_mail_to: "me@example.com"
    check_updates_important: 
      - gitlab-ce:amd64
  roles:
    - updates_mail
```

License
-------

BSD