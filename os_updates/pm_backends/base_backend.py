import fnmatch

class PackageManagerBase( object ):
    def __init__(self):
        self.name = ""
        self.importantPackages = []

    def setImportantPackages( self, importantList ):
        self.importantPackages = importantList

    def getUpgrades( self ):
        raise NotImplementedError()
    
    def getStats( self ):
        return {}
    
    def getHostname(self):
        return None
    
    @staticmethod
    def getSortingKey( upgrade ):
        return upgrade.getSortingKey()
    
    def isPackageImportant( self, pkg ):
        name = pkg.getName()
        for pattern in self.importantPackages:
            if fnmatch.fnmatchcase( name, pattern ):
                return True
        return False