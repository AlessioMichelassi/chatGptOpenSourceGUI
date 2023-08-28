import sys

from PyQt5.QtCore import QAbstractListModel, QMargins, QPoint, QSize, Qt
from PyQt5.QtGui import QColor, QFontMetrics, QPen

# from PyQt5.QtGui import
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QListView,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget, QStyledItemDelegate, QGraphicsDropShadowEffect,
)

BUBBLE_COLORS = {"System": QColor(197, 165, 214, 200), "ChatGpt": QColor(165, 214, 167, 200),
                 "User": QColor(81, 150, 200)}

BUBBLE_PADDING = QMargins(25, 10, 25, 10)
TEXT_PADDING = QMargins(35, 15, 35, 25)


class MessageDelegate(QStyledItemDelegate):
    """
    Draws each message.
    """

    def __init__(self):
        super(MessageDelegate, self).__init__()

        self.thinPen = QPen(QColor(0, 0, 0, 10), 1, Qt.SolidLine)
        self.thickPen = QPen(QColor(0, 0, 0, 20), 2, Qt.SolidLine)

    def paint(self, painter, option, index):
        # Retrieve the user,message tuple from our model.data method.
        user, text = index.model().data(index, Qt.DisplayRole)

        # option.rect contains our item dimensions. We need to pad it a bit
        # to give us space from the edge to draw our shape.

        bubbleRect = option.rect.marginsRemoved(BUBBLE_PADDING)
        txtRect = option.rect.marginsRemoved(TEXT_PADDING)
        # draw the bubble, changing color + arrow position depending on who
        # sent the message. the bubble is a rounded rect, with a triangle in
        # the edge.
        # Crea un'ombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(3, 3)
        shadow.setColor(QColor(0, 0, 0, 80))

        # Dato che non possiamo applicare direttamente l'effetto al widget,
        # dobbiamo simulare l'ombra. Facciamo ciò disegnando un rettangolo
        # trasparente con l'ombra e quindi disegniamo la bolla sopra.

        # Ombra per la bolla
        painter.setBrush(QColor(0, 0, 0, 80))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(bubbleRect.translated(3, 3), 10, 10)  # translate per l'offset dell'ombra

        painter.setPen(Qt.NoPen)
        color = BUBBLE_COLORS[user]
        painter.setBrush(color)
        painter.drawRoundedRect(bubbleRect, 10, 10)

        """# draw the triangle bubble-pointer, starting from

        if "System" in text or "Chat" in text:
            p1 = bubbleRect.topLeft()
        else:
            p1 = bubbleRect.topRight()
        painter.drawPolygon(p1 + QPoint(-30, 0), p1 + QPoint(30, 0), p1 + QPoint(0, 30))
        """
        # draw the text
        painter.setPen(Qt.black)
        full_text = f"{text}"
        painter.drawText(txtRect, Qt.TextWordWrap, full_text)

    def sizeHint(self, option, index):
        _, text = index.model().data(index, Qt.DisplayRole)
        # Calculate the dimensions the text will require.
        metrics = QApplication.fontMetrics()
        rect = option.rect.marginsRemoved(TEXT_PADDING)
        rect = metrics.boundingRect(rect, Qt.TextWordWrap, text)
        rect = rect.marginsAdded(TEXT_PADDING)  # Re add padding for item size.
        return rect.size()


class MessageModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
        self.messages = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Here we pass the delegate the user, message tuple.
            return self.messages[index.row()]

    def rowCount(self, index):
        return len(self.messages)

    def addMessage(self, who, text):
        """
        Add an message to our message list, getting the text from the QLineEdit
        """
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.messages.append((who, text))
            # Trigger refresh.
            self.layoutChanged.emit()
