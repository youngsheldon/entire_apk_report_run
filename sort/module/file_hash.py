#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-11-10 09:20:32
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-06 11:25:03
import hashlib
import os,sys
import functools
import time
import re
from Mylog import Mylog 
from os.path import join, getsize

def check_hash(filepath,type):
    with open(filepath,'rb') as f:
        if type == 'md5':
            obj = hashlib.md5()
        elif type == 'sha1':
            obj = hashlib.sha1()
        elif type == 'sha256':
            obj = hashlib.sha256()
        else:
            obj = hashlib.sha512()
        obj.update(f.read())
        hash = obj.hexdigest()
        return hash    

def get_file_size(path):
    return getsize(path)/1024.0 

def get_filename(path):
    return path.split('/')[-1].split('.')[0]

def get_file_num(rootDir):
    file_path_list=[]
    for root,dirs,files in os.walk(rootDir):
        for filespath in files:
            file_path_list.append(os.path.join(root,filespath))
    return len(file_path_list)

def log_time(md5,index):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            t1 = time.time()
            ret = func(*args,**kw)
            t2 = time.time()
            with open('data/'+ md5 + '/basic_info.txt','a+') as f:
                out = md5 + '|' + str(index) + '|' + str(t2-t1) + '\n'
                f.write(out)
            return ret 
        return wrapper
    return decorator

def out_report(md5,index,value):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            out = md5 + '|' + str(index) + '|' + str(value) + '\n'
            with open('data/' + md5 + '/basic_info.txt','r') as f:
                f.write(out)
            return func(*args,**kw)
        return wrapper
    return decorator

def generate_apk_ucode(md5_str):
    obj = hashlib.md5()
    v = md5_str + str(time.time())
    obj.update(v)
    ucode = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + obj.hexdigest()[:18]
    return ucode    

def get_url(path):
    url_list = []
    pattern = re.compile('http:\/\/.*')  
    with open(path,'r') as f:
        content = f.read()
    ret = pattern.findall(content) 
    for v in ret:
        if '[following]' not in v:
            url_list.append(v)
    out = sorted(url_list, key=lambda x: len(x)) 
    if len(out) > 1:
        return out[0],out[-1]
    else:
        return out[0],out[0]

def get_ip(path):
    pattern = re.compile('\d+\.\d+\.\d+\.\d+')  
    with open(path,'r') as f:
        content = f.read()
    ret = pattern.findall(content) 
    return ret[-1]

def get_apk_file_name(path):
    pattern = re.compile('`.*.apk.*saved')  
    with open(path,'r') as f:
        content = f.read()
    ret = pattern.findall(content) 
    value = str(ret)
    pos1 = value.find('`') 
    pos2 = value.find('\'') 
    file_name = value[pos1+1:pos2]
    return file_name.split('.')[0]

def get_datetime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def get_sms_content():
    return '6AA927B1F5AD5A1C3ED52E6DBC7BBC96ED229317107B7E8FF042AB4D6E34413F53C48EDFF1ACB521258795C596AE51732AB68CBCFEFF8C4EF0B6C8DBC32EBCB1F93CEC057F20862F832339FB26329C92832339FB26329C92832339FB26329C92832339FB26329C92521CE764DCFFBD51'

def get_ip_attribution(ip):
    return '中国黑龙江哈尔滨市'

def get_file_path_list(rootDir):
        file_path_list=[]
        for root,dirs,files in os.walk(rootDir):
            for filespath in files:
                file_path_list.append(os.path.join(root,filespath))
        return file_path_list

def get_to_handle_apk_info(apk_log_path,backup_path):
    alarm_dict = {}
    alarm_list = []
    ret = get_file_path_list(apk_log_path)
    for path in ret:
        if 'apk_' in path and 'compilation/backup/' not in path:
            with open(path,'r') as f:
                for line in f:
                    v = line.strip().split(',')
                    alarm_time = v[0]
                    url = v[1]
                    apk_md5 = v[2]
                    sms_content = v[3]
                    alarm_list.append(sms_content)
                    alarm_list.append(url)
                    alarm_list.append(alarm_time)
                    if alarm_dict.has_key(apk_md5):
                        pass
                    else:
                        alarm_dict[apk_md5] = alarm_list
                    alarm_list = []
            out = 'mv ' + path + ' ' + backup_path
            os.system(out)
    return alarm_dict

def sql_exec(sql):
    sql_exe = ''
    if isinstance(sql,list):
        for v in sql:
            sql_exe += v + '\n'
        out = 'sqlplus smmcadmin/AdminDB^12@SMMC <<!\n' + sql_exe + 'exit;\n' + '!\n'
    else:
        out = 'sqlplus smmcadmin/AdminDB^12@SMMC <<!\n' + sql + '\n' + 'exit;\n' + '!\n'
    os.system(out)

def quote(str_obj):
    return '\'' + str_obj + '\'' 

def update_cost(apk_md5,cost):
    sql = 'update  ywc_apk_basic_info set cost=' + str(int(cost)) + ' where md5 = ' +       '\'' + apk_md5 + '\'' +';'
    sql_exec(sql)

def update_last_update(apk_md5):
    now_datetime = get_datetime()
    sql = 'update  ywc_apk_basic_info set last_update=to_date( \'' + now_datetime + '\' , \'' + 'YYYY-MM-DD HH24:MI:SS\' ) where md5 = ' + '\'' + apk_md5 + '\'' +';'
    sql_exec(sql)

def to_date():
    out = 'to_date(' + '\'' + get_datetime() + '\'' + ',' + '\'' + 'YYYY-MM-DD HH24:MI:SS' + '\'' + ')'  
    return out 