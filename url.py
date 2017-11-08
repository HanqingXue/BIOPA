#coding=utf-8
'''
the url structure of website
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from index import IndexHandler

url = [
    (r'/', IndexHandler),
] 