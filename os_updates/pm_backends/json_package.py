from __future__ import absolute_import

from .base_package import PackageBase

class JsonPackage( PackageBase ):
    def __init__(self, data ):
        super(JsonPackage, self).__init__()
        self.data = data
    
    def getName( self ):
        return self.data["package"]
    
