
class PackageManagerBase( object ):
    def __init__(self):
        pass

    def getUpgrades( self ):
        raise NotImplementedError()
    
    def getStats( self ):
        return {}
