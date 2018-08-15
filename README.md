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
- Ubuntu 18.04 / Mint 19
- Debian 9
- Fedora 28

# Install

To use the APT backend (on Debian, Ubuntu, Mint, ...) you must install python3-apt: 

```
apt install python3-apt
```

For CentOS or Fedora (YUM, DNF) no extra software (aside python) is needed.

Clone the repository (if you have GIT, else install GIT or download and extract an archive):

```
cd /opt/
git clone https://gitlab.terhaak.de/jojo/check_apt_updates.git
```

Adapt the variables in the launcher script. You may also want to copy the script 
somewhere else (i.e. `/root/bin`). If you want you can also just use this script 
as starting point for an own launcher script.

```
vim check_apt_updates/check_updates.sh
```

Schedule the update checks with cron. Adapt the check frequency to your needs. 

```
vim /etc/crontab
```

```
13      4       *       *       6       root            /opt/check_apt_updates/check_updates.sh
```

# Usage

see [docs/usage.md](docs/usage.md)
