#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os 
import re 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from xml.dom.minidom import parseString
from axmlparserpy.apk import APK 

class XmlParser(object):
    """docstring for XmlParser"""
    def __init__(self, apk_path, xml_path):
        self.apk_path = apk_path
        self.xml_path = xml_path
        self.get_xml()
        self.dom = self.initRun()

    def get_xml(self):
        obj = APK(self.apk_path)
        obj.save_copy_xml(self.xml_path)

    def initRun(self):
        with open(self.xml_path,'r') as f:
            data = f.read()
        return parseString(data)

    def praserPermissionOrAction(self,toparser):
        ret_list = []
        nodes = self.dom.getElementsByTagName(toparser)
        for node in nodes:
            if toparser == 'action':
                ret_list.append(node.toxml()[22:][:-3])
            elif toparser == 'uses-permission':
                ret_list.append(node.toxml()[31:][:-3])
        ret_list = list(set(ret_list))
        return ret_list

    def pattern(self,expr,data):
        results = re.compile(expr).findall(data) 
        return results

    def RelateAction(self,data,expr):
        action_list = []
        ret = self.pattern(expr,data)
        if ret:
            for item in ret:
                index = item.find('android:name=')
                v = item[index:].split('\"')[1]
                action_list.append(v)
            return action_list
        else:
            return None

    def Entrance(self,data,expr):
        ret = self.pattern(expr,data)[0]
        if ret:
            index = ret.find('android:name=')
            if 'permission' in ret:
                return ret[index:].split('\"')[1],ret[index:].split('\"')[3]
            else:
                return ret[index:].split('\"')[1],None
        else:
            return None,None

    def parserReceiver(self):
        out_dict = {}
        action_list = []
        nodes = self.dom.getElementsByTagName('receiver')
        for node in nodes:
            data = node.toxml()
            expr = r'\<receiver.*android:name=.*\>'
            entrance,request_permis = self.Entrance(data,expr)
            expr = r'\<action android:name=.*\/\>'
            action_list.append(request_permis)
            action_list.append(self.RelateAction(data,expr))
            out_dict[entrance] = action_list
            action_list = []
        return out_dict

    def parserReceiver2(self):
        return self.parserGenerator('receiver')

    def parserService2(self):
        return self.parserGenerator('service')

    def parserGenerator(self,tar):
        out_dict = {}
        action_list = []
        nodes = self.dom.getElementsByTagName(tar)
        for node in nodes:
            content = node.toxml()
            expr = r'\<.*\>'
            rets = self.pattern(expr,content)
            for line in rets:
                ret = line.find('<' + tar)
                if ret != -1:
                    index = line.find('android:name=')
                    if 'permission' in line:
                        entrance,request_permis = line[index:].split('\"')[1],line[index:].split('\"')[3]
                    else:
                        entrance,request_permis = line[index:].split('\"')[1],None
                    action_list.append(request_permis)
                ret = line.find('action android:name')
                if ret != -1:
                    index = line.find('android:name=')
                    v = line[index:].split('\"')[1]
                    action_list.append(v)
            if len(action_list) < 2:
                action_list.append(None)
            out_dict[entrance] = action_list
            action_list = []
        return out_dict

    def parserService(self):
        out_dict = {}
        action_list = []
        nodes = self.dom.getElementsByTagName('service')
        for node in nodes:
            data = node.toxml()
            expr = r'\<service.*android:name=.*\>'
            entrance,request_permis = self.Entrance(data,expr)
            expr = r'\<action android:name=.*\/\>'
            action_list.append(request_permis)
            action_list.append(self.RelateAction(data,expr))
            out_dict[entrance] = action_list
            action_list = []
        return out_dict

    def parserSdkVersion(self):
        nodes = self.dom.getElementsByTagName('uses-sdk')
        v = nodes[0].toxml()
        minSdkVersion = v.split('\"')[1]
        tarSdkVersion = v.split('\"')[3]
        return minSdkVersion,tarSdkVersion 

    def praserPermissionOrAction2(self,toparser):
        ret_list = []
        nodes = self.dom.getElementsByTagName(toparser)
        for node in nodes:
            if toparser == 'action':
                v = node.toxml()[22:][:-12]
                if 'android' in v:
                    ret_list.append(v)
            elif toparser == 'uses-permission':
                v = node.toxml()[31:][:-21]
                if 'android.permission' in v:
                    ret_list.append(v[19:])
        ret_list = list(set(ret_list))
        return ret_list

# obj = XmlParser('29b95ff530c038fd9632c8d1eef79e20.apk','temp.xml')
