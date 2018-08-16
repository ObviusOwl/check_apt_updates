# -*- coding: utf-8 -*-

from __future__ import absolute_import

import difflib

from . import base_report
from os_updates import TableWriter
from os_updates.errors import FatalError
from os_updates.colordiff import ColorDiff

class CommandlineUpgradesReport( base_report.BaseReport ):
    
    def __init__(self):
        super(CommandlineUpgradesReport, self).__init__()
        self.colors = {
            "default"    : "\033[39m",
            "red"         : "\033[31m",
            "green"     : "\033[32m",
            "yellow"     : "\033[33m",
            "blue"         : "\033[34m"
        }
        self.reportType = "table"
        self.useColors = True 
        self.useAscii = False
        self.hostname = "localhost"

    def setReportType(self, t ):
        self.reportType = t

    def setUseColors(self, v ):
        self.useColors = v

    def setHostname( self, name ):
        self.hostname = name

    def setUseAscii( self, value ):
        self.useAscii = value

    def report( self, pkgMgr ):
        self.sortUpgradeList( pkgMgr.upgrades )
        if self.reportType == "table":
            self.reportTable( pkgMgr )
        elif self.reportType == "list":
            self.reportList( pkgMgr )
        elif self.reportType == "json":
            self.reportJson( pkgMgr )
        else:
            raise FatalError( "Invalid command line report type: "+self.reportType )
    
    def hasUpgradeTypeMeta( self, pkgMgr ):
        for up in pkgMgr.upgrades:
            if "type" in up.meta:
                return True
        return False

    def reportTable(self, pkgMgr ):
        table = TableWriter.TableWriter()
        if not self.useColors:
            table.hasColor = False
        if self.useAscii:
            table.border_vert = " | "
            table.border_hor = "-"
            table.border_inter = "+"
            table.empty_char = " "

        upgradeTypeCol = self.hasUpgradeTypeMeta( pkgMgr )
        if upgradeTypeCol:
            table.appendRow( [ "package", "type", "old version", "new version"] )
        else:
            table.appendRow( [ "package", "old version", "new version"] )

        table.setConf( 0, None, "heading", True)
        for pkg in pkgMgr.upgrades:
            fromV = pkg.getFromVersionString()
            toV = pkg.getToVersionString()
            
            if self.useColors:
                fromV, toV = ColorDiff().colorDiff("ansi",fromV, toV)

            upType = ""
            if "type" in pkg.meta:
                upType = pkg.meta["type"]
                
            if upgradeTypeCol:
                table.appendRow( [ pkg.package.getName(), upType, fromV , toV ] )
            else:
                table.appendRow( [ pkg.package.getName(), fromV , toV ] )
                
        table.display()

    def reportList(self, pkgMgr ):
        for pkg in pkgMgr.upgrades:
            fromV = pkg.getFromVersionString()
            toV = pkg.getToVersionString()
            arrow = "➡"

            if self.useColors:
                fromV, toV = ColorDiff().colorDiff("ansi",fromV, toV)
            if self.useAscii:
                arrow = "=>"

            print( "{0}:".format( pkg.package.getName()) )
            if "type" in pkg.meta:
                print( u"\t{0}".format( pkg.meta["type"] ) )
            print( u"\t{0} {1} {2}".format( fromV, arrow, toV) )

    def reportJson(self, pkgMgr ):
        import json
        data = {
            "hostname": self.hostname,
            "package_manager": pkgMgr.name,
            "upgrades": []
        }
        for pkg in pkgMgr.upgrades:
            up = {}
            up["package"] = pkg.package.getName()
            up["from_version"] = pkg.getFromVersionString()
            up["to_version"] = pkg.getToVersionString()
            up["meta"] = pkg.meta
            data["upgrades"].append( up )
        
        print( json.dumps( data, indent=2, separators=(',', ': ')) )