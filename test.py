#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-05 19:33:54
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-07 19:03:21
import re 

str1 = '52d56c4b440bc840feef41f89803b253/acce3ft/aevbbb/util/a.java|8|public static String c = "15622068602","15592676469@189.cn";'

str2 = '52d56c4b440bc840feef41f89803b253|Key15|/opt/smmc/data_backup/apkSource/52d56c4b440bc840feef41f89803b253/acce3ft/aevbbb/util/a.java|12|public static String g = "15622068602","ayy";'

xx = '\"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*\"'

def get_phone_num(tar):
        expr = '\"1\d{10}"'
        ret = re.compile(expr).findall(tar) 
        return ret[0].split('\"')[1]

def get_email_addr(tar):
    expr = '\".*\"'
    ret = re.compile(expr).findall(tar) 
    xx = ret[0].split('\"')
    for v in xx:
        if '@' in v:
            return v 
    return 'none'

print get_email_addr(str1)
