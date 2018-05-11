import pymongo

class DataBase(object):
	"""docstring for DataBase"""
	def __init__(self, host_id = '127.0.0.1', port_id = 27017):
		super(DataBase, self).__init__()
		self.con = pymongo.MongoClient(host_id, port_id)

	def get_database(self, db_name):
		self.db  = self.con[db_name]
		return self.db

	def search_item(self, query_dic):
		result = []
		for item in self.db.col.find(query_dic):
			result.append(item)

		return result

	def search_all(self):
		result = []
		for item in self.db.col.find():
			result.append(item)

		return result

def search_db(db_instace, db_name, field, keyword):
	db_instace.get_database(db_name).name
	result = db_instace.search_item({field : keyword}) 
	return result

def search_db_all(db_instace, db_name):
	db_instace.get_database(db_name).name
	result = db_instace.search_all() 
	return result