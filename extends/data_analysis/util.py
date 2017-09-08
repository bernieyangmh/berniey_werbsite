# -*- coding: utf-8 -*-
# !/usr/bin/env python

import re
import time
from sqlalchemy import create_engine
import pandas as pd
import os
from collections import OrderedDict


__author__ = 'berniey'


re_limit = re.compile(r"^[0-9]*:[0-9]*")
re_ip = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
re_time = re.compile(r"^\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2}$")

series_to_frame_by_kind = {
                           'get_ip_traffic': (['ip'], 'traffic'),
                           'get_ip_count': (['ip'], 'count'),
                           'get_url_traffic': (['url'], 'traffic'),
                           'get_url_count': (['url'], 'count'),
                           'get_code_count': (['code'], 'count'),
                           'get_url_code_count': (['url', 'code'], 'count'),
                           'get_ip_code_count': (['ip', 'code'], 'count'),
                           'get_ip_url_code_count': (['ip', 'url', 'code'], 'count'),
                           'get_time_traffic_count': (['time'], 'traffic'),
                           }


def singleton(cls, *args, **kw):
    """
    @singleton
    def fun():
    """
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


class SingletonMetaclass(type):
    """
    Singleton Metaclass

    __metaclass__ = SingletonMetaclass

    """

    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(SingletonMetaclass, cls).__call__(*args)
        return cls._inst[cls]


def traffic_decimal(x, pos):
    """
    :param x: value
    :param pos: placeholder

    :return: diff unit abbreviation
    """
    if x <= 1000:
        return '{:1.0f}'.format(x)
    elif 1000 < x <= 1000000:
        return '{:1.0f}K'.format(x*1e-3)
    elif 1000000 < x <= 1000000000:
        return '{:1.1f}M'.format(x*1e-6)
    elif 1000000000 <= x < 1000000000000:
        return '{:1.2f}G'.format(x*1e-9)
    elif x <= 1000000000000:
        return '{:1.3f}P'.format(x * 1e-12)
    return '{:1.0f}WTF'.format(x)


def data_after_argument(aim_data, *args, **kwargs):
    """
    if limit doesn't match re,return all
    if only :x return top x
    if only x: return last x
    if x:y return x to y
    """
    l1 = kwargs.get('limit')[0]
    l2 = kwargs.get('limit')[1]
    if l1 >= 0 and l2:
        return aim_data[l1:l2]
    if l1 >= 0 and not l2:
        return aim_data[l1:]
    if not l1 and l2 >= 0:
        return aim_data[:l2]
    else:
        return aim_data


def parse_limit(limit):
    if not re_limit.match(limit):
        return 0, 0
    a = limit.split(':')
    a1 = int(a[0]) if a[0] != '' else 0
    a2 = int(a[1]) if a[1] != '' else None
    return a1, a2


def convert_time_format(request_time):
    """
    GMT convert to Beijing time
    :return time
    """
    struct_time = time.strptime(request_time, "[%d/%b/%Y:%X+0800]")
    timestamp = time.mktime(struct_time) + 28800
    time_array = time.localtime(timestamp)
    time_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    # 如果需要时间戳并且不需要时间的绘图，可以加上timestamp
    # return time_date, timestamp
    return time_date


def print_summary_information(d, num=20):
    res_dict = {"code_num": [], "url_flx": [], "url_num": [], "ip_flx": [], "ip_num": []}

    to_list = d.get_code_count(limit=parse_limit(':{}'.format(num)))
    for key in to_list.iteritems():
        res_dict.get("code_num").append(key)

    to_list = d.get_url_traffic(limit=parse_limit(':{}'.format(num)))
    for key in to_list.iteritems():
        res_dict.get("url_flx").append(key)

    to_list = d.get_url_count(limit=parse_limit(':{}'.format(num)))
    for key in to_list.iteritems():
        res_dict.get("url_num").append(key)

    to_list = d.get_ip_traffic(limit=parse_limit(':{}'.format(num)))
    for key in to_list.iteritems():
        res_dict.get("ip_flx").append(key)

    to_list = d.get_ip_count(limit=parse_limit(':{}'.format(num)))
    for key in to_list.iteritems():
        res_dict.get("ip_num").append(key)

    return res_dict


def series_to_dataframe(data, columns_value):
    df = pd.DataFrame([i for i in data.index], columns=columns_value[0])
    df[columns_value[1]] = data.values
    return df



