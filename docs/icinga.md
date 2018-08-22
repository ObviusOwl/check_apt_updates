# Icinga set up example

This guide is intended as example and does not replace a solid knowledge of icinga2 
administration. However this might be the right thing to get you started.

We use a icinga2 top down configuration with satellite instances of icinga 
on each server. All icinga2 configuration is synced down from the master to the clients.

Icinga checks are not run with root privileges, however the check updates script 
needs to be run as root. One approach is to configure password-less sudo for the
icinga user and the script. The approach used in this guide is to separate 
the gathering of the updates list and the evaluation for icinga using the nagios 
report backend. The check updates script has for this purpose an JSON import/export 
functionality.

## Schedule updates check with cron

First we need to install the script on each monitored server. Then we set up the 
check cron job. This is very similar to the email report:

Prepare a executable script file `/root/check_updates/icinga_cron.sh ` with content like this:

```sh
#!/bin/bash
export LC_ALL="en_US.UTF-8"

CHECK_APP="/opt/check_apt_updates/check_updates.py"
PY_EXEC="/usr/bin/python3"
OPTS=""
MAIN_OPTS=""

MAIN_OPTS="$MAIN_OPTS --important-list /root/check_updates/important_packages.list"

$PY_EXEC $CHECK_APP $MAIN_OPTS \
    list -j $OPTS > /var/tmp/check_updates/icinga.json
```

Then in `/etc/crontab`:

```
46 4 * * 1 root /root/check_updates/icinga_cron.sh
```

This can easily be automated with the [Ansible role](../contrib/ansible/updates_icinga/README.md) 
shipped with this repository.

## Configure Icinga2

In the global synced template zone we have:

```
object CheckCommand "os-updates" {
  command = [ "/opt/check_apt_updates/check_updates.py" ]
  arguments = {
    "-J" = {
      required = true
      value = "$os_updates_json_path$"
      description = "Load updates form JSON file dumped with 'list --json'"
      order = -2
    }
    "nagios" = {
      required = true
      skip_key = true
      value = "nagios"
      order = -1
    }
    "-w" = {
      value = "$os_updates_warning$"
      description = "Output a warning when there are more than NUM updates available."
      required = true
    }
    "-c" = {
      value = "$os_updates_critical$"
      description = "Ouptut critical status when there are more than NUM updates available."
      required = true
    }
  }
  vars.os_updates_warning = 10
  vars.os_updates_critical = 20
}
```

Note that here we hard code the installation path of the `check_updates.py` script.
This can be decoupled by using `PluginDir` and a symbolic link on the hosts.

In the masters zone we have distributed over several files:

```
apply Service "os updates" {
  import "generic-service"
  check_command = "os-updates"
  command_endpoint = host.vars.client_endpoint // remote check

  vars.os_updates_warning = 10
  vars.os_updates_critical = 20
  vars.os_updates_json_path = "/var/tmp/check_updates/icinga.json"

  check_interval = 1d
  retry_interval = 2h

  assign where (host.vars.client_endpoint && host.vars.monitoring_type in ["basic"] && host.vars.os == "Linux")
}

object ServiceGroup "os updates" {
  display_name = "OS Update Checks"

  assign where match("os updates", service.name)
}

template Host "basic-host" {
  vars.monitoring_type = "basic"
}

template Host "linux-host" {
  vars.os = "Linux"
}

object Host "foo.example.com" {
  import "generic-host"
  import "basic-host"
  import "linux-host"
  address = name
  vars.client_endpoint = name
}
```