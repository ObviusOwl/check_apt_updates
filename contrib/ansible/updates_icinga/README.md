updates_icinga
=========

Installs and sets up check_apt_updates script for weekly update of the json
cache file read by the icinga checks.

This role is very similar to the *updates_mail* role.

This role is provided as is. You most certainly want to adapt this role to your needs
or at least carefully study what the role does to your servers before usage.

Requirements
------------

Tested distributions:

- Debian 8, 9
- CentOS 6, 7
- Ubuntu 16.04 LTS, 18.04 LTS
- Linux Mint 18, 19

This role will not set up icinga checks!

Role Variables
--------------

### User variables

Role variables with default values:

```yaml
check_updates_git_url: "https://gitlab.terhaak.de/jojo/check_apt_updates.git"
check_updates_app_dir: "/opt/check_apt_updates"
check_updates_icinga_launcher_path: "/root/check_updates/icinga_cron.sh"
check_updates_important_path: "/root/check_updates/important_packages.list"

check_updates_icinga_cron_minute: "{{ 59 | random}}"
check_updates_icinga_cron_hour: 4
check_updates_icinga_cron_weekday: 1

check_updates_icinga_json_path: "/var/tmp/check_updates/icinga.json"
```

`check_updates_important` is not set by default. This should be a list of 
package names or shell globing patterns matching package names designing 
packages to be considered important and so their updates.

`check_updates_git_url` is the URL to the GIT repository from where to clone the script.

`check_updates_app_dir` is where the script files are cloned **into**.

`check_updates_icinga_launcher_path` path to the shell script file created by the role from the template and which is executed by cron.

`check_updates_important_path` path to the package list file to be considered important.
This file will be created by the role and populated with the content of 
`check_updates_important`

`check_updates_icinga_cron_minute` the minute when the cron job should run. Defaults to a random number.

`check_updates_icinga_cron_hour` hour when the cron job should run.

`check_updates_icinga_cron_weekday` weekday when the cronjob should run.

`check_updates_icinga_json_path` path of the JSON file created by the script.
This is the file the check_updates script will read when invoked by icinga.

### Internal tunables

Make sure to understand the complete role before changing these:

```yaml
check_updates_python_executable: "/usr/bin/python3"
```

Dependencies
------------

None, but make sure to keep the configuration common to this role and *updates_mail* 
in sync.

Example Playbook
----------------

```yaml
- hosts: updates_icinga
  gather_facts: True
  remote_user: root
  vars:
    check_updates_important: 
      - gitlab-ce:amd64
  roles:
    - updates_icinga
```

License
-------

BSD