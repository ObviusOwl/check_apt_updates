from __future__ import absolute_import

from .base_upgrade import UpgradeBase
from .apt_package import AptPackage

class AptUpgrade( UpgradeBase ):
    def __init__(self, nativePackage ):
        super(AptUpgrade, self).__init__()
        self.pkg = nativePackage
        self.package = AptPackage( self.pkg )
    
    def getFromVersionString(self):
        if self.pkg == None or self.pkg.installed == None:
            return ""
        return self.pkg.installed.version
        
    def getToVersionString(self):
        if self.pkg == None or self.pkg.candidate == None:
            return ""
        return self.pkg.candidate.version

    def getSortingKey( self ):
        return self.package.getName().lower()
