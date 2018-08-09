from __future__ import absolute_import

import logging
import yum
import yum.update_md

from .base_backend import PackageManagerBase
from .yum_package import YumPackage
from .yum_upgrade import YumUpgrade

class YumPackageManager( PackageManagerBase ):
    def __init__(self):
        super(YumPackageManager, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.upgrades = []
        self.yumbase = yum.YumBase()
        # disable yum logging
        self.yumbase.preconf.debuglevel = 0
        self.yumbase.preconf.errorlevel = 0
    
    def getUpgrades( self ):
        ygl = self.yumbase.doPackageLists( pkgnarrow="updates" )
        pkgs = ygl.updates
        pkgsMap = {}
        for pkg in pkgs:
            pkgsMap[ pkg.name ] = pkg
        
        for pkgtup_updated, pkgtup_installed in self.yumbase.up.getUpdatesTuples():
            if pkgtup_updated[0] in pkgsMap:
                upgr = YumUpgrade( pkgsMap[pkgtup_updated[0]], pkgtup_installed, pkgtup_updated)
                self.upgrades.append( upgr )

        return self.upgrades
    
    def getStats( self ):
        return super(YumPackageManager, self).getStats()
