import win32api
import win32gui
from time import sleep

zoom = 1.25
project_x = 180 / zoom
calculate_x = (370 - project_x) / zoom
report_x = (585 - calculate_x - project_x) / zoom


def get_hwnd():
    wdname = "TOPRice_2.4.2_CN"
    hwnd = win32gui.FindWindow("TfrmAssessments", None)
    return hwnd


def get_panel(hwnd):
    TPanle = win32gui.FindWindowEx(hwnd, None, "TPanel", None)
    return TPanle


def get_pos_project(hwnd):
    tpanel = get_panel(hwnd)
    left, top, right, bottom = win32gui.GetWindowRect(tpanel)
    x = right - left
    y = bottom - top
    win32api.SetCursorPos([int(left + project_x / 2), int(top + y / 2)])
    sleep(2)
    pos = win32gui.GetCursorPos()


def get_pos_calculate(hwnd):
    tpanel = get_panel(hwnd)
    left, top, right, bottom = win32gui.GetWindowRect(tpanel)
    x = right - left
    y = bottom - top
    win32api.SetCursorPos([int(left + project_x + calculate_x / 2), int(top + y / 2)])
    sleep(2)
    pos = win32gui.GetCursorPos()


def get_pos_report(hwnd):
    tpanel = get_panel(hwnd)
    left, top, right, bottom = win32gui.GetWindowRect(tpanel)
    x = right - left
    y = bottom - top
    win32api.SetCursorPos([int(left + project_x + calculate_x + report_x / zoom / 2), int(top + y / 2)])
    sleep(2)
    pos = win32gui.GetCursorPos()


def main():
    hwnd = get_hwnd()
    # get_pos_project(hwnd)
    # get_pos_calculate(hwnd)
    get_pos_report(hwnd)


main()
