from PyQt5.QtGui import QTextCursor, QFont, QKeyEvent
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QVBoxLayout


class QConsole(QPlainTextEdit):
    """
    Qt based console
    """
    def __init__(self,):
        super().__init__()

        self.setFont(QFont('consolas', 12))
        self.setStyleSheet("background-color: black; color: white;")
        self.setMaximumBlockCount(32)

        self.setPlainText(">>>")
        self.moveCursor(QTextCursor.End)

    def append(self, text: str):
        self.appendPlainText(f'{str}\n')

    def keyPressEvent(self, event: QKeyEvent):
        if event.type() == QKeyEvent.KeyPress:
            if event.key() == Qt.Key_Up:
                return
            if event.key() == Qt.Key_Backspace:
                cursor: QTextCursor = self.textCursor()
                if cursor.positionInBlock() <= 3:
                    return
            if event.key() == Qt.Key_Return:
                cursor: QTextCursor = self.textCursor()
                self.on_return_pressed(cursor.block())
        super().keyPressEvent(event)

    def on_return_pressed(self, block):
        print(block.text())
            

if __name__ == '__main__':
    from PyQt5.QtWidgets import QWidget

    # app
    app = QApplication([])

    # console
    console = QConsole()

    # layout
    layout = QVBoxLayout()
    layout.addWidget(console)
    
    window = QWidget()
    window.setMinimumSize(500, 300)
    window.setLayout(layout)
    
    window.show()

    exit(app.exec_())

