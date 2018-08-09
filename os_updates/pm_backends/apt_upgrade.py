from __future__ import absolute_import

from .base_upgrade import UpgradeBase
from .apt_package import AptPackage

class AptUpgrade( UpgradeBase ):
    def __init__(self, nativePackage ):
        super(AptUpgrade, self).__init__()
        self.pkg = nativePackage
        self.package = AptPackage( self.pkg )
    
    def getFromVersionString(self):
        return self.pkg.installed.version
        
    def getToVersionString(self):
        return self.pkg.candidate.version

