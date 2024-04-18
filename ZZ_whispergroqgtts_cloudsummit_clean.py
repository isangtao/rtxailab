# whispergroqgtts voice app
# © 2024 Michael Carlos
# Version: 1.0.0
# Originally developed in 2023. Added groq in 2024.

# sudo apt install jackd2 portaudio19-dev
# pip install wheel faster-whisper speechrecognition sounddevice pyaudio gtts playsound 
# Optional: pip install pycairo pygobject 

import json
import speech_recognition as sr
from faster_whisper import WhisperModel
import sounddevice # To hide ALSA messages
import datetime
from groq import Groq
from gtts import gTTS
import playsound
import os

client = Groq(api_key="<API_KEY>")

wake_word = "cameron"
system_prompt = """User information: The user's name is Michael. He is very passionate about advancing AI.
\nThe current location is Vancouver, British Columbia, Canada. The timezone is PT.
\nOther useful information: The metric system is used here. Use celcius. Do not use imperial.
\nYou are a T-900 A I, a reprogrammed terminator brain. Your human name is Cameron. Answer as a T-900 only. Be concise and answer in short sentences. Be succinct."""

whisper_model = WhisperModel('tiny', compute_type = "int8")
recog = sr.Recognizer()
source = sr.Microphone()
with source:
    recog.adjust_for_ambient_noise(source, duration=2)
    os.system("clear")

while True:
    with source:
        audio = recog.listen(source, phrase_time_limit = 8)
        with open("voice.wav", "wb") as f:
            f.write(audio.get_wav_data())
        segments, _ = whisper_model.transcribe('voice.wav')
        text_input = ''.join(segment.text for segment in segments)
        text_input = text_input.lower().strip()
        if wake_word in text_input:
            prompt_text = text_input[text_input.find(wake_word):]
            prompt_text = prompt_text[len(wake_word)+1:]
            if len(prompt_text):
                d = datetime.date.today()
                t = datetime.datetime.now().strftime("%I:%M %p") 
                prompt_final = system_prompt + f"\n\nToday's date is {d} and the current time is {t}. \n\nAnswer the following query: \n{prompt_text}"
                print(f"\n{prompt_text}")
                response = client.chat.completions.create(messages=[{"role": "user", "content": prompt_final}], model="mixtral-8x7b-32768")
                response_text = response.choices[0].message.content
                print(response_text)
                myobj = gTTS(response_text, lang = 'en', tld = 'us') # https://gtts.readthedocs.io/en/latest/module.html#localized-accents
                myobj.save("gtts_response.mp3") 
                playsound.playsound("gtts_response.mp3")
