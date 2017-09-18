# -*- coding: utf-8 -*-
# !/usr/bin/env python


from .util import data_after_argument, series_to_dataframe

__author__ = 'berniey'


class DataAnalysisMethod(object):

    @staticmethod
    def url_traffic(datacore, *args, **kwargs):
        """
        根据url返回对应的流量
        """
        aim_data = datacore.groupby('url').sum()['TrafficSize'].sort_values(ascending=False)
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def url_count(datacore, *args, **kwargs):
        """
        根据url返回对应的访问次数
        """
        aim_data = datacore['url'].value_counts().rename('count').sort_values(ascending=False)
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def ip_traffic(datacore, *args, **kwargs):
        """
        根据ip返回对应的流量
        """
        aim_data = datacore.groupby('ip').sum()['TrafficSize'].sort_values(ascending=False)
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def ip_count(datacore, *args, **kwargs):
        """
        根据ip返回对应的访问次数
        """
        aim_data = datacore['ip'].value_counts().rename('count').sort_values(ascending=False)
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def code_count(datacore, *args, **kwargs):
        """
        根据状态码返回对应的访问次数
        """
        aim_data = datacore['StatusCode'].value_counts().rename('count').sort_values(ascending=False)
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def ip_url_code_count(datacore, *args, **kwargs):
        """
        根据ip、url返回不同状态码对应的访问次数
        """
        aim_data = datacore.groupby(['ip', 'url'])['StatusCode'].value_counts().rename('count').sort_values(ascending=False)
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def url_code_count(datacore, *args, **kwargs):
        """
        根据url和状态码返回对应的访问次数
        """
        aim_data = datacore.groupby('url')['StatusCode'].value_counts().rename('count').sort_values(ascending=False)
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def ip_code_count(datacore, *args, **kwargs):
        """
        根据ip和状态码返回对应的访问次数
        """
        aim_data = datacore.groupby('ip')['StatusCode'].value_counts().rename('count').sort_values(ascending=False)
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def time_traffic(datacore, *args, **kwargs):
        """
        返回指定时间段产生的流量
        """
        aim_data = datacore.groupby('request_time')['TrafficSize'].sum()
        aim_data = series_to_dataframe(aim_data, (['time'], 'traffic'))
        if kwargs.get('start_time'):
            aim_data = aim_data[kwargs.get('start_time') < aim_data['time']]
        if kwargs.get('end_time'):
            aim_data = aim_data[aim_data['time'] < kwargs.get('end_time')]
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def time_count(datacore, *args, **kwargs):
        """
        返回指定时间段对应的访问次数
        """
        aim_data = datacore['request_time'].value_counts(sort=False).rename('count').sort_index()
        aim_data = series_to_dataframe(aim_data, (['time'], 'count'))
        if kwargs.get('start_time'):
            aim_data = aim_data[kwargs.get('start_time') < aim_data['time']]
        if kwargs.get('end_time'):
            aim_data = aim_data[aim_data['time'] < kwargs.get('end_time')]
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def data_by_factor(datacore, *args, **kwargs):
        """
        根据限制条件返回清洗后的日志数据
        """
        aim_data = datacore
        # 过滤指定的状态码，支持nxx的形式
        if kwargs.get('status_code'):
            if str(kwargs['status_code'])[1:] == 'xx':
                aim_data = aim_data[(int(kwargs.get('status_code')[0])*100 <= aim_data.StatusCode)
                                    & (aim_data.StatusCode < (int(kwargs.get('status_code')[0])+1)*100)]
            else:
                aim_data = aim_data[aim_data.StatusCode == int(kwargs['status_code'])]
        if kwargs.get('url'):
            aim_data = aim_data[aim_data.url == kwargs.get('url')]
        if kwargs.get('ip'):
            aim_data = aim_data[aim_data.ip == kwargs.get('ip')]
        if kwargs.get('referer'):
            aim_data = aim_data[aim_data.referer == kwargs.get('referer')]

        if kwargs.get('start_time'):
            aim_data = aim_data[kwargs.get('start_time') < aim_data.request_time.values]

        if kwargs.get('end_time'):
            aim_data = aim_data[aim_data.request_time.values < kwargs.get('end_time')]
        return data_after_argument(aim_data, *args, **kwargs)


