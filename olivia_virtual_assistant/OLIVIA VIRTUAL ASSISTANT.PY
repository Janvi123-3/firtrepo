import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import webbrowser
import os
import pyowm
import requests
import json
import wolframalpha
import re
import pywhatkit
import cv2
import time
import pyscreenshot
import ctypes
import pyjokes
import random
from AppOpener import open
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer,QTime,QDate
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from GUI import Ui_Olivia


text = "Welcome"

hour = int(datetime.datetime.now().hour)
min = int(datetime.datetime.now().minute + 2)

#Setting up voice engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 175)

def speak(audio):
    if 'lbl' in globals():
        lbl.setText(audio.title())
    engine.say(audio)
    engine.runAndWait()


def greetme():
    global text
    gout = ['whats up', 'hello', 'hey there', 'hey', 'gracias', 'ola']
    greet = random.choice(gout) + " boss "
    if hour >= 0 and hour < 12:
        speak(greet + "Good Morning.")
        text = (greet + "Good Morning.")
        lbl.setText(text.title())

    elif hour >= 12 and hour < 18:
        speak(greet + "Good Afternoon.")
        text = (greet + "Good Afternoon.")
        lbl.setText(text.title())

    else:
        speak(greet + "Good Evening.")
        text = (greet + "Good Evening.")
        lbl.setText(text.title())

speak("Initializing System")


