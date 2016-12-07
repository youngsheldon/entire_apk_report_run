#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-05 19:33:54
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-07 17:14:10
import time

def get_datetime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


def get_apk_report_name():
    v = get_datetime().split('-')
    return 'ywc_apk_report_' + v[0] + v[1]

print get_apk_report_name()
