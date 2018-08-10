from __future__ import absolute_import

from .base_upgrade import UpgradeBase
from .dnf_package import DnfPackage

class DnfUpgrade( UpgradeBase ):
    def __init__(self, nativePackageFrom, nativePackageTo ):
        super(DnfUpgrade, self).__init__()
        self.pkgFrom = nativePackageFrom
        self.pkgTo = nativePackageTo
        self.packageFrom = DnfPackage( nativePackageFrom )
        self.packageTo = DnfPackage( nativePackageTo )
        self.pkg = self.pkgTo
        self.package = self.packageTo
    
    def getFromVersionString(self):
        return self.packageFrom.getVersionString()
        
    def getToVersionString(self):
        return self.packageTo.getVersionString()
    
    def setMeta(self, key, value ):
        self.meta[key] = value
