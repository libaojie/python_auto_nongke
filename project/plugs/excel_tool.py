#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    :
@Time       : 2019/2/25 9:01
@Author     : libaojie
@File       : excel_tool.py
@Software   : PyCharm
"""
import os
import shutil
import traceback

import xlrd
import xlwt
from xlutils.copy import copy

from project.plugs.log_tool import LogTool


class ExcelTool(object):

    @staticmethod
    def get_all_excel_files(path):
        '''
        获取指定目录下所有的Excel文件
        Params:
            ppath: String 存放Excel的根目录
        Return:
            指定目录下所有的Excel文件
        '''

        _files = []  # 存放返回的文件列表
        _dir_cnt = 0  # 记录包含文件的文件夹数量

        # 遍历所有文件夹，获取相应的信息
        for _dirpath, _dirnames, _filenames in os.walk(path):
            # 遍历文件夹中的文件
            _dir_cnt += 1
            for _filename in _filenames:
                # 将所有的Excel文件（剔除了临时文件）加载到文件列表中
                if (os.path.splitext(_filename)[1] in ['.xlsx', '.xls']
                ) and (not _filename.startswith('~')):
                    _files.append(os.path.join(_dirpath, _filename))
        # print('包含Excel文件的目录共【{}】个'.format(_dir_cnt))

        if len(_files) < 1:
            # 文件夹内无Excel文件
            LogTool.error("文件夹内无Excel：{0}".format(path))

        return _files

    @staticmethod
    def get_excel_file(path):
        '''
        获取Excel文件
        Params:
            path: String Excel路径
        Return:
            Excel文件
        '''
        try:
            _excel = xlrd.open_workbook(path)
            if not _excel:
                LogTool.error('无此Excel！！！{0}'.format(path))
            return _excel
        except Exception as err:
            LogTool.error(traceback.format_exc())
            LogTool.print(f'Excel文件无法读取')
            return None

    @staticmethod
    def save_to_excel(pheader, pvals, pfname, header_style=None, val_style=None, psname='Sheet1'):
        '''
        保存数据至Excel
        :param pheader: List 标题
        :param pvals: List 内容
        :param pfname: String 路径
        :param header_style: 标题格式
        :param val_style:  内容格式
        :param psname: sheet名称
        :return:
        '''
        if not os.path.isdir(os.path.dirname(pfname)):
            os.makedirs(os.path.dirname(pfname))

        _workbook = xlwt.Workbook(encoding='utf8')  # 创建工作簿对象
        _xlssheet = _workbook.add_sheet(psname)

        # 填充标题
        for _i, _v in enumerate(pheader):
            if header_style is None:
                _xlssheet.write(0, _i, _v)
            else:
                _xlssheet.write(0, _i, _v, header_style)

        # 填充内容
        for _r, _rv in enumerate(pvals):
            for _c, cv in enumerate(_rv):
                cv = str(cv)
                # 一个单元格最长为32766
                if len(cv) > 32766:
                    LogTool.error('写入Excel字段超长！长度{0}'.format(len(cv)))
                    cv = cv[:32766]

                if val_style is None:
                    _xlssheet.write(_r + 1, _c, cv)
                else:
                    _xlssheet.write(_r + 1, _c, cv, val_style)

        # 保存excel文件
        _workbook.save(pfname)

    @staticmethod
    def copy_templet(input_path, output_path):
        """
        复制一下模板
        :param input_path:
        :param output_path:
        :return:
        """
        shutil.copy(input_path, output_path)
        return output_path

    @staticmethod
    def templet_excel(pvals, pfname, psindex, ptitle_rnt=0, ptitle_cnt=0, is_by_row=True, val_style=None,
                      is_auto_col=False, is_new_sheet=False):
        """
        按模板输出Excel
        :param pvals: 数据
        :param pfname: 模板路径
        :param psindex: sheet序号
        :param ptitle_rnt: 标题行数
        :param ptitle_cnt: 标题列数
        :param is_by_row: 是否按行写入
        :param is_auto_col：
        :param is_new_sheet: 是否是新添的sheet
        :return:
        """
        _workbook = xlrd.open_workbook(pfname, formatting_info=True)
        _wb = copy(_workbook)
        if is_new_sheet:
            _sheet = _wb.add_sheet(psindex)
        else:
            _sheet = _wb.get_sheet(psindex)

        max_length_dict = {}
        for _r, _rv in enumerate(pvals):
            for _c, cv in enumerate(_rv):
                # 写入内容
                if is_by_row:
                    # 按行写入
                    _r_result = _r + ptitle_rnt
                    _c_result = _c + ptitle_cnt
                else:
                    # 按列写入
                    _r_result = _c + ptitle_rnt
                    _c_result = _r + ptitle_cnt

                # 一个sheet 最多可以写65535*255个单元格
                if _r_result > 65535 or _c_result > 255:
                    LogTool.error('写入文件过大，超过行列数据被舍弃：{0} - {1}'.format(_r_result, _c_result))
                    continue

                cv = str(cv)
                # 一个单元格最长为32766
                if len(cv) > 32766:
                    LogTool.error('写入Excel字段超长！长度{0}'.format(len(cv)))
                    cv = cv[:32766]

                if val_style is None or _c_result >= len(val_style):
                    _sheet.write(_r_result, _c_result, cv)
                    # if re.match('file://', cv):
                    #     # 文本内容为本地文件
                    #     formula = xlwt.Formula('HYPERLINK("{0}";"{1}")'.format(cv[7:], cv[7:]))
                    #     _sheet.write(_r_result, _c_result, formula)
                else:
                    _sheet.write(_r_result, _c_result, cv, val_style[_c_result])
                    # if re.match('file://', cv):
                    #     # 文本内容为本地文件
                    #     formula = xlwt.Formula('HYPERLINK("{0}";"{1}")'.format(cv[7:], cv[7:]))
                    #     _sheet.write(_r_result, _c_result, formula)

                # 更新最长字符数
                if max_length_dict.__contains__(_c_result):
                    if max_length_dict[_c_result] < len(cv):
                        max_length_dict[_c_result] = len(cv)
                else:
                    max_length_dict[_c_result] = len(cv)

        # 更新列宽
        if is_auto_col:
            for key, value in max_length_dict.items():
                _val = value * 256
                _val = _val if _val < 65536 else 65535
                _sheet.col(key).width = _val

        _wb.save(pfname)
