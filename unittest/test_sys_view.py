from PyQt5.QtWidgets import QApplication

from pyprone.objects import PrSys, PrTime
from pyprone.commands import PrSysCmd
from pyprone.views import PrSysView

def syscon():
    app = QApplication([])
    objects = {"syscon": PrSys('')}
    sys_cmd = PrSysCmd(objects)
    sys_view = PrSysView(objects['syscon'], sys_cmd, add_input=True, title='with input')
    sys_time = PrTime(100)
    sys_time.register(sys_view.update)
    app.exec_()

def sysmon():
    app = QApplication([])
    objects = {"sysmon": PrSys("Welcome")}
    sys_view = PrSysView(objects['sysmon'], title='without input')
    sys_time = PrTime(100)
    sys_time.register(sys_view.update)
    app.exec_()


#syscon()
sysmon()
