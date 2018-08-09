class FatalError( Exception ):
	def __init__(self,value):
		Exception.__init__(self,value)