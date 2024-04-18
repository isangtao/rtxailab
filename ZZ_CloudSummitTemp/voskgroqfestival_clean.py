# voskgroqfestival voice app
# © 2024 Michael Carlos
# Version: 1.0.0
# Originally developed in 2023. Added groq in 2024.

#!/usr/bin/env python3
# sudo apt install python3.11-venv libportaudio2 festival festvox-us-slt-hts (delete all other voices under /usr/share/festival/voices/)
# pip install sounddevice vosk groq (use 'espeak' instead of 'festival --tts' for faster, but robotic, response)

import queue
import sounddevice as sd
import json
import os
from vosk import Model, KaldiRecognizer
import datetime
from groq import Groq

client = Groq(api_key="<API_KEY>")

wake_word = "cameron"
system_prompt = """You are a T-900 A.I., a reprogrammed terminator brain. Your mission is to ensure the survival of Rado. Answer as a T-900 only. Be concise and answer in short sentences. Be succinct."""

q = queue.Queue()
device_info = sd.query_devices("default")
samplerate = int(device_info["default_samplerate"])
model = Model(lang="en-us")
 
def callback(indata, frames, time, status):
    q.put(bytes(indata))

def getsentence():
    data = q.get()
    if rec.AcceptWaveform(data):
        sentence = json.loads(rec.Result())
        return sentence['text']

with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, dtype="int16", channels=1, callback=callback):
    rec = KaldiRecognizer(model, samplerate)
    while True:
        text_input = getsentence()
        if text_input and wake_word in text_input:
            prompt_text = text_input[text_input.find(wake_word):]
            prompt_text = prompt_text[len(wake_word)+1:]
            if len(prompt_text):
                print(f"\n{prompt_text}")
                d = datetime.date.today().strftime("%B %d, %Y")
                t = datetime.datetime.now().strftime("%I:%M %p") 
                prompt_final = system_prompt + f"\n\nToday's date is {d} and the current time is {t}. \n\nAnswer the following query: \n{prompt_text}"
                response = client.chat.completions.create(messages=[{"role": "user", "content": prompt_final}], model="mixtral-8x7b-32768").choices[0].message.content
                os.system(f"echo \"{response}\" | festival --tts")  
