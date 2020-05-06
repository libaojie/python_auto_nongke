import win32api
import win32gui
from time import sleep

import win32con

from project import constant
from project.plugs.config_tool import ConfigTool


class ProjectUI(object):
    """
    工程列表
    """

    def __init__(self):
        self.class_name = "TfrmProjects"
        self.groupBox_win_name = " Browse Projects "
        self.zoom = ConfigTool.get_float("app", "zoom")  # 屏幕缩放率
        # self.button_y = 56 / self.zoom  # 单个按钮长度
        self.canel_btn_size = (ConfigTool.get_int(constant.type, "canel_btn_size_x") / self.zoom,
                               ConfigTool.get_int(constant.type, "canel_btn_size_y") / self.zoom)  # canel按钮大小
        self.open_btn_size = (ConfigTool.get_int(constant.type, "open_btn_size_x") / self.zoom,
                              ConfigTool.get_int(constant.type, "open_btn_size_y") / self.zoom)  # open按钮大小
        self.hwnd = None
        self.tPanel = None
        # self.project_numb = 3  # 项目数量
        # self.main()
        self._get_hwnd()
        pass

    def _get_hwnd(self):
        self.hwnd = win32gui.FindWindow(self.class_name, None)

    # def _get_right_tpanel(self):
    #     """
    #     右边栏
    #     :return:
    #     """
    #     tGroupBox = win32gui.FindWindowEx(self.hwnd, None, "TGroupBox", self.groupBox_win_name)
    #     self.tPanel = win32gui.FindWindowEx(tGroupBox, None, "TPanel", None)
    #     left, top, right, bottom = win32gui.GetWindowRect(self.tPanel)
    #     self.button_y = (bottom - top) / 7

    def _click_open(self):
        """
        点击打开按钮
        :return:
        """
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        x = right - self.canel_btn_size[0] - self.open_btn_size[0] / 2
        y = bottom - self.open_btn_size[0] / 2
        self._pos(x, y)

    def _pos(self, x, y):
        win32api.SetCursorPos([int(x), int(y)])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        # pos = win32gui.GetCursorPos()

    def _choose_next(self):
        """
        选择下一个工程
        :return:
        """
        # 激活窗口
        win32gui.SetForegroundWindow(self.hwnd)
        win32api.keybd_event(40, 0, 0, 0)  # 下一个
        win32api.keybd_event(40, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键

    def open_next(self):
        self._choose_next()
        sleep(1)
        self._click_open()
        sleep(1)
