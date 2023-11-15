try:
	from . import base, connection
except ImportError:
	import base, connection


class Grammer:
	def __init__(self):
		self.tokenMng = base.GrammarlyToken()
		self.connection = connection.Connection(self.tokenMng)
	def text(self, text):
		rev = self.connection.sendText(text)
		return self.connection.getUntilFinish(rev)
	def close(self):
		self.connection.raw.close()		

