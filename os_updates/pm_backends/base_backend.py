
class PackageManagerBase( object ):
    def __init__(self):
        self.name = ""

    def getUpgrades( self ):
        raise NotImplementedError()
    
    def getStats( self ):
        return {}
