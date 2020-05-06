import os
import subprocess
from time import sleep

import uiautomation as auto

print(auto.GetRootControl())
# subprocess.Popen('notepad.exe')
# notepadWindow = automation.WindowControl(searchDepth=1, ClassNam='Notepad')
# print(notepadWindow.Name)
# notepadWindow.SetTopmost(True)
# edit = notepadWindow.EditControl()
# edit.SetValue('Hello')
# edit.SendKeys('{Ctrl}{End}{Enter}World')

subprocess.Popen('C:\Program Files (x86)\PesticideModels\TOPRice\TOPrice.exe')
window = auto.WindowControl(searchDepth=1,  title_re = 'TOPrice*')
if auto.WaitForExist(window, 3):
    auto.Logger.WriteLine("Notepad exists now")
else:
    auto.Logger.WriteLine("Notepad does not exist after 3 seconds", auto.ConsoleColor.Yellow)
window.SetActive()
# windowFont = window.WindowControl(Name='File')
# print(window.Name)
# window.window_(title_re = u'File').Click()
# #
# window.SetTopmost(True)
# window.ButtonControl(name="Projects").Click()

# button = auto.ButtonControl(Name='Projects')
# button.Click()

button = auto.FindControl(window, lambda c:(isinstance(c, auto.EditControl) or isinstance(c, auto.ComboBoxControl)) and c.Name == 'Projects')
button.Click()
sleep(10)


# os.system(r"python -m poetry run python C:\Users\snow\AppData\Local\pypoetry\Cache\virtualenvs\read-html-venv--Gq2blu2-py3.6\Scripts\automation.py -r –d1 –t3 -n")
