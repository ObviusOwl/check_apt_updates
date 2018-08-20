
class UpgradeBase( object ):
    def __init__(self):
        self.meta = {}
        self.isImportant = False

    def getFromVersionString(self):
        raise NotImplementedError()
        
    def getToVersionString(self):
        raise NotImplementedError()

    def getSortingKey( self ):
        raise NotImplementedError()
        
    def getOrigins( self ):
        raise NotImplementedError()
