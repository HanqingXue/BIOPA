
# -*- coding:utf-8 -*-
import urllib2
from lxml import etree
from requests import get as getRequest

def pathcards_parser(gene):
    html_page = getRequest('http://pathcards.genecards.org/Search/results?query=%s' % gene)
    html_tree = etree.HTML(html_page.content)
    super_pathways = html_tree.xpath('//strong/a')
    content = html_tree.xpath('//strong/a/../../../td')
   
    result = {}
    for i in range(len(content)/5):
        x = i * 5
        super_pathways[i] = super_pathways[i].text
        tem = {}
        tem['SuperPathwayName'] = super_pathways[i]
        tem['GenesCount'] = content[x+3].text
        tem['RelevanceScore'] = content[x+4].text
        result[i+1] = tem
    
    return result