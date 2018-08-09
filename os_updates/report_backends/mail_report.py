from __future__ import absolute_import

from . import base_report
from os_updates import TableWriter
from os_updates.errors import FatalError

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

    def printHeaders( self ):
        for k in list( self.headers ):
            print( "{}: {}".format(k, self.headers[k]) )
    
    def printSectionLine( self, force=False ):
        if self.needSectionLine or force:
            print("------------------")
            self.needSectionLine = False

    def format_filesize(self, num):
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "{:.1f}{}B".format(num, unit)
            num /= 1024.0
        return "{:.1f}YiB".format(num)
    
    def report( self, pkgMgr ):
        self.setSubject("{} updates available for {}".format( len(pkgMgr.upgrades), self.hostname) )
        if self.doPrintHeaders:
            self.printHeaders()
        
        table = TableWriter.TableWriter()
        table.appendRow( [ "package", "old version", "new version"] )
        table.setConf( 0, None, "heading", True)
        for pkg in pkgMgr.upgrades:
            table.appendRow( [ pkg.package.getName(), pkg.getFromVersionString() , pkg.getToVersionString() ] )
        
        stats = pkgMgr.getStats()

        print( "There are {} updates available for {}\n".format( 
            len(pkgMgr.upgrades), self.hostname) )
        self.printSectionLine( True )

        sectionLine = False
        if "upgrades" in stats:
            print( "Packages to upgrade: {}".format(stats["upgrades"]) )
            self.needSectionLine = True
        if "downgrades" in stats:
            print( "Packages to downgrade: {}".format(stats["downgrades"]) )
            self.needSectionLine = True
        if "installs" in stats:
            print( "Packages to newly install: {}".format(stats["installs"]) )
            self.needSectionLine = True
        if "deletions" in stats:
            print( "Packages to remove: {}".format(stats["deletions"]) )
            self.needSectionLine = True
        self.printSectionLine()

        if "download_size" in stats:
            print( "Need to download: {}".format( self.format_filesize(stats["download_size"])) )
            self.needSectionLine = True
        if "installed_size" in stats and "curr_installed_size" in stats:
            print( "Difference of disk space usage: {}".format( 
                self.format_filesize(stats["installed_size"]-stats["curr_installed_size"])) )
            self.needSectionLine = True
        self.printSectionLine()

        print("\nPackages to be upgraded:\n")
        table.display()
