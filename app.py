#!/usr/bin/env python3
import shutil
import socket
import argparse
import sys

from errors import FatalError
import TableWriter
import apt

class app(object):
    def __init__(self):
        self.hostname = socket.getfqdn()
        self.upgrades = None
        self.email_to = "root"
        self.email_from = "root"
        self.subcommand = "list"
        self.warn_thres = 10
        self.critical_thres = 30
        self.returncode = 0
        self.use_colors = True;
        self.colors = {
            "default": "\033[39m", "red": "\033[31m", "green": "\033[32m", 
            "yellow" : "\033[33m", "blue": "\033[34m", "magenta": "\033[35m",
            "light_red": "\033[91m", "light_green": "\033[92m", 
            "light_yellow": "\033[93m", "light_blue": "\033[94m"
        }
        
    def parse_args(self):
        parser = argparse.ArgumentParser(description='Check apt-get upgrade and format an email.')
        subparsers = parser.add_subparsers(dest="sub_command")
        
        parser_mail = subparsers.add_parser('mail', help='Outputs the update list packed as email')
        parser_mail.add_argument('--to', action='store', dest="email_to", nargs=1, default=["root",], 
                            help="Email address to use in the 'to' header", metavar="EMAIL" )
        parser_mail.add_argument('--from', action='store', dest="email_from", nargs=1, default=["root",],
                            help="Email address to use in the 'from' header", metavar="EMAIL" )
        parser_mail.add_argument('--headers', action='store_true', dest="email_headers_enable", default=False, 
                            help="Enable email header output for direct piping into sendmail" )

        parser_nag = subparsers.add_parser('nagios', help='Act as a nagios plugin.')
        parser_nag.add_argument('-w', "--warn", action='store', dest="warn", nargs=1, type=int, default=[10,], 
                            help="Output a warning when there are more than NUM updates available.", metavar="NUM" )
        parser_nag.add_argument('-c', "--crirical", action='store', dest="critical", nargs=1, type=int, default=[30,], 
                            help="Ouptut critical status when there are more than NUM updates available.", metavar="NUM" )

        parser_list = subparsers.add_parser('list', help='List the updates in a terminal friendly way')
        parser_list.add_argument('--no-colors', action='store_true', dest="no_color", default=False, 
                            help="Do not use colors in terminal output")

        args = parser.parse_args()
        if args.sub_command == "mail":
            self.email_to = args.email_to[0]
            self.email_from = args.email_from[0]
            self.email_enable = args.email_headers_enable
        elif args.sub_command == "nagios":
            self.warn_thres = args.warn[0]
            self.critical_thres = args.critical[0]
        elif args.sub_command == "list":
            self.use_colors = sys.stdout.isatty() and not args.no_color
        self.subcommand = args.sub_command
        

    def format_filesize(self, num):
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "{:.1f}{}B".format(num, unit)
            num /= 1024.0
        return "{:.1f}YiB".format(num)
    
    def load_upgrades(self):
        cache = apt.Cache()
        cache.update()
        cache.open(None)
        cache.upgrade()
        self.upgrades = cache.get_changes()
        cache.close()
    
    def print_report(self):
        if self.subcommand == "mail":
            self.print_email()
        elif self.subcommand == "nagios":
            self.print_nagios()
        elif self.subcommand == "list":
            self.print_list()
        
    def print_nagios(self):
        if self.upgrades == None:
            raise FatalError("updates not loaded")
        if len(self.upgrades) >= self.warn_thres:
            self.returncode = 1
        # critical overrides warn
        if len(self.upgrades) >= self.critical_thres:
            self.returncode = 2
        print("{} Updates available".format(len(self.upgrades)))

    def print_list(self):
        if self.upgrades == None:
            raise FatalError("updates not loaded")
        for pkg in self.upgrades:
            if self.use_colors:
                print("{}{}{} ({} => {})".format(
                    self.colors["green"],
                    pkg.fullname, 
                    self.colors["default"],
                    pkg.installed.version , pkg.candidate.version))
            else:
                print("{} ({} => {})".format(pkg.fullname, pkg.installed.version , pkg.candidate.version))
        
    def print_email(self):
        if self.upgrades == None:
            raise FatalError("updates not loaded")
        if self.email_enable:
            self.print_email_headers()
        
        table = TableWriter.TableWriter()
        table.width = shutil.get_terminal_size( (100,24)  ).columns
        
        table.appendRow( [ "package", "old version", "new version"] )
        stats = {"upgrades":0, "downgrades":0, "installs":0, "deletions":0, "size":0, "installed_size":0, "curr_installed_size":0 }
        for pkg in self.upgrades:
            if pkg.marked_upgrade:
                stats["upgrades"] += 1
            elif pkg.marked_downgrade:
                stats["downgrades"] += 1
            elif pkg.marked_install:
                stats["installs"] += 1
            elif pkg.marked_delete:
                stats["deletions"] += 1
            stats["size"] += pkg.candidate.size
            stats["installed_size"] += pkg.candidate.installed_size
            stats["curr_installed_size"] += pkg.installed.installed_size
            table.appendRow( [ pkg.fullname, pkg.installed.version , pkg.candidate.version ] )
        table.setConf( 0, None, "heading", True)
        
        print( "There are {} updates available for {}".format( 
            len(self.upgrades), self.hostname) )
        print("\n------------------")
        print( "Packages to upgrade: {}".format(stats["upgrades"]) )
        print( "Packages to downgrade: {}".format(stats["downgrades"]) )
        print( "Packages to newly install: {}".format(stats["installs"]) )
        print( "Packages to remove: {}".format(stats["deletions"]) )
        print("------------------")
        print( "Need to download: {}".format( self.format_filesize(stats["size"])) )
        print( "Difference of disk space usage: {}".format( self.format_filesize(stats["installed_size"]-stats["curr_installed_size"])) )
        print("------------------\n")
        print("\nPackages to be upgraded:\n")
        table.print()

    def print_email_headers(self):
        print( "subject: {} updates available for {}".format( 
            len(self.upgrades), self.hostname) )
        print( "from: {}".format(self.email_from))
        print( "to: {}".format(self.email_to) )
        print( "Content-Type: text/plain; charset=\"utf-8\"" )

if __name__ == "__main__":
    try:
        a = app()
        a.parse_args()
        a.load_upgrades()
        a.print_report()
        exit(a.returncode)
    except Exception as e:
        print(e)
        exit(3)
