#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-01 17:44:54
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-07 17:22:09
import os 
from module.xml_parser import XmlParser
from module.file_hash import *
from module.res_file_find import *
from module.code_sort import Analyze
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MainDataSort(object):
    """docstring for MainDataSort"""
    def __init__(self,apk_path,xml_path,apk_source_path,apk_code,outdata_path,code_key_path):
        self.apk_path = apk_path
        self.xml_path = xml_path
        self.apk_source_path = apk_source_path
        self.outdata_path = outdata_path
        self.apk_code = apk_code
        self.code_key_path = code_key_path

    def write_to_file(self,path,data):
        with open(path,'a+') as f:
            f.write(data)

    def list_type_data_out(self,path,data_type,in_list,apk_code):
        out = ''
        if len(in_list) == 0:
            out += apk_code + '|' + str(data_type) + '|' + '0' + '|' + '0' + '\n'
        else:
            for item in in_list:
                out += apk_code + '|' + str(data_type) + '|' + item + '|'+ '0' + '\n'
        self.write_to_file(path,out)

    def parser_source_code(self):
        obj1 = Analyze(self.apk_source_path,self.apk_code,self.outdata_path,self.code_key_path)
        obj1.enablePrint()
        obj1.run()

    def parser_xml(self):
        obj2 = XmlParser(self.apk_path,self.xml_path)
        action_list = obj2.praserPermissionOrAction2('action')
        permis_list = obj2.praserPermissionOrAction2('uses-permission')
        self.list_type_data_out(self.outdata_path,1,permis_list,self.apk_code)
        self.list_type_data_out(self.outdata_path,2,action_list,self.apk_code)

    def run(self):
        self.parser_source_code()
        self.parser_xml()

    def utf8_to_gbk(self):
        with open(self.outdata_path,'r') as f1:
            content = f1.read()
        with open(self.outdata_path,'w+') as f2:
            src = content.decode("utf8").encode("gbk") 
            f2.write(src)

    def upload_to_database(self):
        sql_list = []
        apk_report_table_name = get_apk_report_name()
        self.utf8_to_gbk()
        with open(self.outdata_path,'r') as f:
            for line in f:
                v = line.strip().split('|')
                apk_code = v[0]
                type_v = v[1]
                name = v[2]
                value = v[3]
                sql = 'insert into  ' + apk_report_table_name + ' (ucode,type,name,value)values(' + quote(apk_code) + ',' + str(type_v) + ',' + quote(name) + ',' + quote(value) + ');'
                sql_list.append(sql)
            sql_exec(sql_list)