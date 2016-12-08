#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-05 19:33:54
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-08 15:57:20
import re 
import urllib2 
import simplejson
from sort.module.xml_parser import XmlParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# obj = XmlParser('104.apk','temp.txt')
# action_list = obj.praserPermissionOrAction2('uses-permission')
# for v in action_list:
#     print v 

import sort.module.axmlparserpy.axmlprinter as axmlprinter

ap = axmlprinter.AXMLPrinter(open('AndroidManifest.xml', 'rb').read())
buff = minidom.parseString(ap.getBuff()).toxml()
print(buff)