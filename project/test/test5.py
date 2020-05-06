import _tkinter
import win32clipboard

import win32com

# xlApp = win32com.client.Dispatch('InternetExplorer.Application')
# print(xlApp)




def clipboard_get():
    """获取剪贴板数据"""
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return data

print(clipboard_get())
