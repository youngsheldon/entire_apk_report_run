#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-11-11 15:36:10
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-08 14:16:49
import os 

def get_file_path_list(rootDir):
    file_path_list=[]
    for root,dirs,files in os.walk(rootDir):
        for filespath in files:
            file_path_list.append(os.path.join(root,filespath))
    return file_path_list

def collect_res(path,tar):
    collect_set = []
    file_path_list = get_file_path_list(path)
    for item in file_path_list:
        ret = item.find(tar)
        if ret != -1:
            collect_set.append(item)
    return collect_set

def collect_picture(path):
    return collect_res(path,'.png') + collect_res(path,'.jpg')

def collect_data(path):
    return collect_res(path,'.xml')

def collect_inf(path):
    return collect_res(path,'META-INF')

def collect_bin(path):
    collect_set = []
    file_path_list = get_file_path_list(path)
    for item in file_path_list:
        ret = item.find('.')
        if ret == -1:
            collect_set.append(item)
    return collect_set

def get_res_file_name(path):
    v = path.split('/')[-1].split('.')
    v_t = ''
    if len(v) == 2:
        return v[0]
    else:
        for coll in v[0:-1]:
            v_t += coll + '.'
        return v_t[:-1]