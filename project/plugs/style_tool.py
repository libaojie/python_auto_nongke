#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 编程格式转换
@Time       : 2019/9/24 9:08
@Author     : libaojie
@File       : style_tool.py
@Software   : PyCharm
"""
import re


class StyleTool(object):
    """
    str类型格式转化
    """

    @staticmethod
    def _2Upper(str):
        """
        _转驼峰命名
        :param str:
        :return:
        """
        str = str.lower()
        _list = str.split('_')
        _list = [StyleTool.first_upper(s) for s in _list]
        str = "".join(_list)
        return str

    @staticmethod
    def upper2_(str):
        """
        驼峰转_ 全小写
        :param str:
        :return:
        """
        pattern = "[A-Z]"
        val = re.sub(pattern, lambda x: "_" + x.group(0), str)
        return val.lower()

    @staticmethod
    def first_upper(str):
        """
        首字母大写
        :param str:
        :return:
        """
        _list = list(str)
        _list[0] = _list[0].upper()
        str = "".join(_list)
        return str

    @staticmethod
    def first_lower(str):
        """
        首字母小写
        :param str:
        :return:
        """
        _list = list(str)
        _list[0] = _list[0].lower()
        str = "".join(_list)
        return str

    @staticmethod
    def get_short(str):
        """
        获取缩写
        :param str:
        :return:
        """
        str = str.lower()
        _list = str.split('_')
        _ret = [s[0] for s in _list]
        return "".join(_ret)
