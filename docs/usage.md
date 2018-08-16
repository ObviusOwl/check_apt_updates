
# Examples

Direct piping into sendmail:

```
/opt/check_apt_updates/check_updates.py mail --headers --to foo@example.org | /usr/sbin/sendmail -t -i
```

Save the updates list to be read later. This can be useful for checking updates in a chroot and 
then using the mail service from the host to send the mail.

```
sudo python3 ./check_updates.py list -j > /tmp/updates.json
sudo python3 ./check_updates.py -J /tmp/updates.json list -l
```

You can specify a list of important packages. Updates of important packages 
are listed first in the table and highlighted in red. This is useful for 
servers hosting specific services and for packages coming from external repos.

content of `important_packages.txt`:

```
gitlab-ce:amd64
```

This file lists one package name per line. Shell style globs are supported (* and ?).

Then check the updates:

```
sudo ./check_updates.py --important-list important_packages.txt mail --html --headers --to user@example.com | sendmail -t -i
```

# Usage

```
usage: check_updates.py [-h] [-H HOST] [-v] [-m {apt,yum,dnf,packagekit}]
                        [-J LOAD_JSON] [-i [PKG [PKG ...]]] [-I FILE]
                        {mail,nagios,list} ...

Check for package upgrades.

positional arguments:
  {mail,nagios,list}
    mail                Report updates for email notification.
    nagios              Act as a nagios plugin.
    list                List the updates in a terminal friendly way

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --hostname HOST
                        Override hostname detection used as human readable
                        machine identifier in reports.
  -v                    Increase verbosity. Specify from 0 to 3 times for
                        logging levels error, warning, info, debug
                        respecively.
  -m {apt,yum,dnf,packagekit}, --manager {apt,yum,dnf,packagekit}
                        Override package manager detection. Use with care!
  -J LOAD_JSON, --load-json LOAD_JSON
                        Load updates form JSON file dumped with 'list --json'
  -i [PKG [PKG ...]], --important [PKG [PKG ...]]
                        List of package names which are considered important.
                        Supports globbing.
  -I FILE, --important-list FILE
                        Path to a file containing package names (one per line)
                        to be considered important. See also --important
```

## list subcommand

```
usage: check_updates.py list [-h] [--no-colors | --colors] [-l | -j] [-a]

optional arguments:
  -h, --help   show this help message and exit
  --no-colors  Do not use ANSI colors in terminal output
  --colors     Force ANSI colors in terminal output
  -l, --list   Display a list instead of a table
  -j, --json   Output all information as JSON
  -a, --ascii  Only use ASCII characters.
```

## mail subcommand

```
usage: check_updates.py mail [-h] [--to [EMAIL [EMAIL ...]]] [--from EMAIL]
                             [--headers] [--html] [-a]

optional arguments:
  -h, --help            show this help message and exit
  --to [EMAIL [EMAIL ...]]
                        Email address(es) to use in the 'to' header. Accepts a
                        space separated list.
  --from EMAIL          Email address to use in the 'from' header
  --headers             Enable email header output for direct piping into
                        sendmail
  --html                Format email as HTML message instead of plain UTF-8
                        text.
  -a, --ascii           Only use ASCII characters.
```

## nagios subcommand

```
usage: check_updates.py nagios [-h] [-w NUM] [-c NUM]

optional arguments:
  -h, --help            show this help message and exit
  -w NUM, --warn NUM    Output a warning when there are more than NUM updates
                        available.
  -c NUM, --crirical NUM
                        Ouptut critical status when there are more than NUM
                        updates available.
```