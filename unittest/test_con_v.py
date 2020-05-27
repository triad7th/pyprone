from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication

from pyprone.core.enums.qt import WnPos, WnStatus
from pyprone.agents import PrWorld, PrAct, PrTime
from pyprone.entities import PrText
from pyprone.views import PrConV, PrMonV

# app
app = QApplication([])

# agents
world = PrWorld('world')
act = PrAct('act', world)
timer = PrTime('timer_con', 20)

# entities
con: PrText = world.find(world.find_id('con'))
mon: PrText = world.find(world.find_id('mon'))

# views
conv = PrConV(
    name='conv',
    world=world,
    act=act,
    target_id=con.id,
    position=WnPos.BOTTOM_RIGHT,
)
monv = PrMonV(
    name='monv',
    world=world,
    act=act,
    target_id=mon.id,
    position=QPoint(2560, 0),
    status=WnStatus.MAXIMIZED
)

# timer registers
timer.register(conv.update, name=conv.name, pid=conv.id)
timer.register(monv.update, name=monv.name, pid=monv.id)

# code
exit(app.exec_())
