import os
import os.path
import shlex
import logging

from os_updates.errors import FatalError

class PackageManagerFactory( object ):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.osInfo = {
            "ID":"",
            "ID_LIKE":[],
            "VERSION": "",
        }
        self.distMap = {
            "debian" : "apt",
            "ubuntu" : "apt",
            "fedora" : "dnf",
            "rhel"   : "yum",
            "centos7": "yum",
            "centos" : "dnf"
        }

    def parseOsRelease( self, fileName ):
        data = {}
        with open( fileName,'r') as fh:
            sh = shlex.shlex( instream=fh, posix=True )
            sh.whitespace = " \t"
            lastTok = currKey = state = None
            currValue = ""
            tok = sh.get_token()
            while tok != sh.eof:
                if tok == "=":
                    state = "value"
                    currValue = ""
                    currKey = lastTok
                elif tok == "\n":
                    state = None
                    data[ currKey ] = currValue
                elif state == "value":
                    currValue += tok
                lastTok = tok
                tok = sh.get_token()
        return data
    
    def loadOsInfo(self):
        if not os.path.exists("/etc/os-release"):
            if os.path.exists("/etc/centos-release"):
                self.osInfo["ID"] = "centos"
                self.osInfo["VERSION"] = "7"
            return;

        data = self.parseOsRelease("/etc/os-release")
        if "ID" in data:
            self.osInfo["ID"] = data["ID"]
        if "ID_LIKE" in data:
            self.osInfo["ID_LIKE"] = data["ID_LIKE"].split(" ")
        if "VERSION" in data:
            self.osInfo["VERSION"] = data["VERSION"]
        self.logger.debug( "OS Info: " + str(self.osInfo) )
    
    def guessPackageManager( self ):
        self.loadOsInfo()
        dists = list( self.distMap )
        osID = self.osInfo["ID"].lower()

        # check for mapping with major version (most derived first)
        if osID + self.osInfo["VERSION"] in dists:
            return self.distMap[ osID + self.osInfo["VERSION"] ]

        # check if we have a direct dist mapping
        if osID in dists:
            return self.distMap[ osID ]
        
        # check for indirect dist mapping 
        for osID in self.osInfo["ID_LIKE"]: 
            osID = osID.lower()
            if osID in dists:
                return self.distMap[ osID ]
    
    def backendFactory( self, managerName=None ):
        if managerName == None:
            managerName = self.guessPackageManager()

        self.logger.info( "Using {0} package manager backend".format(managerName) )
        if managerName == "apt":
            from . import apt_backend
            return apt_backend.AptPackageManager()
        elif managerName == "yum":
            from . import yum_backend
            return yum_backend.YumPackageManager()
        elif managerName == "dnf":
            from . import dnf_backend
            return dnf_backend.DnfPackageManager()
        elif managerName == "json":
            from . import json_backend
            return json_backend.JsonPackageManager()
        else:
            raise FatalError("Unknown package manager backend: {0}".format(managerName) )
