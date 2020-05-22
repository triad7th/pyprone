from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget

def bottom_right(widget):
    ag = QDesktopWidget().availableGeometry()
    #sg = QDesktopWidget().screenGeometry()
    pos = ag.width() - widget.width(), ag.height() - widget.height()

    print(f'widget = {widget.size()}')
    print(f'screen = {ag.size()}')
    print(f'return = {pos}')

    return pos

if __name__ == '__main__':
    print('[geometry]')
    app = QApplication([])
    widget = QWidget()
    widget.setFixedSize(600, 400)
    widget.move(100, 100)

    widget.pos()

    bottom_right(widget)
