#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-05 19:33:54
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-07 15:58:21
item = 'data/sss/hi.2.png'
type_value = item.split('.')[-1]
file_name = item.split('/')[-1].split('.')[0:-1]
print type_value
print file_name