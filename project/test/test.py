import win32gui

wdname = "TOPRice_2.4.2_CN"
hwnd = win32gui.FindWindow(None, wdname)
print(hwnd)
text = win32gui.GetWindowText(hwnd)  # 获取窗口标题
print('窗口标题为:', text)
clsname = win32gui.GetClassName(hwnd)  # 获取窗口类名
print('窗口类名:', clsname)
left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # 获取窗口位置
# left, top是左上角坐标；right, bottom是右下角坐标
print('窗口位置', left, top, right, bottom)

menuHandle = win32gui.GetMenu(hwnd)  # 获取窗口的菜单句柄
print('记事本菜单句柄：', menuHandle)

# 关闭窗口
win32gui.CloseWindow(hwnd)
# #获取第一个子UI句柄
# w2hd=win32gui.FindWindowEx(hwnd,None,None,"File")
# print(w2hd)


# 调用win32gui.EnumWindows()枚举所有窗口句柄
# hWndList = []
# win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
# for hwnd in hWndList:
#     title = win32gui.GetWindowText(hwnd)
#     print(title)
