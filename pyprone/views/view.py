from typing import Union

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QWidget

from pyprone.core.enums.qt import WnPos, WnStatus
from pyprone.core import PrObjCb
from pyprone.entities import PrText, PrTextFactory
from pyprone.agents import PrWorld, PrAct

import pyprone.core.helpers as PrHelper

class PrView(PrObjCb):
    """
    view bass class
    """
    def __init__(self,
        name: str,
        world: PrWorld,
        act: PrAct,
        target_id: int,
        position: Union[WnPos, QPoint] = WnPos.NONE,
        status: WnStatus = WnStatus.NONE):
        """
        name : name of this view
        target_id : PrObj id to show in this iew
        """
        super().__init__(name)

        # agents
        self.world = world
        self.act = act

        # entities
        self.id_to_show = target_id

        # window
        self.window: QWidget = None
        self.position: Union[WnPos, QPoint] = position
        self.status: WnStatus = status

        # build
        self.build()

    @property
    def id_to_show(self):
        """ PrObj id to show """
        return self._id_to_show

    @id_to_show.setter
    def id_to_show(self, target_id: int):
        """ PrObj is automatcially assigned/created when id_to_show is changed """
        self._id_to_show = target_id
        self._obj_to_show: PrText = PrTextFactory(self.world.find(target_id))

    @property
    def obj_to_show(self) -> PrText:
        """ PrObj to show """
        return self._obj_to_show

    # build
    def build(self):
        # window
        self.window = QWidget()
        self.window.setMinimumSize(900, 600)
        self.window.setWindowTitle(self.name)
        self.adjust()
        self.window.show()

    def adjust(self):
        # position
        if isinstance(self.position, WnPos):
            if self.position == WnPos.BOTTOM_RIGHT:
                self.window.move(QPoint(*PrHelper.qt.bottom_right(self.window)))
        elif isinstance(self.position, QPoint):
            self.window.move(self.position)
        else:
            self.window.move(QPoint(0, 0))

        # status
        if self.status == WnStatus.MAXIMIZED:
            self.window.showMaximized()
