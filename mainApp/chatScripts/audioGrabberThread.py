import pygame
from PyQt5.QtCore import QThread, pyqtSignal
import speech_recognition as sr
from gtts import gTTS


class AudioGrabberThread(QThread):
    # Definisci un segnale che verrà emesso quando l'acquisizione e la trascrizione sono completate.
    resultSignal = pyqtSignal(str)

    def __init__(self, recognizer, language="it-IT", parent=None):
        super(AudioGrabberThread, self).__init__(parent)
        self.recognizer = recognizer
        self.language = language

    def run(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        try:
            question = self.recognizer.recognize_google(audio, language=self.language)
            self.resultSignal.emit(question)
        except sr.UnknownValueError:
            self.resultSignal.emit("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            self.resultSignal.emit(f"Could not request results from Google Speech Recognition service; {e}")