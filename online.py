import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

EMAIL = ""
PASSWORD = ""


def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def search_on_google(query):
    kit.search(query)

def youtube(video):
    kit.playonyt(video)

def send_email(receiver_add,subject,message):
    try:

        email = EmailMessage()
        email['To'] = receiver_add
        email['Subject'] = subject
        email['From'] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login(EMAIL,PASSWORD)
        s.send_message(email)
        s.close()
        return True

    except Exception as e:
        print(e)
        return False


def get_news():
    news_headline = []
    result = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey=407a15a2de9a4d1a935a2126f40ae21f").json()
    articles = result["articles"]
    for article in articles:
        news_headline.append(article["title"])
        return news_headline[:6]

def weather_forecast(city):
    res = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=454fc1a5e211d1d38b3f7c5b40b69b3d"
    ).json()
    weather = res["weather"][0]["main"]
    temp = res["main"]["temp"] - 273.15
    feels_like = res["main"]["feels_like"] - 273.15
    return weather,f"{temp:.2f}\u00B0C",f"{feels_like:.2f}\u00B0C"




