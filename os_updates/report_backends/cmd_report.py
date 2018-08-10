# -*- coding: utf-8 -*-

from __future__ import absolute_import

import difflib

from . import base_report
from os_updates import TableWriter
from os_updates.errors import FatalError

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
        self.hostname = "localhost"

    def setReportType(self, t ):
        self.reportType = t

    def setUseColors(self, v ):
        self.useColors = v

    def setHostname( self, name ):
        self.hostname = name

    def report( self, pkgMgr ):
        if self.reportType == "table":
            self.reportTable( pkgMgr )
        elif self.reportType == "list":
            self.reportList( pkgMgr )
        elif self.reportType == "json":
            self.reportJson( pkgMgr )
        else:
            raise FatalError( "Invalid command line report type: "+self.reportType )
    
    def colorDiff(self, text, n_text):
        """
        https://stackoverflow.com/questions/10775029/finding-differences-between-strings
        """
        seqm = difflib.SequenceMatcher(None, text, n_text)
        output_orig = []
        output_new = []
        for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
            orig_seq = seqm.a[a0:a1]
            new_seq = seqm.b[b0:b1]
            if opcode == 'equal':
                output_orig.append(orig_seq)
                output_new.append(orig_seq)
            elif opcode == 'insert':
                output_new.append( self.colors["green"]+new_seq+self.colors["default"] )
            elif opcode == 'delete':
                output_orig.append( self.colors["red"]+orig_seq+self.colors["default"] )
            elif opcode == 'replace':
                output_new.append( self.colors["yellow"]+new_seq+self.colors["default"] )
                output_orig.append( self.colors["yellow"]+orig_seq+self.colors["default"] )
            else:
                print('Error')
        return ''.join(output_orig), ''.join(output_new)
    
    def hasUpgradeTypeMeta( self, pkgMgr ):
        for up in pkgMgr.upgrades:
            if "type" in up.meta:
                return True
        return False

    def reportTable(self, pkgMgr ):
        table = TableWriter.TableWriter()
        if not self.useColors:
            table.hasColor = False

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
                fromV, toV = self.colorDiff(fromV, toV)

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

            if self.useColors:
                fromV, toV = self.colorDiff(fromV, toV)
            print( "{}:".format( pkg.package.getName()) )
            if "type" in pkg.meta:
                print( u"\t{}".format( pkg.meta["type"] ) )
            print( u"\t{} ➡ {}".format( fromV, toV) )

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