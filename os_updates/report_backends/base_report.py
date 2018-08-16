
from os_updates.pm_backends.base_backend import PackageManagerBase

class BaseReport( object ):
    
    def __init__(self):
        pass
    
    def report( self, pkgMgr ):
        raise NotImplementedError()
    
    def sortUpgradeList( self, upgrades ):
        #pm = PackageManagerBase()
        upgrades.sort( key=PackageManagerBase.getSortingKey )
