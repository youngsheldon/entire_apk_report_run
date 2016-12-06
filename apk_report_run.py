#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-02 11:41:57
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-06 11:57:52
import sys,os
import time
from sort.basic_info_sort import BasicInfoSort
from sort.main_info_sort import MainDataSort
from sort.res_sort import ResInfoSort
from sort.module.file_hash import * 
from sort.module.Mylog import Mylog

class ApkReport(object):
    """docstring for ApkReport"""
    def __init__(self):
        self.apk_path = ''
        self.apk_name = ''
        self.source_path = ''
        self.apk_md5 = ''
        self.xml_path = ''
        self.apk_code = ''
        self.file_size = ''
        self.main_info_outdata_path = ''
        self.code_key_path = ''
        self.apk_res_outdata_path = ''
        self.apk_download_log_path = ''
        self.basic_info_outdata_path = ''
        self.sms_content = ''
        self.apk_alarm_log_path = '/opt/smmc/data_backup/compilation'
        self.apk_alarm_log_backup_path = '/opt/smmc/data_backup/compilation/backup/'
        self.mylog = Mylog('data/log.txt').getObject()

    def check_md5(self):
        with open('data/md5.txt','r') as f:
            content = f.read()
            if self.apk_md5 in content:
                return True 
            else:
                return False 

    def save_md5(self):
        out = self.apk_md5 + '\n'
        with open('data/md5.txt','a+') as f:
            f.write(out)

    def mkdir_for_data_file(self):
        out = 'data/' + self.apk_md5
        os.makedirs(out)

    def save_problem_apk_md5(self):
        out = self.apk_md5 + '\n'
        with open('data/problem_apk.txt','a+') as f:
            f.write(out)

    def remove_data_dir(self):
        out = 'rm ' + 'data/' + self.apk_md5 + '/ -rf'
        os.system(out)

    def remove_apk_code_source(self):
        out = 'rm ' + self.source_path + ' -rf'
        os.system(out)

    def decode_apk(self):
        arg = self.source_path + ' ' + self.apk_path
        os.system('JAVA_OPTS=\"-Xmx4G\" jadx -j 1 -d ' + arg)

    def apk_analyze_run(self):
        if self.file_size > 800000:
            print 'file_size is over 800M'
            return False 
        else:
            if self.check_md5():
                print 'this apk has been handled'
                self.mylog.info('[' + self.apk_md5 + ':update last_update]')
                update_last_update(self.apk_md5)
                return False
            else:
                t1 = time.time()
                self.save_md5()
                self.mkdir_for_data_file()
                self.mylog.info('[' + self.apk_md5 + ':begin to decode apk]')
                self.decode_apk()
                try:
                    self.mylog.info('[' + self.apk_md5 + ':begin to generate data for apk_report_yyyymm]')
                    apk_report = MainDataSort(self.apk_path,self.xml_path,self.source_path,self.apk_code,self.main_info_outdata_path,self.code_key_path)
                    apk_report.run()
                    self.mylog.info('[' + self.apk_md5 + ':begin to upload data to apk_report_yyyymm]')
                    apk_report.upload_to_database()
                    self.mylog.info('[' + self.apk_md5 + ':begin to generate data for apk_resource]')
                    apk_res = ResInfoSort(self.source_path,self.apk_res_outdata_path,self.apk_code)
                    apk_res.run()
                    self.mylog.info('[' + self.apk_md5 + ':begin to upload data to apk_resource]')
                    apk_res.upload_to_database()
                    self.mylog.info('[' + self.apk_md5 + ':begin to generate data for apk_basic_info]')
                    apk_basic_obj = BasicInfoSort(self.apk_code,self.apk_path,self.apk_download_log_path,self.xml_path,self.main_info_outdata_path,self.code_key_path,self.sms_content,self.basic_info_outdata_path)
                    apk_basic_obj.basic_info_collect()
                    self.mylog.info('[' + self.apk_md5 + ':begin to upload data to apk_basic_info]')
                    apk_basic_obj.upload_to_database()
                    t2 = time.time()
                    cost = t2 - t1
                    update_cost(self.apk_md5,cost)
                    self.mylog.info('[' + self.apk_md5 + ':-------finish---------]')
                    print self.apk_md5 + '------------finish-----------------'
                except Exception, e:
                    self.save_problem_apk_md5()
                    self.remove_data_dir()
                    self.remove_apk_code_source()
                    self.mylog.exception(self.apk_md5)
                    os._exit(0)

    def run(self):
        alarm_dict = get_to_handle_apk_info(self.apk_alarm_log_path,self.apk_alarm_log_backup_path)
        if len(alarm_dict) > 0:
            for key,item in alarm_dict.items():
                self.sms_content = item[0]
                self.apk_path = '/opt/smmc/data_backup/apk/' + key + '.apk'
                self.apk_name = get_filename(self.apk_path)
                self.source_path = '/opt/smmc/apk_parse/apk_source/' + self.apk_name + '/'
                self.apk_md5 = check_hash(self.apk_path,'md5')
                self.xml_path = self.source_path + 'AndroidManifest.xml'
                self.apk_code = generate_apk_ucode(self.apk_md5)
                self.file_size = get_file_size(self.apk_path)
                self.main_info_outdata_path = 'data/' + self.apk_md5 + '/apk_report_yyyymm.txt'
                self.code_key_path = 'data/' + self.apk_md5 + '/code_key.txt'
                self.apk_res_outdata_path = 'data/' + self.apk_md5 + '/apk_res.txt'
                self.apk_download_log_path = '/opt/smmc/data_backup/apk/' + self.apk_name + '.log'
                self.basic_info_outdata_path = 'data/' + self.apk_md5 + '/apk_basic.txt'
                self.apk_analyze_run()
                self.remove_apk_code_source()
            alarm_dict = {}
            self.sms_content = ''
        else:
            pass 

obj = ApkReport()
obj.run()