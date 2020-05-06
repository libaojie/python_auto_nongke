#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 类型工具
@Time       : 2019/2/28 11:16
@Author     : libaojie
@File       : type_tool.py
@Software   : PyCharm
"""
# import numpy
from project.plugs.log_tool import LogTool


class TypeTool(object):
    """
    类型工具
    """

    @staticmethod
    def change_to_int(numb):
        """
        转化为int
        :param numb:
        :return:
        """
        _result = None

        if isinstance(numb, int):
            return numb

        # isinstance(numb, numpy.int64) or isinstance(numb, numpy.float64)
        # if isinstance(numb, str) or isinstance(numb, float):
        #     try:
        #         _result = int(numb)
        #     except Exception as e:
        #         LogTool.error("{0}转int失败：{1}".format(type(numb), numb))
        #     finally:
        #         return _result
        try:
            _result = int(numb)
        except Exception as e:
            LogTool.error("{0}转int失败：{1}".format(type(numb), numb))
        finally:
            return _result

    @staticmethod
    def change_to_str(val):
        """
        转化str
        :param val:
        :return:
        """
        _result = None

        if val is None:
            return None

        if isinstance(val, str):
            return val

        if isinstance(val, int):
            _result = str(val)
        else:
            try:
                _result = str(val)
            except Exception as e:
                LogTool.error("{0}转str失败：{1}".format(type(val), val))
        return _result

    @staticmethod
    def is_null(val):
        '''
        检测不明类型是否为空
        :param val:
        :return:
        '''
        if val is None:
            return True

        if isinstance(val, str) and val.strip() == '':
            return True

        if isinstance(val, list) and len(val) == 0:
            return True

        return False

    @staticmethod
    def get_val_by_dict(dict_data, key):
        """
        字典取值
        :param dict_data:
        :param key:
        :return:
        """
        if isinstance(dict_data, dict) and dict_data.__contains__(key):
            return dict_data[key]
        return None
