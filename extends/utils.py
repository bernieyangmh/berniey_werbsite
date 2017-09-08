# -*- coding: utf-8 -*-
# !/usr/bin/env python


from data_analysis.data import DataCore
from data_analysis.util import print_summary_information
import sys


def data_analysis(path, num):
    print "data_analysis"
    print path
    d = DataCore(path)
    d.generate_data()
    return print_summary_information(d, num=num)
