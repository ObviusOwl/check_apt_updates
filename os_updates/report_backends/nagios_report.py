from __future__ import absolute_import

from . import base_report
from os_updates import TableWriter
from os_updates.errors import FatalError

class NagiosUpgradesReport( base_report.BaseReport ):
    
    def __init__(self):
        super(NagiosUpgradesReport, self).__init__()
        self.returncode = 0
        self.warn_thres = 10
        self.critical_thres = 30

    def getReturncode(self):
        return self.returncode
    
    def setWarnThreshold(self, val):
        self.warn_thres = val

    def setCriticalThreshold(self, val):
        self.critical_thres = val
    
    def report( self, pkgMgr ):
        numUpgrades = len(pkgMgr.upgrades)
        if numUpgrades >= self.warn_thres:
            self.returncode = 1
        # critical overrides warn
        if numUpgrades >= self.critical_thres:
            self.returncode = 2
        print("{0} Updates available".format(numUpgrades) )
