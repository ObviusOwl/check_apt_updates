#!/usr/bin/env python3
import shutil
import socket
import argparse

from errors import FatalError
import TableWriter
import apt

class app(object):
    def __init__(self):
        self.apt_upgrade = apt.apt_upgrade()
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
    
    def load_upgrades(self):
        self.upgrades = self.apt_upgrade.get_upgrades()
    
    def print_report(self):
        if self.upgrades == None:
            raise FatalError( "no upgrade data available, run load_upgrades()" )
        table = TableWriter.TableWriter()
        table.width = shutil.get_terminal_size( (100,24)  ).columns
        
        table.appendRow( [ "package", "old version", "new version"] )
        for u in self.upgrades["upgrades"]:
            table.appendRow( [ u["package"], u["old_version"], u["new_version"] ] )
        table.setConf( 0, None, "heading", True)
        
        print( "There are {} updates available for {}".format( 
            self.upgrades["nb_upgraded"], self.hostname) )
        print("\n------------------")
        print( self.upgrades["raw_stats"] )
        print( self.upgrades["raw_download_size"] )
        print( self.upgrades["raw_install_size"] )
        print("------------------\n")
        print("\nPackages to be upgraded:\n")
        table.print()

    def print_email_headers(self):
        print( "subject: {} updates available for {}".format( 
            self.upgrades["nb_upgraded"], self.hostname) )
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
