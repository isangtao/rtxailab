# sudo apt install libportaudio2 festival festvox-us-slt-hts (delete all other voices under /usr/share/festival/voices/)
# pip install sounddevice vosk (replace 'festival --tts' with 'espeak' for faster, but robotic, response)
# curl -fsSL https://ollama.com/install.sh | sh
# ollama pull tinyllama (637MB uncensored)

import queue
import sounddevice as sd
import os
import json
from vosk import Model, KaldiRecognizer

wake_word = "computer"

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
                prompt_final = f"Be concise and succinct. Answer in a single sentence if possible. Answer the following query: {prompt_text}"
                print(prompt_final)
                os.system(f"ollama run tinyllama \"{prompt_final}\" | tee out && cat out | festival --tts")
