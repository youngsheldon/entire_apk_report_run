#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: sheldon
# @Date:   2016-08-17 23:03:37
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-07 09:35:25
import urllib2 #导入urllib2
import simplejson #导入simplejson
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getToWriteList(ip):
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip #查询的淘宝API
    f = urllib2.urlopen(url).read() #通过API获得信息，格式为str
    s = simplejson.loads(f) #将str格式转化为dict
    result_list = []
    result_list.append(s['data']['ip'])
    result_list.append(s['data']['country'])
    result_list.append(s['data']['country_id'])
    result_list.append(s['data']['area'])
    result_list.append(s['data']['area_id'])
    result_list.append(s['data']['region'])
    result_list.append(s['data']['region_id'])
    result_list.append(s['data']['city'])
    result_list.append(s['data']['city_id'])
    result_list.append(s['data']['isp'])
    result_list.append(s['data']['isp_id'])
    return result_list
 
def writeResultToFile(ip,file):
    list = getToWriteList(ip)
    tar = 'ip:' + list[0]+'\n'+'country:' + list[1] +'country_id:' + list[2] + '\n' +'area:' + list[3]+'area_id:' +list[4] + '\n'+ 'region:' + list[5]+'region_id:' +list[6]+ '\n'+'city:' + list[7]+'city_id:' +list[8]+ '\n'+'isp:' + list[9]+'isp_id:' + list[10]
    print tar 
    f = open(file,'w')
    f.write(tar)
    f.close()

# ip=sys.argv[1]
# file=sys.argv[2]
# writeResultToFile(ip,file)

for v in getToWriteList('101.226.90.199'):
    print v 