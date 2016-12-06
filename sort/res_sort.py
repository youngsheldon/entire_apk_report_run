#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-01 18:40:33
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-06 11:53:12
import os 
from module.xml_parser import XmlParser
from module.file_hash import *
from module.res_file_find import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ResInfoSort(object):
    """docstring for ResInfoSort"""
    def __init__(self, apk_source_path,outdata_path,apk_code):
        self.apk_source_path = apk_source_path
        self.outdata_path = outdata_path
        self.apk_code = apk_code 

    def write_to_file(self,path,data):
        with open(path,'a+') as f:
            f.write(data)
            
    def list_type_data_out(self,path,in_list,md5):
        if len(in_list) is not None:
            for item in in_list:
                type_value = item.split('.')[1]
                file_name = item.split('/')[-1].split('.')[0]
                file_path = item 
                out = md5 + '|' + type_value + '|' + file_name + '|' + file_path + '\n'
                self.write_to_file(path,out)

    def run(self):
        picture_list = collect_picture(self.apk_source_path)
        data_list = collect_data(self.apk_source_path)
        inf_list = collect_inf(self.apk_source_path)
        bin_list = collect_inf(self.apk_source_path)
        self.list_type_data_out(self.outdata_path,picture_list,self.apk_code)
        self.list_type_data_out(self.outdata_path,data_list,self.apk_code)
        self.list_type_data_out(self.outdata_path,inf_list,self.apk_code)
        self.list_type_data_out(self.outdata_path,bin_list,self.apk_code)

    def utf8_to_gbk(self):
        with open(self.outdata_path,'r') as f1:
            content = f1.read()
        with open(self.outdata_path,'w+') as f2:
            src = content.decode("utf8").encode("gbk") 
            f2.write(src)

    def upload_to_database(self):
        sql_list = []
        self.utf8_to_gbk()
        with open(self.outdata_path,'r') as f:
            for line in f:
                v = line.strip().split('|')
                apk_code = v[0]
                type_v = v[1]
                file_name = v[2]
                path = v[3]
                sql = 'insert into  ywc_apk_resource (ucode,format,name,path)values(' + quote(apk_code) + ',' + quote(type_v) + ',' + quote(file_name) + ',' + quote(path) + ');'
                sql_list.append(sql)
            sql_exec(sql_list)

# apk_source_path = 'apk_source/0f11e5c885d7cc1e5f2d73525f033ca1/'
# outdata_path = 'res_out.txt'
# apk_code = '29b95ff530c038fd9632c'
# obj = ResInfoSort(apk_source_path,outdata_path,apk_code)
# obj.run()