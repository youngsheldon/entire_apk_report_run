#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-05 19:33:54
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-05 19:39:34
x = '搭建'

def uft_to_gbk(content):
    src = content.decode("utf8").encode("gbk") 
    return src 

with open('out.txt','a+') as f:
    f.write(uft_to_gbk(x))