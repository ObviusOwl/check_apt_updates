
# Examples

Direct piping into sendmail:

```
/opt/check_apt_updates/check_updates.py mail --headers --to foo@example.org | /usr/sbin/sendmail -t -i
```

# Usage

```
usage: check_updates.py [-h] [-H HOST] [-v] [-m {apt,yum,dnf,packagekit}]
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
```

## list subcommand

```
usage: check_updates.py list [-h] [--no-colors] [--colors] [-l]

optional arguments:
  -h, --help   show this help message and exit
  --no-colors  Do not use ANSI colors in terminal output
  --colors     Force ANSI colors in terminal output
  -l, --list   Display a list instead of a table
```

## mail subcommand

```
usage: check_updates.py mail [-h] [--to EMAIL] [--from EMAIL] [--headers]

optional arguments:
  -h, --help    show this help message and exit
  --to EMAIL    Email address to use in the 'to' header
  --from EMAIL  Email address to use in the 'from' header
  --headers     Enable email header output for direct piping into sendmail
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