#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 装饰器
@Time       : 2018/7/20 16:23
@Author     : libaojie
@File       : decorator.py
@Software   : PyCharm
"""

import datetime as dt
import traceback
from threading import Thread

from project.plugs.log_tool import LogTool


def except_fun(func):
    """
    获取函数异常
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        try:
            _ret = func(*args, **kwargs)
            return _ret
        except Exception as err:
            LogTool.error(traceback.format_exc())
            LogTool.info(f'函数异常：【{str(func)}】, args:【{args}】， kwargs:【{kwargs}】')
            return None
    return wrapper


def log_fun(func):
    """
    获取执行函数名
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        LogTool.info('开始函数：【{0}】'.format(func.__name__))
        # LogTool.info(f'参数：【{args}】【{kwargs}】')
        _stime = dt.datetime.now()
        _ret = func(*args, **kwargs)
        _etime = dt.datetime.now()
        LogTool.info('结束函数：【{0}】, 执行时间：【{1}】'.format(func.__name__, _etime - _stime))
        return _ret

    return wrapper


def async(f):
    """
    异步多线程
    :param f:
    :return:
    """

    def wrapper(*args, **kwargs):
        LogTool.info(f"开启多线程")
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper
