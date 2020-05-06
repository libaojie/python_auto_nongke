#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 对象工具
@Time       : 2020/2/5 15:32
@Author     : libaojie
@File       : object_tool.py
@Software   : PyCharm
"""


class ObjectTool(object):
    """
    对象工具
    """

    @staticmethod
    def change_to_dict(obj):
        """
        对象转字典
        :param obj:
        :return:
        """
        pr = {}
        for name in dir(obj):
            value = getattr(obj, name)
            if not name.startswith('__') and not name.startswith('_') and not callable(value):
                pr[name] = value
        return pr