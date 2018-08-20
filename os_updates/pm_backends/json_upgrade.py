from __future__ import absolute_import

from .base_upgrade import UpgradeBase
from .json_package import JsonPackage

class JsonUpgrade( UpgradeBase ):
    def __init__(self, data ):
        super(JsonUpgrade, self).__init__()
        self.data = data
        self.package = JsonPackage( self.data )
        if "meta" in self.data:
            self.meta = self.data["meta"]
    
    def getFromVersionString(self):
        return self.data["from_version"]
        
    def getToVersionString(self):
        return self.data["to_version"]

    def getSortingKey( self ):
        key = ""
        if self.isImportant:
            key += "0"
        key += self.package.getName().lower()
        return key

    def getOrigins( self ):
        if "origins" in self.data:
            return self.data["origins"]
        return []
