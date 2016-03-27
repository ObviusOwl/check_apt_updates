import subprocess
from subprocess import CalledProcessError
import re

from errors import FatalError

class apt_upgrade( object ):
    def __init__(self):
        pass
    
    def run_apt(self):
        # check_call does return nothing if exit code != 0, apt-get exits 1 
        cmd = "apt-get -u -V --assume-no upgrade; if [ $? -eq 1 ]; then exit 0; else exit $?; fi"
        out = ""
        try:
            out = subprocess.check_output( cmd, shell=True )
            out = out.decode()
        except CalledProcessError as e:
            if e.returncode != 1:
                raise FatalError( "apt-get returned error code {}".format(e.returncode) )
        return out
    
    def parse_apt(self, aptout ):
        #print( aptout )
        data = { "upgrades":[], 
                "nb_upgraded":0, "nb_insalled":0, "nb_removed":0, "nb_not_upgraded":0,
                "download_size":"", "install_size":"",
                "raw_stats":"", "raw_download_size":"", "raw_install_size":"" }
        status = ""
        for l in aptout.splitlines():
            m = re.fullmatch( "^The following packages will be upgraded:$", l )
            if m != None:
                status = "upgrade"
                continue
            m = re.fullmatch( "([0-9]+) upgraded, ([0-9]+) newly installed, ([0-9]+) to remove and ([0-9]+) not upgraded.", l )
            if m != None:
                status = "stats"
                data["nb_upgraded"]     = int( m.group(1) )
                data["nb_installed"]    = int( m.group(2) )
                data["nb_removed"]      = int( m.group(3) )
                data["nb_not_upgraded"] = int( m.group(4) )
                data["raw_stats"] = m.group(0)
            m = re.fullmatch( "Need to get (.*) of archives.", l )
            if m != None:
                status = "stats"
                data["download_size"] = m.group(1)
                data["raw_download_size"] = m.group(0)
            m = re.fullmatch( "After this operation, (.*) of additional disk space will be used.", l )
            if m != None:
                status = "stats"
                data["install_size"] = m.group(1)
                data["raw_install_size"] = m.group(0)
            if status == "upgrade":
                m = re.fullmatch( "^\s*(.+)\(([^=>]*) => ([^=>]*)\)$", l )
                if m != None:
                    d = {"package":m.group(1), 
                         "old_version":m.group(2), "new_version": m.group(3)}
                    data["upgrades"].append( d )
        return data
    
    def get_upgrades( self ):
        raw = self.run_apt()
        data = self.parse_apt( raw )
        return data
        
"""
import json        
a = apt_upgrade()
print( json.dumps( a.get_upgrades() , indent =4) )
"""