This is a simple utility for checking for pending package upgrades on most common 
Linux server distributions.

The only thing it does is filling your backlog by reporting the pending updates 
not more and not less. If you want to do more complicated stuff (like automatically 
installing the updates) check out packagekit, ansible, chef, puppet and saltstack.

Tested on:

- CentOS 7
- Ubuntu 18.04 / Mint 19
- Debian 9
- Fedora 28

# Install

To use the APT backend (on Debian, Ubuntu, Mint, ...) you must install python3-apt: 

```
apt install python3-apt
```

Clone the repository:

```
cd /opt/
git clone https://gitlab.terhaak.de/jojo/check_apt_updates.git
```

Schedule update checks:

```
vim check_apt_updates/check_updates.sh
```

```
vim /etc/crontab
```

```
13      4       *       *       6       root            /opt/check_apt_updates/check_updates.sh
```

Adapt the shell script:

```
vim /opt/check_apt_updates/check_updates.sh
```

# Usage

see [docs/usage.md](docs/usage.md)
