#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 文件工具
@Time       : 2020/2/18 16:16
@Author     : libaojie
@File       : file_tool.py
@Software   : PyCharm
"""
import os

from project.plugs.log_tool import LogTool


class FileTool(object):
    """
    文件工具
    """

    @staticmethod
    def is_file(file_path):
        """
        判断文件和文件夹是否存在，不存在自动创建文件夹
        :param file_path:
        :return:
        """
        if os.path.exists(file_path):
            LogTool.info("文件路径【%s】存在" % file_path)
        else:
            dir_name = os.path.dirname(file_path)
            if not os.path.exists(dir_name):
                LogTool.info("文件路径【%s】不存在，将自动创建" % file_path)
                os.makedirs(dir_name)
                LogTool.info("路径创建【%s】完成" % dir_name)

    @staticmethod
    def open_file(file_path):
        """
        打开文件操作
        :param file_path: 文件路径
        :return:
        """
        f = None
        content = None
        try:
            with open(file_path, 'r+', encoding='utf8') as f:
                content = f.read()
        except Exception:
            LogTool.error("打开文件出错")
        finally:
            f.close() if f else None
            return content

    @staticmethod
    def write_file(file_path):
        """
        写文件
        :param file_path:
        :return:
        """
        w = None
        try:
            w = open(file_path, 'w+')
            return w
        except Exception:
            LogTool.error("打开文件【%s】出错" % file_path)
            w.close() if w else None
            return None

    @staticmethod
    def del_file(path):
        """
        删除此路径下所有文件及文件夹
        :param path:
        :return:
        """
        if os.path.isdir(path):
            for i in os.listdir(path):
                path_file = os.path.join(path, i)
                FileTool.del_file(path_file)
            # 删除文件夹
            os.rmdir(path)
        elif os.path.isfile(path):
            # 删除文件
            os.remove(path)

    @staticmethod
    def mkdir_parent_file(path):
        """
        创建文件的父菜单
        :param path:
        :return:
        """
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
