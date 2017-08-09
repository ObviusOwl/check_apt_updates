#!/usr/bin/env python3
import shutil
import socket
import argparse

from errors import FatalError
import TableWriter
import apt

class app(object):
    def __init__(self):
        self.hostname = socket.getfqdn()
        self.upgrades = None
        self.email_to = "root"
        self.email_from = "root"
        
    def parse_args(self):
        parser = argparse.ArgumentParser(description='Check apt-get upgrade and format an email')
        parser.add_argument('--to', action='store', dest="email_to", nargs=1, default=["root",], 
                            help="Email address to use in the 'to' header", metavar="EMAIL" )
        parser.add_argument('--from', action='store', dest="email_from", nargs=1, default=["root",],
                            help="Email address to use in the 'from' header", metavar="EMAIL" )
        parser.add_argument('--headers', action='store_true', dest="email_headers_enable", default=False, 
                            help="Enable email header output for direct piping into sendmail" )
        args = parser.parse_args()
        self.email_to = args.email_to[0]
        self.email_from = args.email_from[0]
        self.email_enable = args.email_headers_enable

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
        if self.upgrades == None:
            raise FatalError("updates not loaded")
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
    a = app()
    a.parse_args()
    a.load_upgrades()
    if a.email_enable:
        a.print_email_headers()
    a.print_report()
