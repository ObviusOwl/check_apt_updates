from __future__ import absolute_import

import apt

from .base_backend import PackageManagerBase
from .apt_package import AptPackage
from .apt_upgrade import AptUpgrade

class AptPackageManager( PackageManagerBase ):
    def __init__(self):
        super(AptPackageManager, self).__init__()
        self.name = "apt"
        self.upgrades = []
    
    def getUpgrades( self ):
        cache = apt.Cache()
        cache.update()
        cache.open(None)
        cache.upgrade( dist_upgrade=True )
        upgrades = cache.get_changes()
        cache.close()
        for pkg in upgrades:
            up = AptUpgrade(pkg)
            self.setUpgradeImportant( up )
            self.upgrades.append( up )
        return self.upgrades
    
    def getStats( self ):
        stats = {"upgrades":0, "downgrades":0, "installs":0, "deletions":0, "download_size":0, "installed_size":0, "curr_installed_size":0 }
        for upgrade in self.upgrades:
            pkg = upgrade.pkg
            if pkg.marked_upgrade:
                stats["upgrades"] += 1
            elif pkg.marked_downgrade:
                stats["downgrades"] += 1
            elif pkg.marked_install:
                stats["installs"] += 1
            elif pkg.marked_delete:
                stats["deletions"] += 1
            if pkg.candidate != None:
                stats["download_size"] += pkg.candidate.size
                stats["installed_size"] += pkg.candidate.installed_size
            if pkg.installed != None:
                stats["curr_installed_size"] += pkg.installed.installed_size
        return stats

    def setUpgradeImportant( self, up ):
        up.isImportant = self.isPackageImportant( up.package )
