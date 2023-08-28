"""
This is an override of a standard QTextEditor that enable some special features:

    - send message on enter pressed (it emit a signal with the text of the message inside and clear the box)
    - return carriage on shift+enter pressed

"""

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeyEvent, QTextCursor
from PyQt5.QtWidgets import QTextEdit


class superTxtEditor(QTextEdit):
    returnPressed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        # controlla se è stato premuto invio
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            # emetti il segnale
            self.returnPressed.emit(self.toPlainText())
            self.clear()
            self.moveCursor(QTextCursor.Start)
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and event.modifiers() == Qt.ShiftModifier:
            self.insertPlainText("\n")
        else:
            super().keyPressEvent(event)