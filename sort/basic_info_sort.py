#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-01 19:11:22
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-06 11:00:23
from module.xml_parser import XmlParser
from module.file_hash import *
from module.tell_virus_apk import VirusApkAnalyze
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class BasicInfoSort(object):
    """docstring for BasicInfoSort"""
    def __init__(self, apk_code, apk_path, apk_download_log_path, xml_path, act_permis_path, code_key_path,sms_content,outdata_path):
        self.apk_code = apk_code
        self.apk_path = apk_path
        self.apk_download_log_path = apk_download_log_path
        self.xml_path = xml_path
        self.act_permis_path = act_permis_path
        self.code_key_path = code_key_path
        self.outdata_path = outdata_path
        self.sms_content = sms_content
        self.sql = ''

    def get_virus_grade(self,score):
        if score > 70:
            return '2' 
        elif score >= 60 and score <= 70:
            return '1'
        else:
            return '0'

    def get_apk_analyze_run_time(self):
        return '1024'

    def basic_info_collect(self):
        md5 = check_hash(self.apk_path,'md5')
        sha1 = check_hash(self.apk_path,'sha1')
        sha256 = check_hash(self.apk_path,'sha256')
        sha512 = check_hash(self.apk_path,'sha512')
        short_url,long_url = get_url(self.apk_download_log_path)
        apk_download_ip = get_ip(self.apk_download_log_path)
        apk_file_name = get_apk_file_name(self.apk_download_log_path)
        apk_sdk_obj = XmlParser(self.apk_path,self.xml_path)
        min_sdk,fit_sdk = apk_sdk_obj.parserSdkVersion()
        first_found_time = get_datetime()
        last_found_time = first_found_time
        virus_apk_tell_obj = VirusApkAnalyze(self.act_permis_path,self.code_key_path)
        virus_score = virus_apk_tell_obj.virus_tell()
        virus_grade = self.get_virus_grade(virus_score)
        apk_analyze_run_time = self.get_apk_analyze_run_time()
        ip_attribution = get_ip_attribution(apk_download_ip)

        out = self.apk_code + '|' + apk_file_name + '|' + md5 + '|' + sha1 + '|' + sha256  + '|' + sha512 + '|' + first_found_time + '|' + last_found_time + '|' + apk_download_ip + '|' + short_url + '|' + long_url + '|' + self.sms_content + '|' + virus_score + '|' + virus_grade + '|' + apk_analyze_run_time + '|' + min_sdk +   '|' + fit_sdk + '|' + ip_attribution + '\n'

        with open(self.outdata_path,'w+') as f:
            f.write(out)

        self.sql = 'insert into ywc_apk_basic_info values (' + quote(self.apk_code) + ',' + quote(uft_to_gbk(apk_file_name)) + ',' + quote(md5) + ',' + quote(sha1) + ',' + quote(sha256) + ',' + quote(sha512) + ',' + to_date() + ',' + to_date() + ',' + quote(apk_download_ip) + ',' + quote(uft_to_gbk(short_url)) + ',' + quote(uft_to_gbk(long_url)) + ',' + quote(uft_to_gbk(self.sms_content)) + ',' + quote(virus_score) + ',' + quote(virus_grade) + ',' + quote(apk_analyze_run_time) + ',' + quote(min_sdk) + ',' + quote(fit_sdk) + ',' + quote(uft_to_gbk(ip_attribution)) + ');'

    def upload_to_database(self):
        sql_exec(self.sql)