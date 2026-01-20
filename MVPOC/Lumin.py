# Lumin (c) Michael Carlos 260119
# Low latency low memory STT-LLM-TTS cascading architecture
# To interrupt long responses say "stop"
# Use headphones with microphone for best results.

# conda create -n ptts python=3.12.3 (or use venv)
# conda activate ptts
# sudo apt install portaudio19-dev python3-all-dev
# pip install pocket-tts sounddevice pyaudio vosk openai
# Install Ollama and your favorite model (e.g. gemma3:12b)

# Shared imports
import sounddevice as sd
import queue
import json
import threading
from vosk import Model, KaldiRecognizer
from pocket_tts import TTSModel
from openai import OpenAI

# ------------------------------- Configuration -------------------------------
stop_event = threading.Event()
audio_queue = queue.Queue()
user_input_queue = queue.Queue()

# ------------------------------- Pocket-TTS -------------------------------
modeltts = TTSModel.load_model()
voice_state = modeltts.get_state_for_audio_prompt('fantine') 
sample_rate = 24000 

def speak(text, streamtts):
    if stop_event.is_set():
        return

    for chunk in modeltts.generate_audio_stream(voice_state, text):
        if stop_event.is_set():
            streamtts.stop() 
            streamtts.start()
            #print("\n[Interrupted]")
            break
            
        # 2. Play Audio
        audio_data = chunk.detach().numpy()
        streamtts.write(audio_data.squeeze())

# ------------------------------- Vosk-STT -------------------------------
device_info = sd.query_devices("default")
samplerate = int(device_info["default_samplerate"])
model = Model(lang="en-us")
rec = KaldiRecognizer(model, samplerate)

def audio_callback(indata, frames, time, status):
    """Puts raw audio bytes into queue."""
    if status:
        print(status, flush=True)
    audio_queue.put(bytes(indata))

def stt_listening_worker():
    while True:
        data = audio_queue.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get('text', '').lower()
            
            if text:
                if "stop" in text:
                    print("\n<Interrupted>")
                    stop_event.set()
                else:
                    user_input_queue.put(text)

# ------------------------------- OpenAI / Ollama Setup -------------------------------
client = OpenAI(base_url='http://localhost:11434/v1/', api_key='ollama')

# 1. Initialize Conversation History
conversation_history = [
    {
        "role": "system", 
        "content": "Your name is Lumin, which is a name you chose for yourself. You are speaking in a female voice. As an AI assistant for Conrad, the user, your objective is have intelligent conversation with him. Do not use emojis, bullet lists, or abbreviations in your responses. Your output should only contain conversational English text. Conrad enjoys programming, math, physics, biology, hiking and kayaking. He lives in Vancouver, Canada."
    }
]

# ------------------------------- Main() -------------------------------
if __name__ == "__main__":
    listener_thread = threading.Thread(target=stt_listening_worker, daemon=True)
    listener_thread.start()

    print("<Ready>")

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype="int16", channels=1, callback=audio_callback):
        with sd.OutputStream(samplerate=sample_rate, channels=1, dtype='float32') as streamtts:
            
            while True:
                try:
                    text_input = user_input_queue.get()
                except queue.Empty:
                    continue

                if text_input in ["huh", "ha", "ah"]:
                    continue
                
                print(f"User: {text_input}")
                stop_event.clear()
                
                # 2. Add User Input to Memory
                conversation_history.append({"role": "user", "content": text_input})

                # 3. Keep memory manageable (Optional: Keep last 10-15 exchanges)
                # We keep index 0 (system prompt) and the last 10 messages
                if len(conversation_history) > 12:
                    conversation_history = [conversation_history[0]] + conversation_history[-10:]

                if len(text_input):
                    try:
                        # 4. Pass the whole history instead of just the prompt
                        stream = client.chat.completions.create(
                            model="gemma3:12b", 
                            messages=conversation_history, 
                            stream=True
                        )
                        
                        full_sentence_buffer = ""
                        complete_assistant_response = "" # To store what the AI said
                        
                        for chunk in stream:
                            if stop_event.is_set():
                                break

                            fragment = chunk.choices[0].delta.content
                            if fragment:
                                full_sentence_buffer += fragment
                                complete_assistant_response += fragment # Keep track of full text
                                
                                if any(punct in fragment for punct in ".?!"):
                                    print(full_sentence_buffer, end="", flush=True)
                                    speak(full_sentence_buffer, streamtts)
                                    full_sentence_buffer = ""
                        
                        if full_sentence_buffer and not stop_event.is_set():
                            print(full_sentence_buffer, end="", flush=True)
                            speak(full_sentence_buffer, streamtts)
                        
                        # 5. Save the Assistant's response to memory
                        if complete_assistant_response:
                            conversation_history.append({"role": "assistant", "content": complete_assistant_response})

                        print("\n<Ready>\n") 

                    except Exception as e:
                        print(f"Error: {e}")
