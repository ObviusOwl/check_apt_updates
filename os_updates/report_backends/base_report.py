class BaseReport( object ):
    
    def __init__(self):
        pass
    
    def report( self, pkgMgr ):
        raise NotImplementedError()
