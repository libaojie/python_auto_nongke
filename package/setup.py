#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2018/11/9 10:15
# @Author     : xnchall
# @Description:
# @File       :
# @Software   : PyCharm

import opcode
import platform
import sys

import xlwt
from cx_Freeze import setup, Executable
import os


class Package(object):
    """
    打包类
    """

    def __init__(self):
        """
        初始化
        """
        self.python_path = os.path.dirname(os.path.dirname(os.__file__))
        self.build_exe_options = None
        self.executables = None

        # 设置运行环境
        try:
            approot = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            approot = os.path.dirname(os.path.abspath(sys.argv[0]))
        sys.path.append(os.path.split(approot)[0])

        print("----------------------------")
        print("输出参数：")
        print(f"self.python_path:【{self.python_path}】")
        print(f"approot:【{approot}】")
        print("----------------------------")

    def run(self):
        """
        运行
        :return:
        """
        self._init_data()
        self.__setup()
        pass

    def _init_data(self):
        """
        分平台初始化参数
        :return:
        """
        raise Exception('子类中必须实现该方法')

    def __setup(self):
        """
        打包
        :return:
        """
        setup(name='project',
              version='0.1',
              description='Sample cx_Freeze script',
              options={"build_exe": self.build_exe_options},
              executables=self.executables,
              )


class LinuxPackage(Package):
    """
    Linux打包
    """

    def _init_data(self):
        """
        设置环境变量
        :return:
        """
        os.environ['TCL_LIBRARY'] = os.path.join(self.python_path, 'tcl', 'tcl8.6')
        os.environ['TK_LIBRARY'] = os.path.join(self.python_path, 'tcl', 'tk8.6')
        distutils_path = os.path.join(os.path.dirname(opcode.__file__), 'distutils')

        self.build_exe_options = {
            'packages': ['pandas',
                         'numpy',
                         'asyncio'
                         ],
            'include_files': [(distutils_path, 'lib/distutils'),
                              'linux/start.sh',
                              'linux/stop.sh'],
            'includes': "idna.idnadata",
            'excludes': ['distutils']
        }

        self.executables = [
            Executable('../project/main.py')
        ]

    pass


class WindowsPackage(Package):
    """
    Windows打包
    """

    def _init_data(self):
        """
        初始化数据
        :return:
        """
        # 设置环境变量
        # TCL_LIBRARY = C:\Users\VergilTheHuragok\AppData\Local\Programs\Python\Python35\tcl\tcl8
        # TK_LIBRARY = C:\Users\VergilTheHuragok\AppData\Local\Programs\Python\Python35\tcl\tk8
        os.environ['TCL_LIBRARY'] = os.path.join(self.python_path, 'tcl', 'tcl8.6')
        os.environ['TK_LIBRARY'] = os.path.join(self.python_path, 'tcl', 'tk8.6')
        tcl86t = os.path.join(self.python_path, 'DLLS', 'tcl86t.dll')
        tk86t = os.path.join(self.python_path, 'DLLS', 'tk86t.dll')
        xlwt_lexer_path = os.path.join(os.path.dirname(xlwt.__file__), 'ExcelFormulaLexer.py')
        xlwt_parser_path = os.path.join(os.path.dirname(xlwt.__file__), 'ExcelFormulaParser.py')

        self.build_exe_options = {
            'packages': ['asyncio', 'easygui.boxes.global_state'],
            "include_files": [tcl86t, tk86t, '../project/config.conf',
                              (xlwt_lexer_path, 'lib/xlwt/ExcelFormulaLexer.py'),
                              (xlwt_parser_path, 'lib/xlwt/ExcelFormulaParser.py')
                              ]
        }

        self.executables = [
            Executable('../project/main.py', base="Win32GUI")
        ]

    pass


# 运行打包
package = None
if 'Windows' in platform.platform():
    package = WindowsPackage()
elif 'Linux' in platform.platform():
    package = LinuxPackage()

if package is not None:
    package.run()