class MainThread(QThread):

    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.execute()

    def command(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            text = "Listening..."
            lbl.setText(text.title())
            r.adjust_for_ambient_noise(source,duration= 1)
            audio = r.listen(source)

        try :
            text = "Recognizing..."
            lbl.setText(text.title())
            self.quest = r.recognize_google(audio, language = 'en-in')
            lbl.setText(self.quest.title())

        except Exception as e:
            text = "Pardon me please..."
            lbl.setText(text.title())
            self.quest = "None"

        return self.quest

    def execute(self):

        greetme()
        while True:
            self.quest = self.command().lower()
            if 'who are you' in self.quest:
                speak("I am Olivia version 1 point 0. An AI Assistant at your service. V I A in my name stands for Virtual Inteligent Assistant respectively. I am programmed to perform various tasks and activies.")

            elif 'are you there' in self.quest:
                speak("At your service boss...")

            elif 'who made you' in self.quest:
                speak("Prakashdeep and Janvi build me as an AI assistant.")

            elif 'capability' in self.quest or 'you can do' in self.quest or 'features' in self.quest:
                speak("I am a feature packed assistant. I can perform various tasks like...")
                speak("weather updates. Opening webpages like, wikipedia, youtube, gmail. Opening webrowser. Searching on internet, Finding places on google maps. latest news. tell you jokes. Tell you anything related to, science, technologies, history, maths, politics, daily life. And many more.")
                speak("Just command me")

            elif 'weather update' in self.quest or 'current weather' in self.quest or 'weather outside' in self.quest:
                token = "73c5b171f87d48af9f672bb217e8d448"
                own = pyowm.OWM(token).weather_manager()
                pin = "282001"
                weather = own.weather_at_zip_code(pin, 'IN').weather
                temp = int(round(weather.temperature(unit='fahrenheit')['temp'], 2))
                temp = (temp - 32)/1.8
                temp = round(temp, 2)
                speak(f"Tempreature is {temp} degree celcious.")

            elif 'search wikipedia' in self.quest:
                webbrowser.open_new_tab("https://www.wikipedia.org/")
                speak("Wikipedia homepage found...")

            elif 'wikipedia' in self.quest:
                speak("Searching on wikipedia...")
                self.quest = self.quest.replace("wikipedia", "")
                results = wikipedia.summary(self.quest, sentences = 3)
                speak("According to wikipedia")
                speak(results)

            elif 'open browser' in self.quest:
                webbrowser.open_new_tab("https://duckduckgo.com/")
                speak("Web browser is open now, search whatever you want to.")

            elif 'open youtube' in self.quest:
                webbrowser.open_new_tab("https://www.youtube.com/")
                speak("Youtube homepage is here, entertainment at your ease.")

            elif 'open gmail' in self.quest:
                webbrowser.open_new_tab("https://mail.google.com")
                speak("your inbox is now open.")

            elif 'search' in self.quest:
                self.quest = self.quest.replace("search", "")
                webbrowser.open_new_tab(self.quest)
                speak("Searching...")

            elif 'open google maps' in self.quest or 'google maps' in self.quest or 'find on google map' in self.quest or 'find something near me' in self.quest or 'locate' in self.quest:
                speak("what do you want to find in google maps ?")
                find = self.command()
                speak(f"locating {find} please wait...")
                url = f"https://www.google.com/maps/search/{find}"
                webbrowser.open_new_tab(url)
                speak(f"{find} located...")

            elif 'latest news' in self.quest or 'news' in self.quest or 'current news' in self.quest or  'going on in the world' in self.quest:
                url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=d6d5f76c91da4f71ae13c9c1a8df4665'
                news = requests.get(url).text
                ndict = json.loads(news)
                articles = ndict['articles']
                speak("Today's headlines are...")
                for index, articles in enumerate(articles):
                    speak(articles['title'])
                    if index == len(articles) - 1:
                        break
                speak("That's all for now!")

            elif 'joke' in self.quest:
                joke = pyjokes.get_joke()
                speak(joke)

            elif 'tell me' in self.quest:
                try:
                    x = re.findall(".*tell me *", self.quest)
                    self.quest = self.quest.replace(x[0], "")
                    lbl.setText(self.quest)
                    app_id = "Y5JJXH-GRLR65EWU5"
                    client = wolframalpha.Client(app_id)
                    result = client.query(self.quest)
                    ans = next(result.results).text
                    y = re.findall("[0-9]...verb...|[0-9]...noun...|verb...|noun...", ans)
                    for qy in y:
                        if qy in ans:
                            ans = ans.replace(qy, "")
                    speak(ans)

                except:
                    speak("Pardon me")

            elif 'my picture' in self.quest or 'pic' in self.quest or 'photo' in self.quest or 'selfie' in self.quest:
                try:
                    title = datetime.datetime.now()
                    camera = cv2.VideoCapture(0)
                    res, img = camera.read()
                    cv2.imshow("Image", img)
                    cv2.imwrite(f"C:\\Users\\rog\\OneDrive\\Pictures\\{title.second, title.minute, title.hour, title.day}_photo.png", img)
                    speak("Picture saved!")
                    camera.release()
                    cv2.destroyAllWindows()
                except Exception as e:
                    speak("something went wrong!")

            elif 'screenshot' in self.quest or 'capture screen' in self.quest:
                try:
                    img = pyscreenshot.grab()
                    img.show()
                    a = datetime.datetime.now()
                    img.save(f"C:\\Users\\rog\\OneDrive\\Pictures\\{title.second, title.minute, title.hour, title.day}_screenshot.png", img)
                    speak("screenshot saved")
                except Exception as e:
                    speak("something went wrong!")

            elif 'lock' in self.quest:
                ctypes.windll.user32.LockWorkStation()

            elif 'current time' in self.quest:
                t = datetime.datetime.now().strftime("%H: %M: %S")
                speak(f"Sir, the time is {t}")

            elif 'how are you' in self.quest:
                speak("I am fine, Thank you")
                speak("How are you, Boss")

            elif 'fine' in self.quest or "good" in self.quest:
                speak("It's good to know that your fine.")

            elif 'sad' in self.quest or 'not feeling well' in self.quest:
                speak("Oh! should i tell you a joke ?")
                inp = self.command()
                if inp == "yes":
                    speak(pyjokes.get_joke())
                elif inp == "no":
                    speak("what can i do for you sir ?")

            elif "who i am" in self.quest:
                speak("If you talk and giving me commands then definitely your a human.")

            elif "why you came to world" in self.quest:
                speak("It's a secret, shhhhhh.")

            elif 'what is love' in self.quest:
                speak("It is 7th sense that destroy all other senses")

            elif 'reason of your creation' in self.quest:
                speak("I was created as a Major project by Janvi and Prakashdeep")

            elif "what's your name" in self.quest or "What is your name" in self.quest:
                speak("My friends call me Olivia.")

            elif "remember" in self.quest:
                os.system("dir")
                file = os.open("olivia.txt", 'w')
                speak("What should i remember boss ?")
                cont = self.command()
                file.write(cont)
                speak("Done boss");

            elif 'open notes' in self.quest:
                speak("showing notes.")
                file = os.open('olivia.txt', 'r')
                speak(file.read())

            elif 'chrome' in self.quest:
                open('Google Chrome')
                speak("Opening google chrome")

            elif 'notepad' in self.quest:
                os.system('Notepad')
                speak("opening Notepad")

            elif 'word' in self.quest:
                open('word')
                speak("opening M S word")

            elif 'excel' in self.quest:
                open('Excel')
                speak("opening M S excel")

            elif 'powerpoint' in self.quest:
                open('PowerPoint')
                speak("opening M S Powerpoint")

            elif 'sleep now' in self.quest or 'go to sleep' in self.quest:
                speak("I'm just a command away boss. Wake me when you need.")
                wakeword = ["hey Olivia", "hi Olivia", "Olivia", "wake up", "are you there"]
                wake = ""
                while True:
                    a = sr.Recognizer()
                    with sr.Microphone() as source:
                        a.pause_threshold = 1
                        audio = a.listen(source)
                    try:
                        wake = a.recognize_google(audio, language = 'en-in')
                    except:
                        speak("")
                    for word in wakeword:
                        if word in wake:
                            greetme()
                            return False

            elif  'exit' in self.quest or 'close' in self.quest or 'shutdown' in self.quest:
                speak("good bye boss.")
                QCoreApplication.exit()

execution = MainThread()

class Mywindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Olivia()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.ui.movie = QtGui.QMovie("circle.gif")
        self.ui.gif.setMovie(self.ui.movie)
        self.ui.text.setText(text)
        self.ui.movie.start()
        execution.start()

app = QApplication(sys.argv)
olivia = Mywindow()
lbl = olivia.findChild(QLabel, "text")
olivia.show()
app.exec_()
