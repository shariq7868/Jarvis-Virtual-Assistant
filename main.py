import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import websites
import requests 
from google import genai
 
recogniser = sr.Recognizer() 
engine = pyttsx3.init()
newsapi = "8a908052d68e4e97870092fe628aaf10"
geminiapi = "AIzaSyA6i4ls4R7OFlb9RTkXB9ROlcX7HyM2mI0"

def speak(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) # 0 index for male and 1,2 for female
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if c.lower().startswith("open"):
        web = c.lower().split(" ")[1]
        link = websites.website[web]
        webbrowser.open(link)
    elif c.lower().startswith("play"):
        song = c.replace("play", "").strip().lower()
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        data = r.json()
        articles = data.get("articles",[])
        for article in articles:
            print(article["title"])
            speak(article["title"])
    else:
        client = genai.Client(api_key=f"{geminiapi}")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=c,
        )

        print(response.text)
        speak(response.text)


if(__name__=="__main__"):
    speak("Initialising jarvis....")
    while True:
        r = sr.Recognizer()

        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source,timeout=4,phrase_time_limit=4)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("yes")

                with sr.Microphone() as source:
                    print("jarvis Active....")
                    audio = r.listen(source)
                command = r.recognize_google(audio)
                print(command)
                if command.lower() == "exit":
                    speak("Goodbye!")
                    break
                processCommand(command)
                    
        except Exception as e:
            print("Error;",e)