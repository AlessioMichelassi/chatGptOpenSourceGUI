import os
import openai
import json
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
    isStreamActive = False
    functions = []
    available_functions = {}

    def __init__(self, model, temperature, maxTokens, messages):
        super().__init__()
        self.model = model
        self.initFunctions()
        self.temperature = temperature
        self.maxTokens = maxTokens
        self.messages = messages

    def initFunctions(self):
        self.functions = [
                            {
                                "name": "get_current_weather",
                                "description": "Get the current weather in a given location",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "location": {
                                            "type": "string",
                                            "description": "The city and state, e.g. San Francisco, CA",
                                        },
                                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                                    },
                                    "required": ["location"],
                                },
                            }
                         ]

    def run(self):
        try:
            print(f"thread started: {self.model}")
            answer = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.maxTokens,
                functions= self.functions,
                function_call="auto",
                stream=self.isStreamActive,
            )
            try:
                response_message = answer["choices"][0]["message"]
                print(f"Answer: {answer}")
                # Step 2: check if GPT wanted to call a function
                if response_message.get("function_call"):
                    # Step 3: call the function
                    # Note: the JSON response may not always be valid; be sure to handle errors
                    available_functions = {
                        "get_current_weather": self.getCurrentWeather,
                    }  # only one function in this example, but you can have multiple
                    function_name = response_message["function_call"]["name"]
                    fuction_to_call = available_functions[function_name]
                    function_args = json.loads(response_message["function_call"]["arguments"])
                    function_response = fuction_to_call(
                        location=function_args.get("location"),
                        unit=function_args.get("unit"),
                    )

                    # Step 4: send the info on the function call and function response to GPT
                    self.messages.append(response_message)  # extend conversation with assistant's reply
                    self.messages.append(
                        {
                            "role": "function",
                            "name": function_name,
                            "content": function_response,
                        }
                    )  # extend conversation with function response
                    answer = openai.ChatCompletion.create(
                        model=self.model,
                        messages=self.messages,
                    )  # get a new response from GPT where it can see the function response
                    print(f"2nd Answer: {answer}")
                self.answerReceived.emit(answer)
            except Exception as e:
                self.errorOccurred.emit(str(e))
                self.answerReceived.emit(answer)
                print(f"Answer: {answer}")

        except Exception as e:
            self.errorOccurred.emit(str(e))

    # Example dummy function hard coded to return the same weather
    # In production, this could be your backend API or an external API
    def getCurrentWeather(self, location, unit="celsius"):
        """Get the current weather in a given location"""
        weather_info = {
            "location": location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)


class openAI(QObject):
    models = {"gpt-4", "gpt-4-0613", "gpt-3.5-turbo", "gpt-3.5-turbo-061", "babbage-002", "davinci-002",
              "text-davinci-003", "text-davinci-002", "davinci", "curie", "babbage", "ada"}

    messageHistory = []
    answerReceived = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.messageHistory = []
        self.questionThread = ApiCallThread("gpt-3.5-turbo-0613", 0, 1024, [{"role": "user", "content": "Ciao Chat!"}])
        self.startThread()

    def handleResponse(self, response):
        try:
            answer = response['choices'][0]['message']['content']
            self.messageHistory.append({"role": response['choices'][0]['message']['role'], "content": answer})
            print(self.messageHistory)
            self.answerReceived.emit(answer)
        except Exception as e:
            print(e)
            print(response)

    def startThread(self):
        self.questionThread.answerReceived.connect(self.handleResponse)
        self.questionThread.errorOccurred.connect(self.handleError)
        self.questionThread.start()

    def handleError(self, errorMsg):
        # Qui puoi gestire l'errore come preferisci, ad es. mostrando un messaggio d'errore all'utente
        print("Si è verificato un errore:", errorMsg)

    def getAnswer(self, question, model="gpt-3.5-turbo-0613", temperature=1, maxTokens=1024):
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

