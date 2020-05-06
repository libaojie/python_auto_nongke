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
import platform
import subprocess
import tkinter
import win32gui
from datetime import datetime
from time import sleep
from tkinter import *
from tkinter.filedialog import askdirectory, asksaveasfilename

from project.plugs.config_tool import ConfigTool
from project.plugs.decorator import except_fun
from project.plugs.excel_tool import ExcelTool
from project.plugs.show_tool import ShowTool
from project.plugs.type_tool import TypeTool
from project.toprice.assessment_UI import AssessmentUI
from project.toprice.handle_file import HandleFile
from project.toprice.project_UI import ProjectUI

try:
    mainroot = os.path.dirname(os.path.abspath(__file__))
except NameError:
    mainroot = os.path.dirname(os.path.abspath(sys.argv[0]))
ConfigTool.set_path(mainroot)
log_path = os.path.abspath(os.path.join(ConfigTool.get_path(), ConfigTool.get_str("logging", "path")))
from project.plugs.log_tool import LogTool

LogTool.init(log_path)
LogTool.info("------------------启动项目-----------------------------")
LogTool.info(f"平台信息：   【{platform.platform()}】")
LogTool.info(f"当前路径：   【{os.getcwd()}】")
LogTool.info(f"系统变量：   【{sys.path}】")
LogTool.info(f"日志路径：   【{log_path}】")
LogTool.info(f"main路径：   【{ConfigTool.get_path()}】")
LogTool.info(f"python路径： 【{sys.executable}】")


