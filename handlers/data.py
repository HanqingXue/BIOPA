import tornado.web
'''
Change the workspace to root path.
'''
import sys
sys.path.append('../')

from methods.dbutil import *

class DataHandler(tornado.web.RequestHandler):
    def post(self):
    	'''
    	Get arguments from front page. 
    	'''
        noun1 = self.get_argument('noun1')
        tabindex = self.get_argument('tabindex')
        tabindex = int(tabindex)
    	'''
    	Query is empty. Load the error page.
    	'''
    	if len(noun1) == 0:
    		self.render('error.html')
       
        if tabindex == 3:
        	self.render("gene.html")  

        else:
            '''
            Query the database with keyword.
            '''
            db = DataBase()
            result = search_db(db, 'BioPA', 'PathID', noun1)

            if len(result) != 0:
            	self.render('data.html', noun1=result, keyword=noun1 )
            else:
            	self.render('error.html')
            



