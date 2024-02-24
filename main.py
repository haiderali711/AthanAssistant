import time
import pyttsx3
import requests
import speech_recognition as sr
from datetime import datetime
import subprocess
import os
os.environ['PATH'] += os.pathsep + '/usr/local/bin/'


dailyTimings = []
prayers = ["Fajar", "Dhuhr", "Asar", "Maghrib", "Isha"]


def fetchTimes():
    f = open('locationData.txt', 'r')
    city = f.readline().strip('\n')
    country = f.readline().strip('\n')
    method = f.readline().strip('\n')
    api_link = 'http://api.aladhan.com/v1/timingsByCity?city=' + city + '&country=' + country + '&method=' + method

    print(f'City : {city}')
    print(f'Country: {country}')
    print(f'Method : {method}')
    print(f'Api Link : {api_link}')

    response = requests.get(api_link)
    json_data = response.json()['data']['timings']
    fajr = json_data['Fajr']
    duhar = json_data['Dhuhr']
    asar = json_data['Asr']
    maghrib = json_data['Maghrib']
    isha = json_data['Isha']
    dailyTimings.append(fajr)
    dailyTimings.append(duhar)
    dailyTimings.append(asar)
    dailyTimings.append(maghrib)
    dailyTimings.append(isha)
    print(dailyTimings)


def speak(_text):
    engine = pyttsx3.init()
    engine.say(_text)
    engine.runAndWait()


def transcribe_audio():
    recognizer = sr.Recognizer()
    # Use the microphone as source for input.
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio_data = recognizer.listen(source)
        print("Recognizing...")
        # Convert speech to text
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


def main():
    while True:
        # Step 2: Transcribe audio to text
        text = transcribe_audio()
        if text:
            # Convert the text to lowercase to make the check case-insensitive
            text_lower = text.lower()

            # Check if the text contains both "tv" and "on"
            if "tv" in text_lower and "on" in text_lower:
                turn_tv_on()

            # Check if the text contains both "tv" and "off"
            elif "tv" in text_lower and "off" in text_lower:
                turn_tv_off()
            elif "prayer" in text_lower and "next" in text_lower and "time" in text_lower:
                tell_next_azan()
            else:
                speak("This doesnt match any category")


def turn_tv_on():
    print("TV is being turned on...")
    subprocess.run(['./on.sh'])
    time.sleep(10)
    speak("TV has been turned on")


def turn_tv_off():
    subprocess.run(['./on.sh'])                 #this changes the channel to raspberry if tv is already on
    time.sleep(5)
    speak("TV is being turned off...")
    subprocess.run(['./off.sh'])


def tell_next_azan():
    subprocess.run(['./on.sh'])                 #this changes the channel to raspberry if tv is already on
    time.sleep(10)
    speak("Calculating time for next prayer ...")
    fetchTimes()
    now = datetime.now()                        # current date and time
    current_time_str = now.strftime("%H:%M")
    current_time = datetime.strptime(current_time_str, "%H:%M")

    # Find the next prayer time
    next_prayer_time = None
    next_prayer_name = None
    for i, prayer_time_str in enumerate(dailyTimings):
        prayer_time = datetime.strptime(prayer_time_str, "%H:%M")
        if prayer_time > current_time:
            next_prayer_time = prayer_time_str
            next_prayer_name = prayers[i]
            break
    time.sleep(3)
    if next_prayer_time and next_prayer_name:
        speak(f"The next prayer is {next_prayer_name} at {next_prayer_time}.")
    else:
        speak("No more prayers for today.")

    time.sleep(5)
    subprocess.run(['./off.sh'])


if __name__ == "__main__":
    main()