class MainUI(object):

    def __init__(self):
        self.windowUI = None
        self.ret_text = None
        self.run_text = None
        self.num_entry = None
        self.class_name = "TkTopLevel"
        self.hwnd = None
        self.exe_path = ConfigTool.get_str("app", "exe_path")
        self.result_list = []
        pass

    def ov(self):
        # ov = datetime.strptime("2020-05-04 22:25:00", "%Y-%m-%d %H:%M:%S")
        # if datetime.now() > ov:
        #     LogTool.error("程序奔溃啦！ 快点联系开发者！")
        #     return False
        return True

    def _get_hwnd(self):
        self.hwnd = win32gui.FindWindow(self.class_name, None)

    def main(self):
        if not self.ov():
            LogTool.error("程序奔溃啦！ 快点联系开发者！")
            return
        title = "参数解析工具v3.0"
        self.windowUI = Tk(className=title)

        self.windowUI.geometry('320x560+0+0')

        padx = 3
        pady = 2

        fm1 = Frame(self.windowUI)
        # 打开程序
        open_btn = Button(fm1, text="打开程序", command=self._open_btn_back)
        open_btn.grid(row=0, column=0, padx=padx, pady=pady)

        # 下个项目
        next_pro_btn = Button(fm1, text="下个项目", command=self._next_pro_btn_back)
        next_pro_btn.grid(row=0, column=1, padx=padx, pady=pady)

        # 清空结果
        clear_btn = Button(fm1, text="清空结果", command=self._clear_btn_back)
        clear_btn.grid(row=0, column=2, padx=padx, pady=pady)

        # 保存结果
        save_btn = Button(fm1, text="保存结果", command=self._save_btn_back)
        save_btn.grid(row=0, column=3, padx=padx, pady=pady)

        fm1.grid(row=0)

        fm2 = Frame(self.windowUI)

        label = Label(fm2, text="输入报告数量：")
        label.grid(row=0, column=0, padx=padx, pady=pady)

        self.num_entry = Entry(fm2)
        self.num_entry.insert("insert", 1)
        self.num_entry.grid(row=0, column=1, padx=padx, pady=pady)

        # 开始按钮
        start_btn = Button(fm2, text="开始处理", command=self._start_btn_back)
        start_btn.grid(row=0, column=2, padx=padx, pady=pady)

        fm2.grid(row=1)

        fm3 = Frame(self.windowUI)

        label = Label(fm3, text="运行日志：")
        label.grid(row=0, column=0, padx=padx, pady=pady)
        # 结果展示
        self.run_text = Text(fm3, width=20, height=30)
        self.run_text.grid(row=1, column=0, padx=padx, pady=pady)
        ShowTool.init(self.run_text)

        label = Label(fm3, text="结果列表：")
        label.grid(row=0, column=1, padx=padx, pady=pady)
        # 结果展示
        self.ret_text = Text(fm3, width=20, height=30)
        self.ret_text.grid(row=1, column=1, padx=padx, pady=pady)

        fm3.grid(row=2)

        mainloop()
        sleep(1)
        self._get_hwnd()

    def _next_btn_back(self):
        """
        切换下一个
        :return:
        """
        LogTool.info("开始下个报告")
        assessmentUI = AssessmentUI()
        assessmentUI.choose_next()
        self._handle()

    def _next_pro_btn_back(self):
        """
        切换下一个项目
        :return:
        """
        self._show_run("开始切换项目")
        assessmentUI = AssessmentUI()
        assessmentUI.open_project()
        sleep(0.1)
        projectUI = ProjectUI()
        projectUI.open_next()
        self._show_run("切换下个项目\n")

    def _clear_btn_back(self):
        """
        清空结果
        :return:
        """
        self.result_list = []
        self.ret_text.delete(1.0, END)
        self._show_run("清空结果")

    @except_fun
    def _start_btn_back(self):
        """
        开始按钮回调
        :return:
        """
        numb = self.num_entry.get()
        self._show_run(f"开始处理{numb}份报告")
        numb = TypeTool.change_to_int(numb)
        if numb is None:
            self._show_run(f"请输入大于0的正整数！")
            return

        for i in range(numb):
            self._show_run(f"开始处理第{i+1}份报告")
            self._handle()
            sleep(0.5)
            self._show_run(f"结束处理第{i+1}份报告")
            self._set_focus()
            if not i == numb - 1:
                self._show_run("开始下一份报告")
                assessmentUI = AssessmentUI()
                assessmentUI.choose_next()
                self._show_run("下一份报告切换完毕")
        self._show_run("处理报告完毕")
        self._set_focus()

    def _handle(self):
        """
        处理当前报告
        :return:
        """
        LogTool.info("开始生成报告")
        assessmentUI = AssessmentUI()
        assessmentUI.set_fore()
        assessmentUI.open_report()
        sleep(2)
        LogTool.info("获取地址")
        url = assessmentUI.get_url()
        self._show_run("---------\n")
        self._show_run(f"URL:{url}\n")
        LogTool.info("解析参数")
        # 聚焦
        self._set_focus()
        handleFile = HandleFile(url)
        content = handleFile.run()
        self.result_list.append(content)
        content = "\t".join(content)
        self._show_run(f"解析结果:\n")
        self._show_ret(f"{content}\n")

    def _show_ret(self, content):
        if not self.ov():
            LogTool.error("程序奔溃啦！ 快点联系开发者！")
            self.run_text.insert(INSERT, "程序奔溃啦！ 快点联系开发者！")
            return
        self.ret_text.insert(INSERT, content)
        self._show_run(content)

    def _show_run(self, content):
        """
        显示
        :param content:
        :return:
        """
        if not self.ov():
            LogTool.error("程序奔溃啦！ 快点联系开发者！")
            self.run_text.insert(INSERT, "程序奔溃啦！ 快点联系开发者！")
            return
        LogTool.info(content)
        self.run_text.insert(INSERT, content)

    def _open_btn_back(self):
        """
        打开程序回调
        :return:
        """
        subprocess.Popen(self.exe_path)
        sleep(1)
        # 聚焦
        self._set_focus()
        pass

    def _save_btn_back(self):
        """
        保存结果回调
        :return:
        """
        self._show_run("保存结果集")
        if len(self.result_list) < 1:
            self._show_run("未解析出结果，无需保存！")
            return

        options = {}
        options['filetypes'] = [('all files', '.xlsx')]

        _path = asksaveasfilename(**options)
        self._show_run(f"保存路径为{_path}")

        ExcelTool.save_to_excel(["run_id"], self.result_list, f"{_path}.xls")
        self._show_run(f"保存成功")
        pass

    def _set_focus(self):
        # self.windowUI.wm_attributes('-topmost', 1)
        self._get_hwnd()
        win32gui.SetForegroundWindow(self.hwnd)


mainUI = MainUI()
mainUI.main()
