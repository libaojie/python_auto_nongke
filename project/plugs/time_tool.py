#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 时间工具
@Time       : 2019/2/28 11:11
@Author     : libaojie
@File       : time_tool.py
@Software   : PyCharm
"""
import time
from datetime import datetime

from project.plugs.log_tool import LogTool


class TimeTool(object):
    """
    时间工具
    """

    @staticmethod
    def get_currer_time(dateformat=None):
        """
        获取当前时间
        :param dateformat:
        :return:
        """
        return datetime.now()

    @staticmethod
    def get_cur_time():
        return datetime.now().strftime("%Y-%m-%d %H.%M.%S")

    @staticmethod
    def get_unix_time(datetime):
        """

        :param datetime:
        :return:
        """
        return int(time.mktime(datetime.timetuple()))

    @staticmethod
    def get_sql_time():
        # if cd.DEBUG_MYSQL:
        #     return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # else:
        #     return datetime.now()
        return datetime.now()

    @staticmethod
    def get_sql_str(val):
        """
        获取time的sql形式
        :param val:
        :return:
        """
        if val is None or not isinstance(val, datetime):
            return None
        return f"to_date('{TimeTool.get_std_time(val)}','yyyy-mm-dd hh24:mi:ss')"

    @staticmethod
    def get_timestamp():
        """
        保留两位小数
        :return:
        """
        return datetime.now().strftime('%Y%m%d%H%M%S%f')[:-2]

    @staticmethod
    def get_std_time(val):
        """
        转化为标准时间
        :param val:
        :return:
        """
        if val is None or not isinstance(val, datetime):
            return None
        return val.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def is_valid_date(str):
        """
        判断是否是一个有效的日期字符串
        :param str:
        :return:
        """
        try:
            time.strptime(str, "%Y-%m-%d %H:%M:%S")
            return True
        except:
            return False

    @staticmethod
    def get_time_by_str(str):
        try:
            ret = datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
            LogTool.info(f'格式化后的时间为：{ret}')
            return ret
        except:
            return None

    @staticmethod
    def get_month():
        """
        获取当前时间的月份
        :param dateformat:
        :return:
        """
        return time.strftime('%m', time.localtime(time.time()))

    @staticmethod
    def get_day():
        """
        获取当前时间的日
        :param dateformat:
        :return:
        """
        return time.strftime('%d', time.localtime(time.time()))

    @staticmethod
    def get_file_time():
        return time.strftime("%Y%m%d_%H%M%S", time.localtime())
