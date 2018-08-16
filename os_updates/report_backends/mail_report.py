from __future__ import absolute_import

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from xml.sax.saxutils import escape

from . import base_report
from os_updates import TableWriter
from os_updates.errors import FatalError
from os_updates.colordiff import ColorDiff

class MailUpgradesReport( base_report.BaseReport ):
    
    def __init__(self):
        super(MailUpgradesReport, self).__init__()
        self.headers = {
            "From": "root",
            "To": "root",
            "Subject":"",
            "Content-Type": "text/plain; charset=\"utf-8\""
        }
        self.doPrintHeaders = False
        self.hostname = "localhost"
        self.needSectionLine = False
        self.doHtml = False
        self.useAscii = False
    
    def setFrom(self, addr ):
        self.headers["From"] = addr

    def setTo(self, addr ):
        self.headers["To"] = addr
    
    def setSubject(self, msg ):
        self.headers["Subject"] = msg
    
    def setHostname( self, name ):
        self.hostname = name
    
    def setDoPrintHeaders(self, value ):
        self.doPrintHeaders = value

    def setDoHtml(self, value ):
        self.doHtml = value
    
    def setUseAscii( self, value ):
        self.useAscii = value

    def printHeaders( self ):
        for k in list( self.headers ):
            if k == "To":
                print( "{0}: {1}".format(k, ",".join(self.headers[k])) )
            else:
                print( "{0}: {1}".format(k, self.headers[k]) )
    
    def printSectionLine( self, force=False ):
        if self.needSectionLine or force:
            print("------------------")
            self.needSectionLine = False

    def format_filesize(self, num):
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "{0:.1f}{1}B".format(num, unit)
            num /= 1024.0
        return "{0:.1f}YiB".format(num)

    def hasUpgradeTypeMeta( self, pkgMgr ):
        for up in pkgMgr.upgrades:
            if "type" in up.meta:
                return True
        return False
    
    def report( self, pkgMgr ):
        self.sortUpgradeList( pkgMgr.upgrades )
        if self.doHtml:
            return self.reportHtml( pkgMgr )
        return self.reportTxt( pkgMgr )

    def reportTxt( self, pkgMgr ):
        self.setSubject("{0} updates available for {1}".format( len(pkgMgr.upgrades), self.hostname) )
        if self.doPrintHeaders:
            self.printHeaders()

        table = TableWriter.TableWriter()
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

            upType = ""
            if "type" in pkg.meta:
                upType = pkg.meta["type"]
                
            if upgradeTypeCol:
                table.appendRow( [ pkg.package.getName(), upType, fromV , toV ] )
            else:
                table.appendRow( [ pkg.package.getName(), fromV , toV ] )
        
        stats = pkgMgr.getStats()

        print( "There are {0} updates available for {1}\n".format( 
            len(pkgMgr.upgrades), self.hostname) )
        self.printSectionLine( True )

        sectionLine = False
        if "upgrades" in stats:
            print( "Packages to upgrade: {0}".format(stats["upgrades"]) )
            self.needSectionLine = True
        if "downgrades" in stats:
            print( "Packages to downgrade: {0}".format(stats["downgrades"]) )
            self.needSectionLine = True
        if "installs" in stats:
            print( "Packages to newly install: {0}".format(stats["installs"]) )
            self.needSectionLine = True
        if "deletions" in stats:
            print( "Packages to remove: {0}".format(stats["deletions"]) )
            self.needSectionLine = True
        self.printSectionLine()

        if "download_size" in stats:
            print( "Need to download: {0}".format( self.format_filesize(stats["download_size"])) )
            self.needSectionLine = True
        if "installed_size" in stats and "curr_installed_size" in stats:
            print( "Difference of disk space usage: {0}".format( 
                self.format_filesize(stats["installed_size"]-stats["curr_installed_size"])) )
            self.needSectionLine = True
        self.printSectionLine()

        print("\nPackages to be upgraded:\n")
        table.display()
    
    def getHtmlCss(self):
        html = ""
        html += "<style type=\"text/css\">\n"
        html += ".updates_table{ border-collapse: collapse; }\n"
        html += ".updates_table, .updates_table td, .updates_table th, .updates_table tr{ border: 1px solid #eaecea; }\n"
        html += ".updates_table td, .updates_table th{ padding: .2em .5em; font-family: monospace; font-size: 1.5em;}\n"
        html += ".updates_table th{ text-align: left; }\n"
        html += ".updates_table tr:nth-child(even) { background: #f5f5f5}\n"
        html += ".stats_table th{ text-align: right; padding-right:1em; font-weight: normal;}\n"
        html += ".stats_table{ margin: 2em 0;}\n"
        html += ".important_package{ color:#741f1e; }\n"
        html += "</style>\n"
        return html
    
    def getHtmlUpgradeTable( self, pkgMgr ):
        html = ""
        upgradeTypeCol = self.hasUpgradeTypeMeta( pkgMgr )

        html += "<table class=\"updates_table\">\n" 
        if upgradeTypeCol:
            html += "<tr><th>package</th><th>type</th><th>old version</th><th>new version</th></tr>\n" 
        else:
            html += "<tr><th>package</th><th>old version</th><th>new version</th></tr>\n" 

        for pkg in pkgMgr.upgrades:
            fromV = escape(pkg.getFromVersionString())
            toV = escape(pkg.getToVersionString())
            fromV, toV = ColorDiff().colorDiff("html",fromV, toV)
            if pkg.isImportant:
                pName = "<span class=\"important_package\">"+escape(pkg.package.getName())+"</span>"
            else:
                pName = escape(pkg.package.getName())

            upType = ""
            if "type" in pkg.meta:
                upType = escape(pkg.meta["type"])
                
            if upgradeTypeCol:
                html += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>\n".format(pName, upType, fromV , toV)
            else:
                html += "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>\n".format(pName, fromV , toV)
        html += "</table>\n"
        return html

    def reportHtml( self, pkgMgr ):
        stats = pkgMgr.getStats()
        subject = "{0} updates available for {1}".format( len(pkgMgr.upgrades), self.hostname )
        self.setSubject( subject )

        msg = MIMEMultipart('alternative')
        for h in self.headers:
            if h == "To":
                msg[h] = ",".join( self.headers[h] )
            else:
                msg[h] = self.headers[h]
        text = ""
        html = ""

        html += "<!DOCTYPE html>\n<html lang=\"en\">\n"
        html += "<head> <meta charset=\"utf-8\"/>  <title>{0}</title>\n".format( escape(subject) )
        html += self.getHtmlCss()
        html += "</head>\n"
        html += "<body>\n"

        html += "<p>There are <b>{0}</b> updates available for <b>{1}</b>.</p>\n".format( 
            len(pkgMgr.upgrades), escape(self.hostname))

        html += "<table class=\"stats_table\">\n" 
        if "upgrades" in stats:
            html += "<tr><th>Packages to upgrade</th><td>{0}</td></tr>\n".format( stats["upgrades"] )
        if "downgrades" in stats:
            html += "<tr><th>Packages to downgrade</th><td>{0}</td></tr>\n".format( stats["downgrades"] )
        if "installs" in stats:
            html += "<tr><th>Packages to install</th><td>{0}</td></tr>\n".format( stats["installs"] )
        if "deletions" in stats:
            html += "<tr><th>Packages to remove</th><td>{0}</td></tr>\n".format( stats["deletions"] )

        if "download_size" in stats:
            d = self.format_filesize(stats["download_size"])
            html += "<tr><th>Need to download</th><td>{0}</td></tr>\n".format(d) 
        if "installed_size" in stats and "curr_installed_size" in stats:
            d = self.format_filesize(stats["installed_size"]-stats["curr_installed_size"])
            html += "<tr><th>Difference of disk space usage</th><td>{0}</td></tr>\n".format(d) 
        html += "</table>\n" 

        html += "<p>Packages to be upgraded:</p>\n"
        html += self.getHtmlUpgradeTable( pkgMgr )

        html += "</body>\n"
        html += "</html>\n"
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        if self.doPrintHeaders:
            print( str(msg) )
        else:
            print( html )
