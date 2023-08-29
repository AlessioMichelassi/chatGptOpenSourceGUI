from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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
    fgColor = QColor(200, 200, 200)
    systemColorBg = QColor(255, 150, 10)
    userColorBg = QColor(102, 178, 255)
    chatColorBg = QColor(70, 200, 10)

    questionComing = pyqtSignal(str, name="question coming")
    isListenEnabled = pyqtSignal(bool, name="is listen enabled")
    grabAudioFromMic = pyqtSignal(name="grab audio from mic")

    """
    ITA:
        Questa classe è il widget che contiene la chat grafica. i pulsanti,
        emettono segnali che possono essere catturati dal mainWidget.
        Se si scrive qualcosa nella questionBox e si preme invio, viene emesso
        il segnale questionComing che contiene la domanda scritta nella questionBox così
        come se viene premuto invio.
        
        Se la questionBox è vuota e si preme il pulsante send, viene emesso il segnale
        grabAudioFromMic che dice al mainWidget di catturare l'audio dal microfono.
        
        Se si preme il pulsante listen, viene emesso il segnale isListenEnabled che dice
        al mainWidget di abilitare o disabilitare la funzione di ascolto del messaggio ricevuto.
        
    ENG:
        This class is the widget that contains the graphic chat. the buttons,
        emit signals that can be captured by the mainWidget.
        If you write something in the questionBox and press enter, the signal is emitted
        questionComing that contains the question written in the questionBox as well
        as if you press enter.
        
        If the questionBox is empty and you press the send button, the signal is emitted
        grabAudioFromMic that tells the mainWidget to capture the audio from the microphone.
        
        If you press the listen button, the signal is emitted isListenEnabled that says
        to the mainWidget to enable or disable the function of listening to the received message.
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
        btnLayout.addWidget(self.btnListen)
        btnLayout.addItem(spacer)
        btnLayout.addWidget(self.btnSend)
        return btnLayout

    def initStyle(self):
        self.chatBox.setReadOnly(True)
        self.btnListen.setCheckable(True)

    def initGeometry(self):
        self.questionBox.setFixedHeight(100)
        self.chatBox.setMinimumHeight(self.questionBox.height() * 2)

    def initConnections(self):
        self.questionBox.returnPressed.connect(self.addQuestion)
        self.btnSend.clicked.connect(self.getQuestionFromQuestionBox)
        self.btnListen.toggled.connect(self.listen)

    def addQuestion(self, question):
        self.addMessage("You", question, self.userColorBg)
        self.questionBox.clear()
        self.questionComing.emit(question)

    def addAnswerFromChatBot(self, answer):
        self.addMessage("ChatBot", answer, self.chatColorBg)

    def addAnswerFromSystem(self, info):
        self.addMessage("System", info, self.systemColorBg)

    def addMessage(self, name, message, color):
        cursor = self.chatBox.textCursor()  # Ottieni il cursore del testo corrente
        cursor.movePosition(QTextCursor.End)  # Vai alla fine del documento

        self._insertName(cursor, name, color)
        self._insertMessage(cursor, message, color)

        self.chatBox.setTextCursor(cursor)

    def _insertName(self, cursor, name, color):
        text_format = QTextBlockFormat()
        text_format.setAlignment(Qt.AlignLeft)
        text_format.setBackground(Qt.GlobalColor.transparent)
        cursor.insertBlock(text_format)

        char_format = QTextCharFormat()
        char_format.setFontWeight(QFont.Bold)
        color.setAlpha(255)
        char_format.setForeground(color)
        cursor.insertText(f"{name}:\n", char_format)

    def _insertMessage(self, cursor, message, color):
        text_format = QTextBlockFormat()
        color.setAlpha(10)
        text_format.setBackground(color)
        text_format.setBottomMargin(0)
        text_format.setLineHeight(100, QTextBlockFormat.SingleHeight)
        text_format.setAlignment(Qt.AlignJustify)
        cursor.insertBlock(text_format)

        char_format = QTextCharFormat()
        char_format.setFontWeight(QFont.Normal)
        char_format.setForeground(self.fgColor)
        if message:
            sentences = message.split("\n")
            for sent in sentences:
                cursor.insertText(f"\n\t{sent}\n", char_format)
            cursor.insertText(f"\n", char_format)

    def getQuestionFromQuestionBox(self):
        question = self.questionBox.toPlainText()
        if question:
            self.addQuestion(question)
            self.questionBox.clear()
        else:
            self.grabAudioFromMic.emit()

    def listen(self, isListen):
        self.isListenEnabled = isListen
        if isListen:
            self.btnListen.setText("Stop")
            self.isListenEnabled.emit(True)
        else:
            self.btnListen.setText("Listen")
            self.isListenEnabled.emit(False)
        self.btnListen.update()

# this is for test the widget
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ChatBox()
    w.show()
    sys.exit(app.exec_())
