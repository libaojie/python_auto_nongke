#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 程序主入口
@Time       : 2018/5/17 9:50
@Author     : libaojie
@File       : server.py
@Software   : PyCharm
"""
import os
import re

import easygui as e





def open_path_UI(title):
    path = e.enterbox(msg='输入浏览器路径', title=title, default='C:/Users/snow/Desktop/0333-LW24.htm', strip=True, image=None,
                      root=None)
    result_UI(title, path)


def result_UI(title, path):
    if os.path.exists(path):
        ret = run(path)
        if ret:
            msg = "解析结果"
            fields = ["结果"]
            e.multenterbox(msg, title, fields, values=['\t'.join(ret)])
        else:
            e.msgbox("无法正确解析，请检查文本内容！")
    else:
        e.msgbox("文本不存在，请检查路径！")

    open_path_UI(title)


def run(path):
    content = open_file(path)
    ret = []
    par_id = get_par_id(content)
    if par_id is None:
        return None
    ret.append(par_id)

    local = get_local(content)
    ret = ret + local

    # print(par_id)
    par1 = get_par_1(content)
    # print(par1)
    ret.append(par1)
    par2 = get_par_2(content)
    # print(par2)
    ret.append(par2)
    par3 = get_par_3(content)
    # print(par3)
    # ret.append("\t".join(par3))
    ret = ret + par3
    return ret


def get_local(content):
    """
    捞取local
    :param content:
    :return:
    """
    """
    * Location           : Nanchang
    * Meteo station      : Nanchang
    * Soil type          : Nanchang_Soil
    * Crop calendar      : Nanchang-Rice1
    * Substance          : A
    * Application scheme : A-4-2
    * Deposition scheme  : No
    * Irrigation scheme  : Surface_Auto
    *
    * End of PEARL REPORT: Header
    
    * PEARL REPORT: Leaching
    * Start date      :   01-Jan-1901
    * End date        :   31-Dec-1926
    * Target depth    :   1.00 m
    * Annual application to the crop at 10-Aug; dosage =     0.0500 kg.ha-1
    * Annual application to the crop at 17-Aug; dosage =     0.0500 kg.ha-1
    
    * Leaching summary for compound A
    """
    ret = []
    pattern = re.compile(r'\*.+?Location.+?Leaching.+?summary')
    ret = pattern.findall(content)
    # if ret:
    #     for r in ret:
    #         return r

    return ret


def get_par_id(content):
    # pattern = re.compile(r'RUN.+?ID.+?([\d,.]+)')
    pattern = re.compile(r'Run.+?ID.+?([\d,.]+)')
    ret = pattern.findall(content)
    if ret:
        for r in ret:
            return r
    return None


def get_par_3(content):
    # * Target  TWA period    Maximum TWA             TWA
    # * End of TOXSWA REPORT: Time weighted average exposure concentrations (TWA) water layer selected year
    pattern = re.compile(
        r'Target.+?TWA.+?period.+?Maximum.+?TWA[\s\S]+?substance.+?<BR>([\s\S]+?)\*.+?<BR>[\s\S]+?End.+?of.+?TOXSWA.+?REPORT')
    temp = pattern.findall(content)
    ret = []
    if temp:
        for r in temp:
            # TWA1d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.00&nbsp;&nbsp;&nbsp;&nbsp;31-Dec-1920-00h30&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;17.65 <BR>
            pattern1 = re.compile(r'.{7}(\d*\.\d*).{0,3}?<BR>')
            temp2 = pattern1.findall(r)
            for r2 in temp2:
                ret.append(r2)
    return ret


def get_par_1(content):
    # The average concentration of 0333 closest to the 89th percentile is      0.019137 ug/L'
    pattern = re.compile(r'average.+?concentration.+?of.+?percentile.+?is.+?([\d,.]+).+?ug/L')
    ret = pattern.findall(content)
    if ret:
        for r in ret:
            return r
    return None


def get_par_2(content):
    # The 89 percentile peak concentration of 0333 in the pond is     21.787681 ug/L'
    pattern = re.compile(r'peak.+?concentration.+?of.+?pond.+?is.+?([\d,.]+).+?ug/L')
    ret = pattern.findall(content)
    if ret:
        for r in ret:
            return r
    return None


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
        print("打开文件出错")
    finally:
        f.close() if f else None
        return content


# def main():
#     title = "参数解析工具v1.0"
#     open_path_UI(title)
#     # path = e.enterbox(msg='输入浏览器路径', title=title, default='C:/Users/snow/Desktop/0333-LW24.htm', strip=True, image=None, root=None)
#     # if os.path.exists(path):
#     #     ret = run(path)
#     #     if ret:
#     #         msg = "解析结果"
#     #         fields = ["结果"]
#     #         e.multenterbox(msg, title,  fields, values=['\t'.join(ret)])
#     #     else:
#     #         e.msgbox("无法正确解析，请检查文本内容！")
#     # else:
#     #     e.msgbox("文本不存在，请检查路径！")
#
# main()
