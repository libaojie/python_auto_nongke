#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 日志模块
@Time       : 2018/8/15 15:36
@Author     : libaojie
@File       : log_tool1.py
@Software   : PyCharm
"""
import logging
import os
import shutil
import time
import zipfile


class LogTool(object):
    """
    日志模块
    """
    __instance = None   # 定义一个类属性做判断
    is_init = False     # 是否进行初始化
    path = None         # 文件保存路径
    handler = None      # 文件句柄
    errhandler = None   # 错误句柄
    logger = None       # log句柄
    day = None          # 当前日期
    max_length = 300    # 最大写入长度
    levels = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL, }

    def __new__(cls):
        if cls.__instance is None:
            # 如果__instance为空证明是第一次创建实例
            # 通过父类的__new__(cls)创建实例
            cls.__instance == object.__new__(cls)
            return cls.__instance
        else:
            # 返回上一个对象的引用
            return cls.__instance

    @classmethod
    def init(cls, path):
        """
        初始化
        :param path:
        :return:
        """
        cls.path = path
        cls.logger = logging.getLogger()
        level = 'default'
        cls.logger.setLevel(cls.levels.get(level, logging.NOTSET))
        cls.is_init = True

    # logger可以看做是一个记录日志的人，对于记录的每个日志，他需要有一套规则，比如记录的格式（formatter），
    # 等级（level）等等，这个规则就是handler。使用logger.addHandler(handler)添加多个规则，
    # 就可以让一个logger记录多个日志。


    # 静态方法
    @staticmethod
    def print(log_message):
        if not LogTool.is_init:
            return None
        print(log_message)
        LogTool.info(log_message)

    # 静态方法
    @staticmethod
    def debug(log_message):
        if not LogTool.is_init:
            return None
        LogTool._set_handler('debug')
        LogTool.logger.debug("[DEBUG " + LogTool._get_cur_time() + "]" + log_message)
        LogTool._rm_handler('debug')

    @staticmethod
    def info(log_message):
        if not LogTool.is_init:
            return None
        LogTool._set_handler('info')
        LogTool.logger.info("[INFO " + LogTool._get_cur_time() + "]" + log_message)
        LogTool._rm_handler('info')

    @staticmethod
    def warning(log_message):
        if not LogTool.is_init:
            return None
        LogTool._set_handler('warning')
        LogTool.logger.warning("[WARNING " + LogTool._get_cur_time() + "]" + log_message)
        LogTool._rm_handler('warning')

    @staticmethod
    def error(log_message):
        if not LogTool.is_init:
            return None
        LogTool._set_handler('error')
        _log = "[ERROR " + LogTool._get_cur_time() + "]" + log_message
        print(_log)
        LogTool.logger.error(_log)
        LogTool._rm_handler('error')

    @staticmethod
    def critical(log_message):
        if not LogTool.is_init:
            return None
        LogTool._set_handler('critical')
        LogTool.logger.critical("[CRITICAL " + LogTool._get_cur_time() + "]" + log_message)
        LogTool._rm_handler('critical')

    # ---------------------------------------------
    # 私有函数区
    # ---------------------------------------------


    @classmethod
    def _set_handler(cls, level):
        """
        设置句柄
        :param level:
        :return:
        """
        cls._check_day()
        if level == 'error':
            cls.logger.addHandler(cls.errhandler)
        # 把logger添加上handler
        cls.logger.addHandler(cls.handler)


    @classmethod
    def _rm_handler(cls, level):
        """
        移除句柄
        :param level:
        :return:
        """
        if level == 'error':
            cls.logger.removeHandler(cls.errhandler)
        cls.logger.removeHandler(cls.handler)

    @classmethod
    def _get_handler(cls, day):
        """
        获得句柄
        :param day:
        :return:
        """
        log_filename = os.path.join(cls.path, day, 'log.log')
        err_filename = os.path.join(cls.path, day, 'error.log')
        cls._create_file(log_filename)
        cls._create_file(err_filename)
        # 注意文件内容写入时编码格式指定
        cls.handler = logging.FileHandler(log_filename, encoding='utf-8')
        cls.errhandler = logging.FileHandler(err_filename, encoding='utf-8')

    @classmethod
    def _check_day(cls):
        """
        检查每一天
        :return:
        """
        cur_day = cls._get_cur_day()

        if cls.day:
            if cur_day != cls.day:
                # 压缩过去一天
                cls._zip_file_path(os.path.join(cls.path, cls.day))
                # 新一天
                cls._get_handler(cur_day)
                # 删除过去一天
                cls._delete_file_path(os.path.join(cls.path, cls.day))
        else:
            cls._get_handler(cur_day)
        cls.day = cur_day


    @classmethod
    def _get_cur_time(cls):
        dateformat = '%Y-%m-%d %H:%M:%S'
        return time.strftime(dateformat, time.localtime(time.time()))

    @classmethod
    def _get_cur_day(cls):
        dateformat = '%Y-%m-%d'
        return time.strftime(dateformat, time.localtime(time.time()))

    @classmethod
    def _zip_file_path(cls, input_path):
        """
        压缩文件夹
        :param input_path:
        :return:
        """
        output_name = input_path + '.zip'
        z = zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(input_path):
            fpath = dirpath.replace(input_path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()


    @classmethod
    def _create_file(cls, filename):
        """
        创建文件
        :param filename:
        :return:
        """
        if not os.path.isdir(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        if not os.path.isfile(filename):
            # 创建并打开一个新文件
            fd = open(filename, mode='w', encoding='utf-8')
            fd.close()

    @classmethod
    def _delete_file_path(cls, input_path):
        """
        删除原文件夹
        :param input_path:
        :return:
        """
        if os.path.isdir(input_path):
            shutil.rmtree(input_path)

