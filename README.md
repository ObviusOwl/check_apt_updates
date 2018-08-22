This is a simple utility for checking for pending package upgrades on most common 
Linux server distributions.

The only thing it does is filling your backlog by reporting the pending updates 
not more and not less. If you want to do more complicated stuff (like automatically 
installing the updates) check out packagekit, ansible, chef, puppet and saltstack.

Best used like a email news letter and then on patch-day as ToDo list:
delete the email after having updated the server and enjoy the list of emails 
in your inbox melting away.

Tested on:

- CentOS 6/7
- Ubuntu 16.04 / 18.04 
- Linux Mint 19
- Debian 8/9
- Fedora 28

# Show case

See [docs/example.html](docs/example.html) for an example of HTML mail produced 
by this script.

# Install

To use the APT backend (on Debian, Ubuntu, Mint, ...) you must install python3-apt: 

```sh
apt install python3-apt
```

For CentOS or Fedora (YUM, DNF) no extra software (aside python) is needed.

Clone the repository (if you have GIT, else install GIT or download and extract an archive):

```sh
git clone https://gitlab.terhaak.de/jojo/check_apt_updates.git /opt/check_apt_updates
```

Adapt the variables in the launcher script. You may also want to copy the script 
somewhere else (i.e. `/root/bin`). If you want you can also just use this script 
as starting point for an own launcher script.

```sh
mkdir /root/check_updates
cp /opt/check_apt_updates/check_updates.sh /root/check_updates/
vim /root/check_updates/check_updates.sh
```

Schedule the update checks with cron. Adapt the check frequency to your needs. 

```sh
vim /etc/crontab
```

```
13      4       *       *       6       root            /root/check_updates/
```

# Usage

See the file [docs/usage.md](docs/usage.md) for the script help pages and some usage examples.

An example Icinga2 set up is described in the file [docs/icinga.md](docs/icinga.md).

There are also two Ansible roles provided as starting point for your own deploy scripts:

- [contrib/ansible/updates_mail/README.md](contrib/ansible/updates_mail/README.md)
- [contrib/ansible/updates_icinga/README.md](contrib/ansible/updates_icinga/README.md)
