#!/bin/sh
# @Author: anchen
# @Date:   2016-12-06 19:04:37
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-07 09:25:47
export LD_LIBRARY_PATH="/opt/smmc/apk_parse/entire_apk_report_run/check/lib"
cd /opt/smmc/apk_parse/entire_apk_report_run/check/
ipcheck $1 $2