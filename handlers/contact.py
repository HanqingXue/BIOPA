import tornado.web

class ContactHandler(tornado.web.RequestHandler):
	"""docstring for Contact"""
	def get(self):
		self.render('contact.html')
		pass

