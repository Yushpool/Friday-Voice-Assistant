import time
from operator import truediv
from re import search
import json
import psutil # type: ignore
from datetime import datetime, timedelta

import re
import pyttsx3
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import imdb
import wolframalpha
import pyautogui
import webbrowser

from datetime import datetime

from click import command
from decouple import config
from random import choice

from pyautogui import click
from pyexpat.errors import messages

from conv import random_text
from online import find_my_ip,search_on_google,search_on_wikipedia,youtube,send_email,get_news,weather_forecast

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate',200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


USER = config('USER')
HOSTNAME = config('BOT')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_me():
    hour = datetime.now().hour
    if(hour>=6) and (hour<=12):
        speak(f"Good Morning {USER}")
    elif(hour >= 12) and (hour <= 16 ):
        speak(f"Good Afternoon {USER}")
    elif(hour >= 16) and (hour <= 19):
        speak(f"Good Evening {USER}")
    speak(f"I am {HOSTNAME}. How may I assist you? {USER}")

listening = False

def start_listening():
    global listening
    listening = True
    print("started listening")

def pause_listening():
    global listening
    listening = False
    print("stopped listening")

keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        queri = r.recognize_google(audio,language='en-in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir, take care!")
            else:
                speak("Have a good day sir!")
                exit()

    except Exception:
        speak("Sorry I couldn't understand. can you please repeat that?")
        queri = 'None'
    return queri



def add_todo(task):
    with open('todo.json', 'r+') as f:
        try:
            todos = json.load(f)
        except json.JSONDecodeError:
            todos = []
        todos.append({"task": task, "completed": False})
        f.seek(0)
        json.dump(todos, f)
        f.truncate()
    speak(f"Added task: {task}")

def list_todos():
    with open('todo.json', 'r') as f:
        try:
            todos = json.load(f)
        except json.JSONDecodeError:
            todos = []
    if todos:
        speak("Here are your todos:")
        for i, todo in enumerate(todos, 1):
            status = "completed" if todo["completed"] else "not completed"
            speak(f"{i}. {todo['task']}, {status}")
    else:
        speak("You have no todos.")

def set_timer(minutes):
    end_time = datetime.now() + timedelta(minutes=minutes)
    speak(f"Timer set for {minutes} minutes.")
    while datetime.now() < end_time:
        time.sleep(1)
    speak("Timer finished!")

def get_system_info():
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    speak(f"Memory usage is {memory.percent}%")
    speak(f"CPU usage is {cpu_percent}%")
    speak(f"Disk usage is {disk.percent}%")
    speak("For your convenience I am printing it on screen sir")
    print(f"Memory usage is {memory.percent}%,CPU usage is {cpu_percent}%,Disk usage is {disk.percent}%")


if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I am absolutely fine sir, What about you?")

            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')

            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')

            elif "open camera" in query:
                speak("Opening camera sir")
                sp.run('start microsoft.windows.camera:',shell=True)

            elif "open notepad" in query:
                speak("Opening Notepad for you sir")
                notepad_path = ("C:\\Program Files\\WindowsApps\\Microsoft.WindowsNotepad_11.2412.16.0_x64__8wekyb3d8bbwe\\Notepad\\Notepad.exe")
                os.startfile(notepad_path)

            elif "open Microsoft word" in query:
                speak("Opening Microsoft word for you sir")
                Microsoft_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
                os.startfile(Microsoft_path)


            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(
                    f"your ip address is {ip_address}"
                )
                print(f"your Ip address is {ip_address}")

            elif "open youtube" in query:
                speak("What do you want to play on youtube sir?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"What do you want to search on google {USER}")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak("what do you want to search on wikipedia sir?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia, {results}")
                speak("I am printing in on terminal")
                print(results)

            elif "send an email" in query:
                speak("On what email address do you want to send sir? Please enter in the terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject sir?")
                subject = take_command().capitalize()
                speak("What is the message ?")
                message = take_command().capitalize()
                if send_email(receiver_add,subject,message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("something went wrong Please check the error log")

            elif "give me news" in query:
                speak(f"I am reading out the latest headline of today, sir")
                speak(get_news())
                speak("I am printing it on screen sir")
                print(*get_news(),sep='\n')

            elif "weather" in query:
                ip_address = find_my_ip()
                speak("tell me the name of your city")
                city = input("Enter name of your city")
                speak(f"Getting weather report for your city {city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                speak(f"Also, the weather report talks about {weather}")
                speak("For your convenience, I am printing it on the screen sir.")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name:")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("searching for" + text)
                speak("I found these")
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title}-{year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info["rating"]
                    cast = movie_info["cast"]
                    actor = cast[0:5]
                    plot = movie_info.get('plot outline','plot summary not available')
                    speak(f"{title} was released in {year} has imdb rating of {rating}.It has a cast of {actor}. The "
                          f"plot summary of movie is {plot}")
                    print(f"{title} was released in {year} has imdb rating of {rating}.It has a cast of {actor}. The "
                          f"plot summary of movie is {plot}")

            elif "calculate" in query:
                app_id = "RYJWP8-AJ5R5E4EVX"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(result.results).text
                    speak("The answer is " + ans)
                    print("The answer is " + ans)
                except StopIteration:
                    speak("I couldn't find that. Please try again")

            elif "what is" in query or 'who is' in query or 'which is' in query:
                app_id = "RYJWP8-AJ5R5E4EVX"
                client = wolframalpha.Client(app_id)
                try:
                    ind = query.lower().index('what is') if 'what is' in query.lower() else \
                        query.lower().index('who is') if 'who is' in query.lower() else \
                        query.lower().index('which is') if 'which is' in query.lower() else None

                    if ind is not None:
                        text = query.split()[ind+2:]
                        result = client.query(" ".join(text))
                        ans = next(result.results).text
                        speak("The answer is " + ans)
                        print("The answer is " + ans)
                    else:
                        speak("I could not find that")

                except StopIteration:
                    speak("I couldn't find that. please try again")

            elif "add todo" in query:
                speak("What task would you like to add?")
                task = take_command().lower()
                add_todo(task)

            elif "list todos" in query:
                list_todos()

            elif "set timer" in query:
                speak("How many minutes?")
                command = take_command()

                #Extracting the number using regex
                match = re.search(r'\d+',command)
                if match:
                    minutes = int(match.group(0))
                    set_timer(minutes)
                else:
                    speak("I couldn't understand the time duration. Please try again.")

            elif "system info" in query:
                get_system_info()

        time.sleep(1)


#
# import time
# import pyttsx3
# import speech_recognition as sr
# import keyboard
# import os
# import subprocess as sp
# import re
# from datetime import datetime
# from decouple import config
# from random import choice
# from conv import random_text
# from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast
# import imdb
# import psutil
# from datetime import datetime, timedelta
#
# engine = pyttsx3.init('sapi5')
# engine.setProperty('volume', 1.5)
# engine.setProperty('rate', 200)
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)
#
# USER = config('USER')
# HOSTNAME = config('BOT')
#
# listening = False
#
#
# def speak(text):
#     engine.say(text)
#     engine.runAndWait()
#
#
# def greet_me():
#     hour = datetime.now().hour
#     if hour >= 6 and hour <= 12:
#         speak(f"Good Morning {USER}")
#     elif hour >= 12 and hour <= 16:
#         speak(f"Good Afternoon {USER}")
#     elif hour >= 16 and hour <= 19:
#         speak(f"Good Evening {USER}")
#     speak(f"I am {HOSTNAME}. How may I assist you? {USER}")
#
#
# def start_listening():
#     global listening
#     listening = True
#     print("Started listening")
#
#
# def pause_listening():
#     global listening
#     listening = False
#     print("Stopped listening")
#
#
# keyboard.add_hotkey('ctrl+alt+k', start_listening)
# keyboard.add_hotkey('ctrl+alt+p', pause_listening)
#
#
# def take_command():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening....")
#         r.pause_threshold = 1
#         audio = r.listen(source)
#
#     try:
#         print("Recognizing....")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"User said: {query}")
#
#         # Check if "Friday" is in the query
#         if 'friday' in query.lower():
#             speak(f"Yes, {USER}? How can I assist you?")
#             return query.lower()  # Return the query for further processing
#         else:
#             return 'None'  # Ignore everything else until "Friday" is said
#
#     except Exception:
#         return 'None'
#
#
# def set_timer(minutes, sleep=time.sleep(1)):
#     end_time = datetime.now() + timedelta(minutes=minutes)
#     speak(f"Timer set for {minutes} minutes.")
#     while datetime.now() < end_time:
#         sleep
#     speak("Timer finished!")
#
# def get_system_info():
#     cpu_percent = psutil.cpu_percent()
#     memory = psutil.virtual_memory()
#     disk = psutil.disk_usage('/')
#     speak(f"Memory usage is {memory.percent}%")
#     speak(f"CPU usage is {cpu_percent}%")
#     speak(f"Disk usage is {disk.percent}%")
#     speak("For your convenience I am printing it on screen sir")
#     print(f"Memory usage is {memory.percent}%,CPU usage is {cpu_percent}%,Disk usage is {disk.percent}%")
#
#
#
#
#
# if __name__ == '__main__':
#     greet_me()
#     while True:
#         if listening:
#             query = take_command()
#
#             # Process only if "Friday" is mentioned
#             if 'friday' in query:
#                 if "how are you" in query:
#                     speak("I am absolutely fine sir, What about you?")
#
#                 elif "open command prompt" in query:
#                     speak("Opening command prompt")
#                     os.system('start cmd')
#
#                 elif "open camera" in query:
#                     speak("Opening camera sir")
#                     sp.run('start microsoft.windows.camera:', shell=True)
#
#                 elif "open notepad" in query:
#                     speak("Opening Notepad for you sir")
#                     notepad_path = (
#                         "C:\\Program Files\\WindowsApps\\Microsoft.WindowsNotepad_11.2410.21.0_x64__8wekyb3d8bbwe\\Notepad\\Notepad.exe")
#                     os.startfile(notepad_path)
#
#                 elif "open microsoft word" in query:
#                     speak("Opening Microsoft Word for you sir")
#                     microsoft_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
#                     os.startfile(microsoft_path)
#
#                 elif "ip address" in query:
#                     ip_address = find_my_ip()
#                     speak(f"Your IP address is {ip_address}")
#                     print(f"Your IP address is {ip_address}")
#
#                 elif "open youtube" in query:
#                     speak("What do you want to play on YouTube, sir?")
#                     video = take_command().lower()
#                     youtube(video)
#
#                 elif "open google" in query:
#                     speak(f"What do you want to search on Google, {USER}?")
#                     search_query = take_command().lower()
#                     search_on_google(search_query)
#
#                 elif "wikipedia" in query:
#                     speak("What do you want to search on Wikipedia, sir?")
#                     search_term = take_command().lower()
#                     results = search_on_wikipedia(search_term)
#                     speak(f"According to Wikipedia, {results}")
#                     print(results)
#
#                 elif "send an email" in query:
#                     speak("On what email address do you want to send, sir? Please enter in the terminal.")
#                     receiver_add = input("Email address:")
#                     speak("What should be the subject, sir?")
#                     subject = take_command().capitalize()
#                     speak("What is the message?")
#                     message = take_command().capitalize()
#                     if send_email(receiver_add, subject, message):
#                         speak("I have sent the email, sir.")
#                     else:
#                         speak("Something went wrong. Please check the error log.")
#
#                 elif "give me news" in query:
#                     speak("Here are the latest headlines for today, sir.")
#                     speak(get_news())
#                     print(*get_news(), sep='\n')
#
#                 elif "weather" in query:
#                     speak("Tell me the name of your city.")
#                     city = input("Enter the name of your city: ")
#                     speak(f"Getting the weather report for {city}.")
#                     weather, temp, feels_like = weather_forecast(city)
#                     speak(
#                         f"The current temperature is {temp}, but it feels like {feels_like}. The weather is {weather}.")
#                     print(f"Weather: {weather}, Temperature: {temp}, Feels like: {feels_like}")
#
#                 elif "movie" in query:
#                     movies_db = imdb.IMDb()
#                     speak("Please tell me the movie name.")
#                     movie_name = take_command()
#                     movies = movies_db.search_movie(movie_name)
#                     speak(f"Searching for {movie_name}. I found these movies:")
#                     for movie in movies:
#                         title = movie["title"]
#                         year = movie["year"]
#                         speak(f"{title} - {year}")
#
#                 # elif "add todo" in query:
#                 #     speak("What task would you like to add?")
#                 #     task = take_command().lower()
#                 #     add_todo(task)
#                 #
#                 # elif "list todos" in query:
#                 #     list_todos()
#
#                 elif "set timer" in query:
#                     speak("How many minutes?")
#
#                     time_input = take_command()
#                     match = re.search(r'\d+', time_input)
#                     if match:
#                         minutes = int(match.group(0))
#                         set_timer(minutes)
#                     else:
#                         speak("I couldn't understand the time duration. Please try again.")
#
#                 elif "system info" in query:
#                     get_system_info()
#
#         time.sleep(1)