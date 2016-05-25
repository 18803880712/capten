# -*- coding: utf-8 -*-
""" 数据推送函数
"""
import urllib
import urllib2
import json


def post_data(data=None, url='', timeout=5):
    """ 向指定url post数据
    """
    if data is None:
        data = {}
        ret = {}
    try:
        data = urllib.urlencode(data)
        content = urllib2.urlopen(url, data, timeout)
        print content
        ret = json.loads(content.read())
    except:
#        print content
        return 
       
    return ret
