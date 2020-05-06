from pywinauto.application import Application
import time

app = Application().start('"C:\Program Files (x86)\PesticideModels\TOPRice\TOPrice.exe"')
time.sleep(1)


# app['TOPRice_2.4.2_CN'].menu_select("File")

dlg_spec = app['TOPRice_2.4.2_CN']
print(dlg_spec.print_control_identifiers())