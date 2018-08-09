from __future__ import absolute_import

from .base_package import PackageBase

class AptPackage( PackageBase ):
    def __init__(self, nativePackage ):
        super(AptPackage, self).__init__()
        self.pkg = nativePackage
    
    def getName( self ):
        return self.pkg.fullname
    
