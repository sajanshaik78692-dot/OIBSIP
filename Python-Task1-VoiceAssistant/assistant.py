import datetime
import smtplib
import webbrowser
from email.message import EmailMessage
import pyttsx3
import requests
import speech_recognition as sr

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)


def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"User: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand what you said. Please try again.")
        return ""
    except sr.RequestError:
        speak("Speech service is currently unavailable.")
        return ""


def get_weather(city_name, api_key="YOUR_OPENWEATHERMAP_API_KEY"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5).json()
        if response.get("cod") == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            speak(f"The current temperature in {city_name} is {temp} degrees Celsius with {desc}.")
        else:
            speak("City not found or invalid API key.")
    except Exception:
        speak("Unable to connect to the weather service.")


def send_email(to_email, subject, body):
    # Dummy SMTP configuration for local testing
    sender_email = "test@example.com"
    sender_password = "dummy_password"

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        speak("Email sent successfully.")
    except Exception as e:
        speak("Failed to send email. Please check your SMTP settings.")


def main():
    speak("Voice Assistant activated. How can I help you today?")
    while True:
        command = listen_command()
        if not command:
            continue

        if "hello" in command:
            speak("Hello! How can I assist you?")
        elif "time" in command or "date" in command:
            now = datetime.datetime.now().strftime("%I:%M %p on %B %d, %Y")
            speak(f"The current time and date is {now}.")
        elif "search" in command:
            query = command.replace("search", "").strip()
            speak(f"Searching web for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        elif "weather" in command:
            speak("Which city would you like the weather for?")
            city = listen_command()
            if city:
                get_weather(city)
        elif "stop" in command or "exit" in command or "bye" in command:
            speak("Goodbye!")
            break


if __name__ == "__main__":
    main()