from __future__ import absolute_import

import logging
import subprocess
import re

import dnf

from .base_backend import PackageManagerBase
from .dnf_package import DnfPackage
from .dnf_upgrade import DnfUpgrade

class DnfPackageManager( PackageManagerBase ):
    def __init__(self):
        super(DnfPackageManager, self).__init__()
        self.name = "dnf"
        self.logger = logging.getLogger(__name__)
        self.upgrades = []
    
    def getUpgrades( self ):
        self.dnfbase = dnf.Base()
        self.dnfbase.read_all_repos()
        self.dnfbase.update_cache()
        self.dnfbase.fill_sack(load_system_repo=True, load_available_repos=True)
        self.dnfbase.upgrade_all()
        self.dnfbase.resolve()

        upgradeDict = {}
        for pkg in self.dnfbase.transaction.install_set:
            upgradeDict[ pkg.name ] = {"to":pkg, "from":None}

        for pkg in self.dnfbase.transaction.remove_set:
            if pkg.name in upgradeDict:
                upgradeDict[ pkg.name ]["from"] = pkg
        
        for k in upgradeDict:
            up = DnfUpgrade( upgradeDict[k]["from"], upgradeDict[k]["to"] )
            upgradeDict[k]["up"] = up
            self.setUpgradeImportant( up )
            self.upgrades.append( up )

        try:
            data = subprocess.check_output(["dnf", "--refresh", "updateinfo", "list"])
            lineRe = re.compile( "^(\S+)\s+(\S+)\s+(\S+)$" )
            for line in data.decode().splitlines():
                m = lineRe.match( line )
                if m != None:
                    for k in upgradeDict:
                        if m.group(3).startswith( k+"-"+upgradeDict[k]["up"].getToVersionString() ):
                            upgradeDict[k]["up"].setMeta("type",m.group(2))
                            break
        except subprocess.CalledProcessError as e:
            self.logger.error( "Subprocess '{0}' faild with exit code {1}".format( e.cmd, e.returncode )  )
        
        self.dnfbase.close()
        return self.upgrades

    def setUpgradeImportant( self, up ):
        up.isImportant = self.isPackageImportant( up.package )
