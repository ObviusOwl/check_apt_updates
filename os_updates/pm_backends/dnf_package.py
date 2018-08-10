from __future__ import absolute_import

from .base_package import PackageBase

class DnfPackage( PackageBase ):
    def __init__(self, nativePackage ):
        super(DnfPackage, self).__init__()
        self.pkg = nativePackage
    
    def getVersionString(self):
        if self.pkg == None:
            return ""
        if self.pkg.epoch == 0:
            return "{0}-{1}.{2}".format( self.pkg.version, self.pkg.release, self.pkg.arch)
        else:
            return "{0}:{1}-{2}.{3}".format( self.pkg.epoch, self.pkg.version, self.pkg.release, self.pkg.arch)
    
    def getName( self ):
        return self.pkg.name
    
