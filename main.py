import speech_recognition as sr
from elevenlabs.client import ElevenLabs
import subprocess
elevenlabs_client = ElevenLabs(api_key="65882d98b6272c225e535c6c2eb4901b")


# Function to transcribe audio to text using Google Cloud Speech-to-Text
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


# Function to synthesize text to speech using ElevenLabs
def synthesize_text(text, output_file_path):
    # Hypothetical method call, adjust based on actual library usage
    response = elevenlabs_client.synthesize_speech(text=text, voice_id="bella")
    with open(output_file_path, "wb") as file:
        file.write(response.audio_content)
    print(f"Synthesized speech saved to {output_file_path}")


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
                print("Turning TV on.")

            # Check if the text contains both "tv" and "off"
            elif "tv" in text_lower and "off" in text_lower:
                turn_tv_off()
                print("Turning TV off.")
            else:
                print("No text transcribed.")


def turn_tv_on():
    print("TV is being turned on...")
    status = subprocess.run(['./status.sh'], capture_output=True)
    status = status.stdout
    status = status.decode('utf-8')
    print(type(status))
    print(status)
    subprocess.run(['./on.sh'])


def turn_tv_off():
    print("TV is being turned off...")
    subprocess.run(['/off.sh'])

def tell_next_azan():
    print("Calculating time for next prayer ...")


if __name__ == "__main__":
    main()
