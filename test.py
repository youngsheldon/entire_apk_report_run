#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-05 19:33:54
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-07 11:16:25
def get_virus_grade(score):
    if score > 70:
        return '2' 
    elif score >= 60 and score <= 70:
        return '1'
    else:
        return '0' 

print get_virus_grade(35.33/1.1)