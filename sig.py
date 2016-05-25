# -*- coding: utf-8 -*-

""" 签名模块定义
"""
import hmac
import hashlib


def gen_sig(app_key='', data=None):
    """ 签名产生函数
    """
    if data is None:
        data = {}
    list = sorted(data.items(), key=lambda data: data[0])
    para_str = ''
    for item in list:
        if para_str == '':
            para_str = str(item[0]) + '=' + str(item[1])
        else:
            para_str += '&' + str(item[0]) + '=' + str(item[1])
    app_key += '&'
    return hmac.new(str(app_key), str(para_str), hashlib.sha1).digest().encode('base64').rstrip()
