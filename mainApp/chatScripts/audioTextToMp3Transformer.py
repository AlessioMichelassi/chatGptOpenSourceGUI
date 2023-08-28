import pygame
from PyQt5.QtCore import QThread, pyqtSignal
from gtts import gTTS


class AudioTextToMp3Transformer(QThread):

    fileDone = pyqtSignal(str)

    def __init__(self, text, index, language="it-IT", tld = 'us', parent=None):
        super(AudioTextToMp3Transformer, self).__init__(parent)
        pygame.mixer.init()
        self.text = text
        self.index = index
        self.language = language
        self.tld = tld

    def run(self):
        tts = gTTS(text=self.text, lang=self.language, slow=False, tld=self.tld, lang_check=True)
        filename = f"mainApp/tempFolder/audio{self.index}.mp3"
        tts.save(filename)
        self.fileDone.emit(filename)