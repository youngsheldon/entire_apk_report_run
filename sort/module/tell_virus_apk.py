#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-09-27 12:05:28
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-07 14:21:44
import re 
import os 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

permis_grade_fir = ['PROCESS_OUTGOING_CALLS','READ_CALENDAR','READ_CONTACTS','READ_HISTORY_BOOKMARKS','READ_SMS','RECEIVE_SMS','SEND_SMS','WRITE_SMS','CALL_PHONE','BROADCAST_SMS','BROADCAST_STICKY','BROADCAST_WAP_PUSH','READ_LOGS','WRITE_CONTACTS','WRITE_CALL_LOG']
permis_grade_sec = ['KILL_BACKGROUND_PROCESSES','MODIFY_PHONE_STATE','READ_PHONE_STATE','REBOOT','RECEIVE_BOOT_COMPLETED','RECEIVE_WAP_PUSH','WRITE_SECURE_SETTINGS','WRITE_SETTINGS','BIND_DEVICE_ADMIN','DELETE_PACKAGES','INSTALL_PACKAGES','WRITE_EXTERNAL_STORAGE','GET_TASKS','RESTART_PACKAGES','CHANGE_NETWORK_STATE']
action_grade_fir = ['android.intent.action.NEW_OUTGOING_CALL','android.provider.Telephony.SMS_RECEIVED' ,'android.provider.Telephony.SMS_RECEIVED_2','android.provider.Telephony.GSM_SMS_RECEIVED','android.net.conn.CONNECTIVITY_CHANGE','android.provider.Telephony.SMS_DELIVER','android.intent.action.SEND','android.intent.action.SENDTO','android.intent.action.RESPOND_VIA_MESSAGE']
action_grade_sec = ['android.intent.action.PACKAGE_RESTARTED','android.intent.action.BOOT_COMPLETED','android.media.RINGER_MODE_CHANGED','android.intent.action.DELETE','android.app.action.DEVICE_ADMIN_ENABLED','android.intent.action.PACKAGE_ADDED','android.intent.action.PACKAGE_REPLACED','android.intent.action.PACKAGE_INSTALL','android.intent.action.ACTION_PACKAGE_CHANGED','android.intent.action.SIG_STR']

sender = ['19_a_11','19_a_12']
sendExe = ['19_a_7','19_a_8']
getContent = ['19_a_2','19_a_3','19_a_4','19_a_6']
badBehavior = ['19_a_1','19_a_5','19_a_13','19_a_10']

class VirusApkAnalyze(object):
    """docstring for VirusApkAnalyze"""
    def __init__(self, act_permis_path,code_key_path):
        self.act_permis_path = act_permis_path
        self.code_key_path = code_key_path
        self.permis_list = []
        self.act_list = []
        self.permis_act_list_generator(self.act_permis_path)

    def item_couter(self,detectItem):
        couter = 0 
        code_key_list = self.get_code_key()
        for v in code_key_list:
            if v in detectItem:
                couter += 1 
        return couter 


    def get_code_key(self):
        ret = []
        with open(self.code_key_path,'r') as f:
            for line in f:
                v = line.strip()
                ret.append(v)
            return ret

    def permis_act_list_generator(self,path):
        with open(path,'r') as f:
            for line in f:
                v = line.strip().split('|')[2]
                index = line.strip().split('|')[1]
                if index == '1':
                    self.permis_list.append(v)
                elif index == '2':
                    self.act_list.append(v)

    def codeblock_evaluation(self):
        senderCouter = self.item_couter(sender)
        print 'senderCouter=' + str(senderCouter)
        sendExeCouter = self.item_couter(sendExe)
        print 'sendExeCouter=' + str(sendExeCouter)
        getContentCouter = self.item_couter(getContent)
        print 'getContentCouter=' + str(getContentCouter)
        badBehaviorCouter = self.item_couter(badBehavior)
        print 'badBehaviorCouter=' + str(badBehaviorCouter) 
        if senderCouter != 0 and sendExeCouter != 0 and getContentCouter != 0:
            ret1 = 50.0 + 10.0 * ((senderCouter + sendExeCouter + getContentCouter)/8.0)
        else:
            ret1 = 0
        ret2 = 10.0 * (badBehaviorCouter/4.0)
        sum = ret1 + ret2 
        return ret1 + ret2 

    def permis_evaluation(self):
        permis_grade_fir_couter = 0 
        permis_grade_sec_couter = 0 
        for v1 in self.permis_list:
            for v2 in permis_grade_fir:
                ret = v1.find(v2)
                if ret != -1:
                    permis_grade_fir_couter += 1 
                    break
            for v3 in permis_grade_sec:
                ret = v1.find(v3)
                if ret != -1:
                    permis_grade_sec_couter += 1
                    break 
        print 'permis_grade_fir_couter=' + str(permis_grade_fir_couter)
        print 'permis_grade_sec_couter=' + str(permis_grade_sec_couter)
        return 10.0*permis_grade_fir_couter/15.0 + 10.0*permis_grade_sec_couter/15.0  

    def act_evaluation(self):
        action_grade_fir_couter = 0 
        action_grade_sec_couter = 0 
        for item in self.act_list:
            if item in action_grade_fir:
                action_grade_fir_couter += 1
            if item in action_grade_sec:
                action_grade_sec_couter += 1
        print 'action_grade_fir_couter=' + str(action_grade_fir_couter)
        print 'action_grade_sec_couter=' + str(action_grade_sec_couter)
        return 5.0*action_grade_fir_couter/9.0 + 5.0*action_grade_sec_couter/10.0  

    def virus_tell(self):
        value = self.codeblock_evaluation()+self.permis_evaluation() + self.act_evaluation()
        print 'virus_probility' + ':' + str(value)
        return str(int(float(value)))

# obj = VirusApkAnalyze('29b95ff530c038fd963','code_block.txt','code_key.txt')
# print obj.virus_tell()