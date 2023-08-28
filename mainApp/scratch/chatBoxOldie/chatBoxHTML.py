from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from mainApp.widgets.tools.superTxtEditorAnswer import superTxtEditor


class ChatBox(QWidget):
    questionBox: superTxtEditor
    chatBox: QTextEdit
    btnSend: QPushButton
    btnListen: QPushButton

    """
        Generally i use to divide the initUI() method in 3 o more parts to make code cleaner and more readable.
        ini initUI() method i use to define the main widgets. In initLayout() method i use to define the layout of the 
        main widgets. if the layout widget became to much complex i use to define a new method to define the layout like:
        initOtherStuffLayout() and i return the layout in the initLayout() method so i can add it to the main layout.
        In initStyle() method i use to define the styleSheet of the widgets. In initConnections() method i use to define
        all the connections between the widgets. Optionally if i have some geometry constrain like one part need to be 3 times
        another one i use to define a initGeometry() method. 
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.initLayout()
        self.initStyle()
        self.initGeometry()
        self.initConnections()

    def initUI(self):
        self.chatBox = QTextEdit()
        self.questionBox = superTxtEditor()
        self.btnSend = QPushButton("Send")
        self.btnListen = QPushButton("Listen")

    def initLayout(self):
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.chatBox)
        mainLayout.addWidget(self.questionBox)
        btnLayout = self.btnLayout()
        mainLayout.addLayout(btnLayout)
        self.setLayout(mainLayout)

    def btnLayout(self):
        btnLayout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        btnLayout.addItem(spacer)
        btnLayout.addWidget(self.btnSend)
        btnLayout.addWidget(self.btnListen)
        return btnLayout

    def initStyle(self):
        pass

    def initGeometry(self):
        self.questionBox.setFixedHeight(100)
        self.chatBox.setMinimumHeight(self.questionBox.height() * 2)

    def initConnections(self):
        self.questionBox.returnPressed.connect(self.addQuestion)

    def addQuestion(self, message):
        self.addMessage("You", message, "lightblue")

    def addAnswerFromChatBot(self, message):
        self.addMessage("ChatBot", message, "lightgreen")

    def addAnswerFromSystem(self, message):
        self.addMessage("System", message, "lightyellow")

    def addMessage(self, name, message, bg_color):
        html_msg = f"""<div style="margin: 4px; padding: 5px; background-color: {bg_color}; border-radius: 10px;">"""
        html_msg += f"""<b>{name}:</b> {message}</div>"""
        # Aggiunge uno spazio vuoto (trasparente) tra i messaggi
        html_msg += """<div style="height: 10px;"></div>"""
        self.chatBox.moveCursor(QTextCursor.End)
        self.chatBox.insertHtml(html_msg)


# this is for test the widget
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ChatBox()
    w.show()
    sys.exit(app.exec_())
