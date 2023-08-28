import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtGui import QTextCursor, QFont, QColor, QTextBlockFormat, QTextCharFormat


class ChatBox(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.chatBox = QTextEdit()
        self.chatBox.setAcceptRichText(True)
        self.chatBox.setReadOnly(True)
        self.layout.addWidget(self.chatBox)

        self.userButton = QPushButton("Aggiungi Messaggio dell'Utente")
        self.userButton.clicked.connect(self.addQuestion)
        self.layout.addWidget(self.userButton)

        self.chatbotButton = QPushButton("Aggiungi Messaggio del ChatBot")
        self.chatbotButton.clicked.connect(self.addAnswerFromChatBot)
        self.layout.addWidget(self.chatbotButton)

        self.systemButton = QPushButton("Aggiungi Messaggio di Sistema")
        self.systemButton.clicked.connect(self.addAnswerFromSystem)
        self.layout.addWidget(self.systemButton)

        self.setLayout(self.layout)

    def addQuestion(self):
        self.addMessage("You", "Questo è un messaggio dell'utente", QColor(0, 255, 255))

    def addAnswerFromChatBot(self):
        self.addMessage("ChatBot", "Questo è un messaggio del ChatBot", QColor(255, 0, 0))

    def addAnswerFromSystem(self):
        self.addMessage("System", "Questo è un messaggio di sistema", QColor(255, 255, 0))

    def addMessage(self, name, message, color):
        cursor = self.chatBox.textCursor()  # Ottieni il cursore del testo corrente
        cursor.movePosition(QTextCursor.End)  # Vai alla fine del documento
        # Imposta il colore di sfondo e altri stili
        text_format = QTextBlockFormat()
        text_format.setBackground(QColor(color))
        text_format.setBottomMargin(5)  # Spazio tra messaggi
        cursor.insertBlock(text_format)

        # Aggiungi il nome
        char_format = QTextCharFormat()
        char_format.setFontWeight(QFont.Bold)
        cursor.insertText(f"{name}: ", char_format)

        # Aggiungi il messaggio
        cursor.insertText(message)

        self.chatBox.setTextCursor(cursor)


app = QApplication(sys.argv)
window = ChatWidget()
window.show()
sys.exit(app.exec_())
