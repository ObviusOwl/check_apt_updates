#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import socket
import argparse
import sys
import os.path
import traceback
import logging
import logging.handlers

from os_updates.errors import FatalError
from os_updates.report_backends.mail_report import MailUpgradesReport
from os_updates.report_backends.cmd_report import CommandlineUpgradesReport
from os_updates.report_backends.nagios_report import NagiosUpgradesReport

class app(object):
    def __init__(self):
        # LOGGING
        self.logger = logging.getLogger() # root instance
        self.logFormatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
        self.logHandler = logging.StreamHandler()
        self.logHandler.setLevel( logging.ERROR )
        self.logHandler.setFormatter( self.logFormatter )
        self.logger.setLevel( logging.ERROR )
        self.logger.addHandler( self.logHandler )

        # status
        self.hostname = socket.getfqdn()
        self.pkgMgr = None
        self.subcommand = "list"
        self.returncode = 0

        # config
        self.email_to = "root"
        self.email_from = "root"
        self.email_html = False
        self.email_print_headers = False
        self.force_package_manager = None
        self.report_type = None 
        self.warn_thres = 10
        self.critical_thres = 30
        self.use_colors = True;
        self.use_ascii = False
        self.load_file = None
        self.colors = {
            "default": "\033[39m", "red": "\033[31m", "green": "\033[32m", 
            "yellow" : "\033[33m", "blue": "\033[34m", "magenta": "\033[35m",
            "light_red": "\033[91m", "light_green": "\033[92m", 
            "light_yellow": "\033[93m", "light_blue": "\033[94m"
        }
    
    
    def parse_args(self):
        parser = argparse.ArgumentParser(description='Check for package upgrades.')
        parser.add_argument('-H','--hostname', action='store', dest="hostname", default=None, metavar="HOST",
                            help="Override hostname detection used as human readable machine identifier in reports." )
        parser.add_argument('-v', action='count', dest="verbosity", default=0,
                            help="Increase verbosity. Specify from 0 to 3 times for logging levels error, warning, info, debug respecively." )
        parser.add_argument('-m','--manager', action='store', dest="manager", default=None, choices=["apt","yum","dnf","packagekit"],
                            help="Override package manager detection. Use with care!" )
        parser.add_argument('-J','--load-json', action='store', dest="load_json", default=None,
                            help="Load updates form JSON file dumped with 'list --json'" )

        subparsers = parser.add_subparsers(dest="sub_command")
        
        parser_mail = subparsers.add_parser('mail', help='Report updates for email notification.')
        parser_mail.add_argument('--to', action='store', dest="email_to", default="root", 
                            help="Email address to use in the 'to' header", metavar="EMAIL" )
        parser_mail.add_argument('--from', action='store', dest="email_from", default="root",
                            help="Email address to use in the 'from' header", metavar="EMAIL" )
        parser_mail.add_argument('--headers', action='store_true', dest="email_headers_enable", default=False, 
                            help="Enable email header output for direct piping into sendmail" )
        parser_mail.add_argument('--html', action='store_true', dest="email_html_enable", default=False, 
                            help="Format email as HTML message instead of plain UTF-8 text." )
        parser_mail.add_argument('-a','--ascii', action='store_true', dest="ascii_enable", default=False, 
                            help="Only use ASCII characters." )

        parser_nag = subparsers.add_parser('nagios', help='Act as a nagios plugin.')
        parser_nag.add_argument('-w', "--warn", action='store', dest="warn", type=int, default=10, 
                            help="Output a warning when there are more than NUM updates available.", metavar="NUM" )
        parser_nag.add_argument('-c', "--crirical", action='store', dest="critical", type=int, default=30, 
                            help="Ouptut critical status when there are more than NUM updates available.", metavar="NUM" )

        parser_list = subparsers.add_parser('list', help='List the updates in a terminal friendly way')
        color_mutex = parser_list.add_mutually_exclusive_group()
        color_mutex.add_argument('--no-colors', action='store_true', dest="no_color", default=False, 
                            help="Do not use ANSI colors in terminal output")
        color_mutex.add_argument('--colors', action='store_true', dest="color", default=False, 
                            help="Force ANSI colors in terminal output")
    
        list_t_mutex = parser_list.add_mutually_exclusive_group()
        list_t_mutex.add_argument('-l','--list', action='store_true', dest="report_list", default=False, 
                            help="Display a list instead of a table" )
        list_t_mutex.add_argument('-j','--json', action='store_true', dest="report_json", default=False, 
                            help="Output all information as JSON" )
        parser_list.add_argument('-a','--ascii', action='store_true', dest="ascii_enable", default=False, 
                            help="Only use ASCII characters." )

        args = parser.parse_args()
        
        # hostname
        if args.hostname != None:
            self.hostname = args.hostname
        # logging
        verbosityMap = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG ]
        args.verbosity = min( [args.verbosity, 3] )
        self.logHandler.setLevel( verbosityMap[args.verbosity] )
        self.logger.setLevel( verbosityMap[args.verbosity] )
        # package manager override
        if args.manager != None:
            self.force_package_manager = args.manager
        if args.load_json != None:
            self.force_package_manager = "json"
            self.load_file = args.load_json
        if args.ascii_enable:
            self.use_ascii = True

        if args.sub_command == "mail":
            self.email_to = args.email_to
            self.email_from = args.email_from
            self.email_print_headers = args.email_headers_enable
            self.email_html = args.email_html_enable
        elif args.sub_command == "nagios":
            self.warn_thres = args.warn
            self.critical_thres = args.critical
        elif args.sub_command == "list":
            if args.no_color:
                self.use_colors = False
            elif args.color:
                self.use_colors = True
            if args.report_list:
                self.report_type = "list"
            elif args.report_json:
                self.report_type = "json"
        self.subcommand = args.sub_command
    
    def load_upgrades(self):
        import os_updates.pm_backends
        pkgMgrFac = os_updates.pm_backends.PackageManagerFactory()
        self.pkgMgr = pkgMgrFac.backendFactory( self.force_package_manager )
        if self.force_package_manager == "json":
            self.pkgMgr.setFile( self.load_file )
        self.pkgMgr.getUpgrades()
    
    def print_report(self):
        pkgHostName = self.pkgMgr.getHostname()
        if pkgHostName != None:
            self.hostname = pkgHostName

        if self.subcommand == "mail":
            rep = MailUpgradesReport()
            rep.setDoHtml( self.email_html )
            rep.setDoPrintHeaders( self.email_print_headers )
            rep.setFrom( self.email_from )
            rep.setTo( self.email_to )
            rep.setHostname( self.hostname )
            rep.setUseAscii( self.use_ascii )
            rep.report( self.pkgMgr )
        elif self.subcommand == "nagios":
            rep = NagiosUpgradesReport()
            rep.setWarnThreshold( self.warn_thres )
            rep.setCriticalThreshold( self.critical_thres )
            rep.report( self.pkgMgr )
            self.returncode = rep.getReturncode()
        elif self.subcommand == "list":
            rep = CommandlineUpgradesReport()
            rep.setHostname( self.hostname )
            if self.report_type != None:
                rep.setReportType( self.report_type )
            rep.setUseAscii( self.use_ascii )
            rep.setUseColors( self.use_colors )
            rep.report( self.pkgMgr )
        

if __name__ == "__main__":
    try:
        a = app()
        a.parse_args()
        a.load_upgrades()
        a.print_report()
        exit(a.returncode)
    except Exception as e:
        sys.stderr.write( str(e) + "\n" )
        sys.stderr.write( traceback.format_exc() + "\n" )
        sys.stdout.flush()
        exit(3)
