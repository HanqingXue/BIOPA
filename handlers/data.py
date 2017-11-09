import tornado.web
'''
Change the workspace to root path.
'''
import sys
sys.path.append('../')

from methods.dbutil import *

class DataHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        db = DataBase()
        print db.get_database('BioPA').name
        result = db.search_item({'PathID': noun1})
        if len(result) == 0:
            self.render('gene.html')
        else:
            self.render('data.html', noun1=result, keyword=noun1 )