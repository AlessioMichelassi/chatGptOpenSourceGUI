import os
import openai
from PyQt5.QtCore import QObject, pyqtSignal, QThread

from mainApp.AI import secretKeys

openai.api_key = secretKeys.openAi
if not openai.api_key:
    raise ValueError("Nessuna chiave API di OpenAI trovata nell'ambiente.")

"""
https://open-meteo.com/en/docs
"""

class ApiCallThread(QThread):
    answerReceived = pyqtSignal(object)
    errorOccurred = pyqtSignal(str)

    def __init__(self, model, temperature, maxTokens, messages):
        super().__init__()
        self.model = model
        self.temperature = temperature
        self.maxTokens = maxTokens
        self.messages = messages

    def run(self):
        try:
            print(f"thread started: {self.model}")
            answer = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.maxTokens,
            )
            self.answerReceived.emit(answer)
            print(f"Answer: {answer}")
        except Exception as e:
            self.errorOccurred.emit(str(e))


class openAI(QObject):
    models = {"gpt-4", "gpt-4-0613", "gpt-3.5-turbo", "gpt-3.5-turbo-061", "babbage-002", "davinci-002",
              "text-davinci-003", "text-davinci-002", "davinci", "curie", "babbage", "ada"}

    messageHistory = []

    answerReceived = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.messageHistory = []
        self.questionThread = ApiCallThread("gpt-3.5-turbo", 0, 1024, [{"role": "user", "content": "Ciao Chat!"}])
        self.startThread()

    def handleResponse(self, response):
        answer = response['choices'][0]['message']['content']
        self.messageHistory.append({"role": response['choices'][0]['message']['role'], "content": answer})
        print(self.messageHistory)
        self.answerReceived.emit(answer)

    def startThread(self):
        self.questionThread.answerReceived.connect(self.handleResponse)
        self.questionThread.errorOccurred.connect(self.handleError)
        self.questionThread.start()

    def handleError(self, errorMsg):
        # Qui puoi gestire l'errore come preferisci, ad es. mostrando un messaggio d'errore all'utente
        print("Si è verificato un errore:", errorMsg)

    def getAnswer(self, question, model="gpt-3.5-turbo", temperature=0, maxTokens=1024):
        print(f"Question: {question}")
        messages = [
            {"role": "user", "content": f"{question}"},
        ]
        self.questionThread = ApiCallThread(model, temperature, maxTokens, messages)
        self.startThread()

    def pythonBugFixer(self, question, model="gpt-3.5-turbo", temperature=0, maxTokens=1024):
        messages = [
            {"role": "system", "content": "You will be provided with a piece of Python code, "
                                          "and your task is to find and fix bugs in it."},
            {"role": "user", "content": f"{question}"},
        ]
        self.questionThread = ApiCallThread(model, temperature, maxTokens, messages)
        self.startThread()

    def codeEfficiencyImprovement(self, question, model="gpt-4", temperature=0, maxTokens=1024):
        messages = [
            {"role": "system", "content": "You will be provided with a piece of Python code, "
                                          "and your task is to provide ideas for efficiency improvements."},
            {"role": "user", "content": f"{question}"},
        ]
        self.questionThread = ApiCallThread(model, temperature, maxTokens, messages)
        self.startThread()

    def codeExplainer(self, question, model="gpt-3.5-turbo", temperature=0, maxTokens=1024):
        messages = [
            {"role": "system", "content": "You will be provided with a piece of code, and your task is to explain it "
                                          "in a concise way."},
            {"role": "user", "content": f"{question}"},
        ]
        self.questionThread = ApiCallThread(model, temperature, maxTokens, messages)
        self.startThread()



