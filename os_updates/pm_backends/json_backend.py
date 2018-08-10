from __future__ import absolute_import

import json
import os.path

from os_updates.errors import FatalError
from .base_backend import PackageManagerBase
from .json_package import JsonPackage
from .json_upgrade import JsonUpgrade

class JsonPackageManager( PackageManagerBase ):
    def __init__(self):
        super(JsonPackageManager, self).__init__()
        self.fileName = None
        self.upgrades = []
        self.data = None
    
    def setFile(self, name ):
        self.fileName = name
    
    def getUpgrades( self ):
        if not os.path.exists(self.fileName):
            raise FatalError("File '{}' does not exists".format(self.fileName) )

        with open( self.fileName,'r') as fh:
            self.data = json.load( fh )
        
        if "upgrades" in self.data:
            for pkg in self.data["upgrades"]:
                if "package" in pkg and "from_version" in pkg and "to_version" in pkg:
                    self.upgrades.append( JsonUpgrade(pkg) )
        return self.upgrades

    def getHostname(self):
        if "hostname" in self.data:
            return self.data["hostname"]
        return None
