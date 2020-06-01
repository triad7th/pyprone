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
        self.setMaximumBlockCount(30)

    def append(self, text: str):
        pass

    def back(self):
        pass

    def keyPressEvent(self, event: QKeyEvent):
        if event.type() == QKeyEvent.KeyPress:
            if event.key() == Qt.Key_Up:
                return
            if event.key() == Qt.Key_Backspace:
                cursor: QTextCursor = self.textCursor()
                self.on_backspace_pressed(cursor)
                return
            if event.key() == Qt.Key_Return:
                cursor: QTextCursor = self.textCursor()
                self.on_return_pressed(cursor)
                return

        #super().keyPressEvent(event)
        self.on_text_pressed(event.text())        

    def on_text_pressed(self, text):
        self.append(text)

    def on_backspace_pressed(self, cursor):
        self.back()

    def on_return_pressed(self, cursor):
        self.append('\n>>>')

if __name__ == '__main__':
    from PyQt5.QtCore import QTimer
    from PyQt5.QtWidgets import QWidget
    import subprocess as sp    

    # app
    app = QApplication([])

    # console
    console = QConsole()
    g_text = "Hello Console!\n>>>"
    g_cursor_str = ">>>"

    # layout
    layout = QVBoxLayout()
    layout.addWidget(console)
    
    window = QWidget()
    window.setMinimumSize(500, 300)
    window.setLayout(layout)
    
    window.show()
    
    # callback func
    def append(text: str):
        sp.call('cls', shell=True)
        global g_text
        g_text += f'{text}'
        print(g_text)
        
    def back():
        sp.call('cls', shell=True)
        global g_text, g_cursor_str        
        if not g_text[len(g_text)-4:len(g_text)] == f'\n{g_cursor_str}':
            if len(g_text) > len(g_cursor_str):
                g_text = g_text[0:len(g_text)-1]
        print(g_text)

    def update():
        global console, g_text
        console.setPlainText(g_text)
        console.moveCursor(QTextCursor.End)

    # alter object
    console.append = append
    console.back = back

    # timer
    timer = QTimer()    
    timer.timeout.connect(update)
    timer.start(200)

    exit(app.exec_())
