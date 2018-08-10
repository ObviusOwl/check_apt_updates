
class UpgradeBase( object ):
    def __init__(self):
        self.meta = {}

    def getFromVersionString(self):
        raise NotImplementedError()
        
    def getToVersionString(self):
        raise NotImplementedError()
