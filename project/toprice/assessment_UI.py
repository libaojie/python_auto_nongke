import win32api
import win32clipboard
import win32gui
import win32process
from time import sleep

import win32con

from project import constant
from project.plugs.config_tool import ConfigTool
from project.plugs.log_tool import LogTool


class AssessmentUI(object):

    def __init__(self):
        self.class_name = "TfrmAssessments"
        self.hwnd = None
        self.tPanel = None
        self.zoom = ConfigTool.get_float("app", "zoom")
        self.project_x = ConfigTool.get_int(constant.type, "project_x") / self.zoom
        self.calculate_x = ConfigTool.get_int(constant.type, "calculate_x") / self.zoom
        self.report_x = ConfigTool.get_int(constant.type, "report_x") / self.zoom

        self._get_hwnd()
        self._get_panel()
        pass

    def _get_hwnd(self):
        self.hwnd = win32gui.FindWindow(self.class_name, None)

    def _get_panel(self):
        self.tPanel = win32gui.FindWindowEx(self.hwnd, None, "TPanel", None)

    def set_fore(self):
        win32gui.SetForegroundWindow(self.hwnd)

    def open_project(self):
        """
        点击Project按钮
        :return:
        """
        self.set_fore()
        left, top, right, bottom = win32gui.GetWindowRect(self.tPanel)
        x = right - left
        y = bottom - top
        self._pos(left + self.project_x / 2, top + y / 2)

    def open_report(self):
        """
        打开报告
        :return:
        """
        win32gui.SetForegroundWindow(self.hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(self.tPanel)
        x = right - left
        y = bottom - top
        self._pos(left + self.project_x + self.calculate_x + self.report_x / self.zoom / 2, top + y / 2)

    def choose_next(self):
        """
        选择下一个工程
        :return:
        """
        # 激活窗口
        win32gui.SetForegroundWindow(self.hwnd)
        win32api.keybd_event(40, 0, 0, 0)  # 下一个
        win32api.keybd_event(40, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键

    def _pos(self, x, y):
        """
        点击
        :param x:
        :param y:
        :return:
        """
        LogTool.info(f"点击鼠标【{x}】【{y}】")
        win32api.SetCursorPos([int(x), int(y)])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        # pos = win32gui.GetCursorPos()

    # def open_next_report(self):
    #     """
    #     打开下一份报告
    #     :return:
    #     """
    #     self._choose_next()
    #     sleep(1)
    #     self.open_report()

    def get_url(self):
        """
        获取生成报告地址
        :return:
        """
        processId = None
        content = None
        cur_client = None
        # 获取浏览器
        for i in range(3):
            cur_client = win32gui.GetForegroundWindow()
            name = win32gui.GetClassName(cur_client)
            thread, processId = win32process.GetWindowThreadProcessId(cur_client)
            LogTool.info(f"当前应用名【{name}】")
            if "WidgetWin" in name:
                LogTool.info("找到了浏览器！")
                break
            sleep(1)
            win32api.keybd_event(13, 0, 0, 0)  # 回车
            win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键

        # 杀死进程
        # os.kill(processId, signal.CTRL_C_EVENT)

        # 点击一下
        left, top, right, bottom = win32gui.GetWindowRect(cur_client)
        x = right - left
        y = bottom - top
        self._pos(left + x / 2, top + y / 2)
        sleep(0.1)

        # 通过tab方式获取url
        for i in range(5):
            win32gui.SetActiveWindow(cur_client)
            win32gui.SetForegroundWindow(cur_client)
            win32api.keybd_event(9, 0, 0, 0)  # tab
            win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
            sleep(0.5)

            # 清空 剪切板
            self.clipboard_set("")
            sleep(0.1)

            # 全选
            win32api.keybd_event(17, 0, 0, 0)  # Ctrl
            win32api.keybd_event(65, 0, 0, 0)  # A
            win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
            win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
            sleep(0.1)
            # 复制
            win32api.keybd_event(17, 0, 0, 0)  # Ctrl
            win32api.keybd_event(67, 0, 0, 0)  # C
            win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
            win32api.keybd_event(67, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
            sleep(0.1)
            temp = self.clipboard_get()
            LogTool.info(f"剪切板内容【{temp}】")
            if "htm" in temp:
                content = temp
                LogTool.info(f"找到了网址{content}")
                break

        return content

    def clipboard_get(self):
        """
        获取剪贴板数据
        :return:
        """
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        return data

    def clipboard_set(self, data):
        """设置剪贴板数据"""
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, data)
        win32clipboard.CloseClipboard()

# assessmentUI = AssessmentUI()
# assessmentUI.open_report()
# assessmentUI.test()
