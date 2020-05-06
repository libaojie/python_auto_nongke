#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 工具箱
@Time       : 2018/7/20 16:20
@Author     : libaojie
@File       : utils.py
@Software   : PyCharm
"""
import uuid


class Utils(object):
    """
    工具类
    """

    @staticmethod
    def get_uuid():
        """
        获取uuid
        :return:

        """
        return uuid.uuid1().hex.upper()

    @staticmethod
    def append_dict(dict1, dict2):
        """
        合并字典
        :param self:
        :param dict1:
        :param dict2:
        :return:
        """
        return dict(dict1, **dict2)

