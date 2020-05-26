from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from .common import log

def bottom_right(widget):
    ag = QDesktopWidget().availableGeometry()
    sg = QDesktopWidget().screenGeometry()
    pos = sg.width() - widget.width(), sg.height() - widget.height() - 32

    log(bottom_right.__name__, f'widget = {widget.size()}')
    log(bottom_right.__name__, f'screen = {ag.size()}')
    log(bottom_right.__name__, f'return = {pos}')

    return pos

if __name__ == '__main__':
    print('[geometry]')
    app = QApplication([])
    widget = QWidget()
    widget.setFixedSize(600, 400)
    widget.move(100, 100)

    widget.pos()

    bottom_right(widget)
