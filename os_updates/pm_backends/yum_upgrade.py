from __future__ import absolute_import

from .base_upgrade import UpgradeBase
from .yum_package import YumPackage

class YumUpgrade( UpgradeBase ):
    def __init__(self, nativePackage, fromVersion, toVersion ):
        super(YumUpgrade, self).__init__()
        self.pkg = nativePackage
        self.package = YumPackage( self.pkg )
        self.fromVersion = fromVersion
        self.toVersion = toVersion
    
    def formatVersion(self, ver ):
        #package tuple: (name, arch, epoch, version, release)
        if str(ver[2]) == str('0'):
            return "{0}-{1}.{2}".format( ver[3], ver[4], ver[1])
        else:
            return "{0}:{1}-{2}.{3}".format( ver[2], ver[3], ver[4], ver[1])
    
    def getFromVersionString(self):
        return self.formatVersion( self.fromVersion )
        
    def getToVersionString(self):
        return self.formatVersion( self.toVersion )
