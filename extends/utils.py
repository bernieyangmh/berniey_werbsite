# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
import re
import time
import urllib
import tempfile
import subprocess
from data_analysis.data import DataCore
from data_analysis.util import print_summary_information

tem_dir = tempfile.mkdtemp(suffix='_python_code', prefix='website_')
python_file_index = 0

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


def url_decode_encode(url):
    return urllib.quote_plus(url.encode('utf-8'))


def python_script_run(version, code):
    global python_file_index

    exec_3 = "/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6"
    exec_2 = "/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python"

    python_file_name = "python_%d" % python_file_index
    python_file_index += 1
    python_file_path = os.path.join(tem_dir, '%s.py' % python_file_name)
    code = code.encode('utf-8')

    with open(python_file_path, 'w') as f:
        f.write(code)
    print('Code wrote to: %s' % python_file_path)
    try:
        if version == '3.6':
            res_ouput = subprocess.check_output([exec_3, python_file_path], stderr=subprocess.STDOUT)
        else:
            res_ouput = subprocess.check_output([exec_2, python_file_path], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        res_ouput = dict(error='Exception', output=e.output)
    return res_ouput
