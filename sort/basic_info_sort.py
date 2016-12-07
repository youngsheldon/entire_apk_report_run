#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-01 19:11:22
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-07 17:17:21
from module.xml_parser import XmlParser
from module.file_hash import *
from module.tell_virus_apk import VirusApkAnalyze
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class BasicInfoSort(object):
    """docstring for BasicInfoSort"""
    def __init__(self, apk_code, apk_path, apk_download_log_path, xml_path, act_permis_path, code_key_path,sms_content,first_found_time,apk_source_path,outdata_path):
        self.apk_code = apk_code
        self.apk_path = apk_path
        self.apk_download_log_path = apk_download_log_path
        self.xml_path = xml_path
        self.act_permis_path = act_permis_path
        self.code_key_path = code_key_path
        self.outdata_path = outdata_path
        self.sms_content = sms_content
        self.first_found_time = first_found_time
        self.apk_source_path = apk_source_path
        self.sql = ''
        self.v = None

    def get_virus_grade(self,score):
        if score > 70:
            return '2' 
        elif score >= 60 and score <= 70:
            return '1'
        else:
            return '0'

    def get_apk_analyze_run_time(self):
        return '10'

    def utf8_to_gbk(self):
        with open(self.outdata_path,'r') as f1:
            content = f1.read()
        with open(self.outdata_path,'w+') as f2:
            src = content.decode("utf8").encode("gbk") 
            f2.write(src)

    def basic_info_collect(self):
        md5 = check_hash(self.apk_path,'md5')
        sha1 = check_hash(self.apk_path,'sha1')
        sha256 = check_hash(self.apk_path,'sha256')
        sha512 = check_hash(self.apk_path,'sha512')
        short_url,long_url = get_url(self.apk_download_log_path)
        apk_file_name = get_apk_file_name(self.apk_download_log_path)
        apk_sdk_obj = XmlParser(self.apk_path,self.xml_path)
        min_sdk,fit_sdk = apk_sdk_obj.parserSdkVersion()
        last_found_time = self.first_found_time
        virus_apk_tell_obj = VirusApkAnalyze(self.act_permis_path,self.code_key_path)
        virus_score = virus_apk_tell_obj.virus_tell()
        virus_grade = self.get_virus_grade(int(virus_score))
        apk_analyze_run_time = self.get_apk_analyze_run_time()
        init_ip,target_ip = get_ip(self.apk_download_log_path)
        init_ip_attribution = get_ip_attribution(init_ip)
        target_ip_attribution = get_ip_attribution(target_ip)
        apk_file_size = get_file_size(self.apk_path)
        apk_source_file_num = get_file_num(self.apk_source_path)

        out = self.apk_code + '|' + apk_file_name + '|' + md5 + '|' + sha1 + '|' + sha256  + '|' + sha512 + '|' + self.first_found_time + '|' + last_found_time + '|' + short_url + '|' + long_url + '|' + self.sms_content + '|' + virus_score + '|' + virus_grade + '|' + apk_analyze_run_time + '|' + min_sdk +   '|' + fit_sdk + '|' + init_ip + '|' + init_ip_attribution + '|' + target_ip + '|' + target_ip_attribution + '|' + str(apk_file_size) + '|' + str(apk_source_file_num) + '\n'

        with open(self.outdata_path,'w+') as f:
            f.write(out)

        self.utf8_to_gbk()

        with open(self.outdata_path,'r') as f:
            for line in f:
                self.v = line.strip().split('|')
                break 

        self.sql = 'insert into ywc_apk_basic_info values (' + quote(self.v[0]) + ',' + quote(self.v[1]) + ',' + quote(self.v[2]) + ',' + quote(self.v[3]) + ',' + quote(self.v[4]) + ',' + quote(self.v[5]) + ',' + to_date() + ',' + to_date() + ',' + quote(self.v[8]) + ',' + quote(self.v[9]) + ',' + quote(self.v[10]) + ',' + quote(self.v[11]) + ',' + quote(self.v[12]) + ',' + quote(self.v[13]) + ',' + quote(self.v[14]) + ',' + quote(self.v[15]) + ',' + quote(self.v[16]) + ',' + quote(self.v[17]) + ',' + quote(self.v[18]) + ',' + quote(self.v[19]) + ',' + quote(self.v[20]) + ',' + quote(self.v[21]) + ');'

    def upload_to_database(self):
        sql_exec(self.sql)


