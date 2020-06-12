from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication

from pyprone.core.enums import WnPos, WnStatus
from pyprone.entities import PrText
from pyprone.agents import PrWorld, PrAct, PrTime
from pyprone.views import PrConV, PrMonV

# app
app = QApplication([])

# agents
world = PrWorld('world')
act = PrAct('act', world)
time = PrTime('time')

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

conv.window.activateWindow()

# timer registers
time.register(conv)
time.register(monv)

# code
exit(app.exec_())