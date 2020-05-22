from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication

from pyprone.objects import PrSys, PrTime
from pyprone.commands import PrSysCmd
from pyprone.views import PrSysView
  
app = QApplication([])

objects = {
    'sysmon': PrSys(''),
    'syscon': PrSys("welcome to the syscon..."),
    'syscon_time': PrTime(100)
}

# creating sysmon
sysmon_view = PrSysView(objects['sysmon'], title='system monitor', pos=QPoint(0, -450))

# creating syscon
syscon_cmd = PrSysCmd(objects)
syscon_cmd.mon('syscon created...')
syscon_view = PrSysView(objects['syscon'], syscon_cmd, add_input=True, title='system console')

# timers
syscon_cmd.mon('timer settings...')
objects['syscon_time'] = PrTime(100)
objects['syscon_time'].register(syscon_view.update)
objects['syscon_time'].register(sysmon_view.update)

app.exec_()
