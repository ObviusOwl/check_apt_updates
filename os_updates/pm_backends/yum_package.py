from __future__ import absolute_import

from .base_package import PackageBase

class YumPackage( PackageBase ):
    def __init__(self, nativePackage ):
        super(YumPackage, self).__init__()
        self.pkg = nativePackage
        
    def getName( self ):
        return self.pkg.name
    
