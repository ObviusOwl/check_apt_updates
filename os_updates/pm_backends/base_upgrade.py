
class UpgradeBase( object ):
    def __init__(self):
        pass

    def getFromVersionString(self):
        raise NotImplementedError()
        
    def getToVersionString(self):
        raise NotImplementedError()
