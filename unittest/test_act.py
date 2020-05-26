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

# views
conv = PrConV(
    name='conv',
    world=world,
    act=act,
    target_id=con.id,
    position=Position.BOTTOM_RIGHT,
)

# timer registers
timer.register(conv.update, name=conv.name, pid=conv.id)

# code
con.append("Hello World")
app.exec_()