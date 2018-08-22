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

<style type="text/css">
.updates_table{ border-collapse: collapse; }
.updates_table, .updates_table td, .updates_table th, .updates_table tr{ border: 1px solid #eaecea; }
.updates_table td, .updates_table th{ padding: .2em .5em; font-family: monospace; font-size: 1em;}
.updates_table th{ text-align: left; }
.updates_table tr:nth-child(even) { background: #f5f5f5}
.stats_table th{ text-align: right; padding-right:1em; font-weight: normal;}
.stats_table{ margin: 2em 0;}
.important_package{ color:#741f1e; }
</style>
</head>
<body>
<p>There are <b>3</b> updates available for <b>gitlab.example.com</b>.</p>
<table class="stats_table">
<tr><th>Packages to upgrade</th><td>3</td></tr>
<tr><th>Need to download</th><td>420.7MiB</td></tr>
<tr><th>Difference of disk space usage</th><td>-317.0KiB</td></tr>
</table>
<p>Packages to be upgraded:</p>
<table class="updates_table">
<tr><th>package</th><th>old version</th><th>new version</th></tr>
<tr><td><span class="important_package">gitlab-ce:amd64</span></td><td>11.1.<span style='color:#cc9900'>1</span>-ce.0</td><td>11.1.<span style='color:#cc9900'>4</span>-ce.0</td></tr>
<tr><td>busybox:amd64</td><td>1:1.22.0-9+deb8u<span style='color:#cc9900'>1</span></td><td>1:1.22.0-9+deb8u<span style='color:#cc9900'>4</span></td></tr>
<tr><td>mutt:amd64</td><td>1.5.23-3</td><td>1.5.23-3<span style='color:#567b24'>+deb8u1</span></td></tr>
</table>
</body>
</html>

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
