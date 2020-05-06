#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 压缩处理
@Time       : 2018/5/25 10:37
@Author     : libaojie
@File       : zip_tool.py
@Software   : PyCharm
"""
import os
import zipfile

from project.plugs.log_tool import LogTool


class ZipTool(object):
    """
    压缩工具
    """

    @classmethod
    def zip_file_path(cls, input_path, output_name):
        # output_name = input_path + '.zip'  # 压缩后文件夹的名字
        z = zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
        for dirpath, dirnames, filenames in os.walk(input_path):
            fpath = dirpath.replace(input_path, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
                LogTool.info("压缩成功")
        z.close()
