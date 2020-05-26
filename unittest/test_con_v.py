from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication

from pyprone.enums.qt import Position
from pyprone.agents import PrWorld, PrAct, PrTime
from pyprone.entities import PrText
from pyprone.views import PrConV

# app
app = QApplication([])

# agents
world = PrWorld('world')
act = PrAct('act', world)
timer = PrTime('timer_con', 100)

# entities
con: PrText = world.find(world.find_id('con'))
mon: PrText = world.find(world.find_id('mon'))

# views
conv = PrConV(
    name='conv',
    world=world,
    act=act,
    target_id=con.id,
    position=Position.BOTTOM_RIGHT,
)
monv = PrConV(
    name='monv',
    world=world,
    act=act,
    target_id=mon.id,
    position=QPoint(2560, 0),
)

# timer registers
timer.register(conv.update, name=conv.name, pid=conv.id)
timer.register(monv.update, name=monv.name, pid=monv.id)

# code
con.append("Hello World")
app.exec_()