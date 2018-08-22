from __future__ import absolute_import

from . import base_report
from os_updates import TableWriter
from os_updates.errors import FatalError

"""
See Also https://nagios-plugins.org/doc/guidelines.html#PLUGOUTPUT
"""

class NagiosUpgradesReport( base_report.BaseReport ):
    
    def __init__(self):
        super(NagiosUpgradesReport, self).__init__()
        self.returncode = 0
        self.upgradeCount = 0
        self.warn_thres = 10
        self.critical_thres = 30
        self.statusMap = {0:"OK",1:"Warning",2:"Critical",3:"Unknown"}
        self.service = "UPDATES"
        
    def getReturncode(self):
        return self.returncode
    
    def setWarnThreshold(self, val):
        self.warn_thres = val

    def setCriticalThreshold(self, val):
        self.critical_thres = val
    
    def getPerfData(self):
        return "label='os updates available'={0};{1};{2};0;0".format( self.upgradeCount, self.warn_thres, self.critical_thres)

    def displayStatusLine(self):
        stat = self.statusMap[ self.returncode ].upper()
        perf = self.getPerfData()
        print( "{0} {1}: {2} Updates available|{3}".format(self.service, stat, self.upgradeCount, perf) )
    
    def displayPackageList(self, pkgMgr):
        for pkg in pkgMgr.upgrades:
            toV = pkg.getToVersionString()
            name = pkg.package.getName()
            print( "{0}-{1}".format( name, toV) )
        
    def rankStatus(self):
        if self.upgradeCount >= self.warn_thres:
            self.returncode = 1
        # critical overrides warn
        if self.upgradeCount >= self.critical_thres:
            self.returncode = 2
    
    def report( self, pkgMgr ):
        self.upgradeCount = len(pkgMgr.upgrades)
        self.rankStatus()
        self.displayStatusLine()
        self.displayPackageList( pkgMgr )
