import ctypes
import win32api
import win32gui
from time import sleep

import win32con


zoom = 1.25

# wdname = "TOPRice_2.4.2_CN"
# #hwnd = win32gui.FindWindow("TfrmAssessments", "TOPRice_2.4.2_CN - Assessments [project: Project_1]")
# hwnd = win32gui.FindWindow("TfrmAssessments", None)
# print(hwnd)
# text = win32gui.GetWindowText(hwnd)  # 获取窗口标题
# print(text)
#win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 600, 300, 600, 600, win32con.SWP_SHOWWINDOW)
#win32gui.ShowWindow(hwnd,win32con.SW_MAXIMIZE)
#win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 10,  10,600,600,win32con.SWP_SHOWWINDOW)


# TPanle = win32gui.FindWindowEx(hwnd, None, "TPanel", None)
# print(TPanle)
# left, top, right, bottom = win32gui.GetWindowRect(TPanle)  # 获取窗口位置
# # left, top是左上角坐标；right, bottom是右下角坐标
# print('窗口位置', left, top, right, bottom)
#button =  win32gui.FindWindowEx(TPanle, None, "text", None)
#print(button)

# 子控件
# hwndChildList = []
# win32gui.EnumChildWindows(TPanle, lambda hwnd, param: param.append(hwnd),  hwndChildList)
# print(hwndChildList)

# <00001> 00130042 S WM_SETCURSOR hwnd:00130042 nHittest:HTCLIENT wMouseMsg:WM_MOUSEMOVE
# SendMessage(00130042,WM_SETCURSOR,00130042,HTCLIENT+WM_MOUSEMOVE*65536)
# <00184> 000F0E7E S WM_SETCURSOR hwnd:000F0E7E nHittest:HTCLIENT wMouseMsg:WM_LBUTTONDOWN
# win32gui.SendMessage(hwnd, win32con.WM_SETCURSOR, menuItemHandle, 0)


# button =  win32gui.FindWindowEx(TPanle, None, "TMemo", None)
# print(button)

def get_hwnd():
    wdname = "TOPRice_2.4.2_CN"
    # hwnd = win32gui.FindWindow("TfrmAssessments", "TOPRice_2.4.2_CN - Assessments [project: Project_1]")
    hwnd = win32gui.FindWindow("TfrmAssessments", None)
    # print(hwnd)
    # text = win32gui.GetWindowText(hwnd)  # 获取窗口标题
    # print(text)

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # 获取窗口位置
    # left, top是左上角坐标；right, bottom是右下角坐标
    print('桌面位置', left, top, right, bottom)

    return hwnd


def get_panel(hwnd):
    TPanle = win32gui.FindWindowEx(hwnd, None, "TPanel", None)
    # print(TPanle)

    # left, top, right, bottom = win32gui.GetWindowRect(TPanle)  # 获取窗口位置
    # # left, top是左上角坐标；right, bottom是右下角坐标
    # print('桌面位置', left, top, right, bottom)
    #
    # left, top, right, bottom = win32gui.GetClientRect(TPanle)  # 获取窗口位置
    # # left, top是左上角坐标；right, bottom是右下角坐标
    # print('窗口位置', left, top, right, bottom)
    return TPanle

def get_pos_project(hwnd):
    project_x = 180

    tpanel = get_panel(hwnd)
    left, top, right, bottom = win32gui.GetWindowRect(tpanel)
    x = right - left
    y = (bottom - top) * zoom
    print(left*zoom+project_x/2, top*zoom + y/2)
    win32api.SetCursorPos([int((left*zoom+project_x/2)/zoom), int((top*zoom + y/2)/zoom)])
    sleep(2)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # print(x*1.5, y*1.5)
    pos = win32gui.GetCursorPos()
    print(pos)


def main():
    hwnd = get_hwnd()
    get_pos_project(hwnd)


main()






