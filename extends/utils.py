# -*- coding: utf-8 -*-
# !/usr/bin/env python


from data_analysis.data import DataCore
from data_analysis.util import print_summary_information
import sys
import re
import time

def data_analysis(path, num):
    print "data_analysis"
    print path
    d = DataCore(path)
    d.generate_data()
    return print_summary_information(d, num=num)


def get_timestamp_date(timestamp_data):
    re_date = re.compile(r"^\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2}$")
    re_timestamp = re.compile(r"^[0-9]{1,45}$")
    if re_timestamp.match(timestamp_data):
        timestamp_data_res = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp_data)))

    elif re_date.match(timestamp_data):
        timestamp_data_res = time.mktime(time.strptime(timestamp_data, '%Y-%m-%d %H:%M:%S'))
    else:
        timestamp_data_res = "格式不匹配"
    return timestamp_data_res
