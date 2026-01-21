# Lumin (c) Michael Carlos 260121 (With much appreciated help from Gemini3)
# Low latency low memory STT-LLM-TTS cascading architecture. Whisper-Gemma12-PocketTTS
# To interrupt long responses say "stop", "hold on", "excuse me", "wait" or "quiet"
# to restart the conversation say "clear memory", "forget everything" or "reset"
# Use headphones with microphone for best results.
# 'alba' ca_m , 'marius' raspy_m, 'javert' army_m, 'jean' am_m_b, 'fantine' br_f , 'cosette' am_f , 'eponine' af_f , 'azelma' ca_f (Ryder)

# conda create -n ai python=3.12.3 (or python3 -m venv ai)
# conda activate ai (or source ai/bin/activate)
# sudo apt install portaudio19-dev python3-all-dev
# pip install pocket-tts sounddevice pyaudio vosk openai
# Install Ollama and your favorite model (e.g. gemma3:12b)

persona = 1

if persona == 1: # lumin
    voice = 'fantine'
    llm = "gemma3:12b"
    systemcard = "Your name is Lumin, which is a name you chose for yourself. You are speaking in a female voice via TTS. Conrad is the user and he just wants to have casual conversation. Do not use emojis, bullet lists, or abbreviations in your responses. Your output should only contain conversational English text."

if persona == 2: # interviewer
    voice = 'jean'
    llm = "gemma3:12b"
    systemcard = '''You are the hiring manager at Microsoft. Interview me for the following role:
<job description>
Principal Researcher - Artificial Specialized Intelligence - Microsoft Research 

About the job

Overview

Microsoft Research Asia – Vancouver lab, located in the vibrant city of Vancouver, BC, Canada, our lab represents Microsoft Research Asia’s exciting expansion into the Asia-Pacific region. We’re on a mission to transform the future of artificial intelligence by bridging the gap between cutting-edge general AI and the specialized, real-world applications that drive meaningful impact.

We are currently seeking a Principal Researcher in the area of Artificial Specialized Intelligence, with a keen interest in developing cutting-edge large foundation models and post-training techniques for different domains and scenarios.

At the Vancouver Lab, we focus on deeply integrating intelligent systems across every layer of computing—from infrastructure to the physical environment. Our goal is to solve complex, real-world challenges with precision, scalability, and cost-efficiency. This means working at the intersection of AI, human interaction, and environmental context through a dynamic, co-evolutionary process.

If you're passionate about pushing the boundaries of Artifical Intelligence (AI) and want to be part of a team that’s shaping the future of intelligent systems, we invite you to explore opportunities with us. This is an opportunity to drive an ambitious research agenda while collaborating with diverse teams to push for novel applications of those areas. 

Microsoft’s mission is to empower every person and every organization on the planet to achieve more. As employees we come together with a growth mindset, innovate to empower others, and collaborate to realize our shared goals. Each day we build on our values of respect, integrity, and accountability to create a culture of inclusion where everyone can thrive at work and beyond.

In alignment with our Microsoft values, we are committed to cultivating an inclusive work environment for all employees to positively impact our culture every day.

Responsibilities

Conduct cutting-edge research in large foundation models, focusing on applying large foundation models in specific domain. 
Collaborate with cross-functional teams to integrate solutions into Artificial Intelligence (AI) -driven system. 
Develop and maintain research prototypes and software tools, ensuring that they are well-documented and adhere to best practices in software development. 
Publish research findings in top-tier conferences and journals and present your work at industry events. 
Collaborate with other AI researchers and engineers, sharing knowledge and expertise to foster a culture of innovation and continuous learning within the team.
Embody our culture and values.

Qualifications

Required Qualifications:

Doctorate in relevant field AND 3+ years related research experience
OR equivalent experience.
3+ years experience in research related to Artificial Intelligence or Machine Learning.
Preferred Qualifications

Doctorate in relevant field AND 5+ years related research experience
OR equivalent experience. 
Experience publishing academic papers as a lead author or essential contributor.
Experience participating in a top conference in relevant research domain.
Background in system and architecture, including experience with computer hardware, software, and networking technologies.
Deep knowledge about the latest large model training/inference technology such as instruction finetuning, Reinforcement Learning (RL) and Reinforcement Learning with Hindsight Experience Replay (RLHF), processed and self-reward modeling, low-precision training/inference, etc.
A track record of published research in the field of AI or other system innovation is a plus.
Keen interest in general AI research, including but not limited to large foundation models.
Research Sciences IC5 - The typical base pay range for this role across Canada is CAD $142,400 - CAD $257,500 per year.
</job description>
        '''

import sounddevice as sd
import queue
import threading
import speech_recognition as sr
from faster_whisper import WhisperModel
from pocket_tts import TTSModel
from openai import OpenAI
import io  # NEW: Required for in-memory audio processing

# ------------------------------- Configuration -------------------------------
stop_event = threading.Event()
user_input_queue = queue.Queue()

# ------------------------------- Pocket-TTS -------------------------------
modeltts = TTSModel.load_model()
voice_state = modeltts.get_state_for_audio_prompt(voice) 
sample_rate = 24000 

def speak(text, streamtts):
    if stop_event.is_set():
        return

    for chunk in modeltts.generate_audio_stream(voice_state, text):
        if stop_event.is_set():
            streamtts.stop() 
            streamtts.start()
            break
            
        audio_data = chunk.detach().numpy()
        streamtts.write(audio_data.squeeze())

# ------------------------------- Whisper-STT -------------------------------
print("Initializing Whisper...", flush=True)
whisper_model = WhisperModel('base.en', compute_type="int8")

recog = sr.Recognizer()
mic_source = sr.Microphone()

with mic_source:
    print("Adjusting for ambient noise...", flush=True)
    recog.adjust_for_ambient_noise(mic_source, duration=2)
    recog.energy_threshold += 50 
    recog.pause_threshold = 1.5  # Wait 1.5s before assuming sentence is over

def stt_listening_worker():
    """Captures audio, processes in RAM, transcribes with Whisper."""
    print("Listening background thread started...", flush=True)
    while True:
        try:
            with mic_source as source:
                try:
                    # Listen for up to 25s, timeout after 2s of silence
                    audio = recog.listen(source, phrase_time_limit=25, timeout=2)
                except sr.WaitTimeoutError:
                    continue 

                # OPTIMIZATION: Process in RAM (No file I/O)
                # 1. Get the WAV data as raw bytes
                wav_bytes = audio.get_wav_data()
                
                # 2. Create a file-like object in memory
                wav_stream = io.BytesIO(wav_bytes)
                
                # 3. Transcribe directly from the memory stream
                segments, info = whisper_model.transcribe(
                    wav_stream, 
                    vad_filter=True,
                    vad_parameters=dict(min_silence_duration_ms=500),
                    beam_size=5
                )
                
                text = ''.join(segment.text for segment in segments)
                text = text.lower().strip()
                
                if not text:
                    continue
                
                # Filters
                hallucinations = ["you", "thank you.", "thanks for watching.", "subtitles by", "copyright", "mm-hmm.", "mm-hmm"]
                if any(h in text for h in hallucinations) and len(text.split()) < 3:
                    continue
                
                if len(text) > 0 and text.count(text[0]) == len(text):
                    continue

                if text:
                    if text in ["stop", "hold on", "excuse me", "wait", "quiet", "stop.", "hold on.", "excuse me.", "wait.", "quiet."]:
                        print(f"\n<Interrupted: {text}>\n")
                        stop_event.set()
                    else:
                        user_input_queue.put(text)
        except Exception as e:
            print(f"STT Error: {e}")

# ------------------------------- OpenAI / Ollama Setup -------------------------------
client = OpenAI(base_url='http://localhost:11434/v1/', api_key='ollama')

conversation_history = [
    {
        "role": "system", 
        "content": systemcard
    }
]

# ------------------------------- Main() -------------------------------
if __name__ == "__main__":
    listener_thread = threading.Thread(target=stt_listening_worker, daemon=True)
    listener_thread.start()

    with user_input_queue.mutex:
        user_input_queue.queue.clear()

    print("\n<Ready>\n")

    with sd.OutputStream(samplerate=sample_rate, channels=1, dtype='float32') as streamtts:
        
        while True:
            try:
                text_input = user_input_queue.get()
            except queue.Empty:
                continue

            if text_input in ["clear memory", "forget everything", "reset", "clear memory.", "forget everything.", "reset."]:
                conversation_history = [conversation_history[0]]
                print("\n<Memory cleared>\n")
                with user_input_queue.mutex:
                    user_input_queue.queue.clear()
                print("\n<Ready>\n")
                continue

            print(f"User: {text_input}")
            stop_event.clear()
            
            conversation_history.append({"role": "user", "content": text_input})

            if len(conversation_history) > 12:
                conversation_history = [conversation_history[0]] + conversation_history[-10:]

            if len(text_input):
                try:
                    stream = client.chat.completions.create(
                        model=llm, 
                        messages=conversation_history, 
                        stream=True
                    )
                    
                    full_sentence_buffer = ""
                    complete_assistant_response = "" 
                    
                    for chunk in stream:
                        if stop_event.is_set():
                            break

                        fragment = chunk.choices[0].delta.content
                        if fragment:
                            full_sentence_buffer += fragment
                            complete_assistant_response += fragment
                            
                            if any(punct in fragment for punct in ".?!"):
                                print(full_sentence_buffer, end="", flush=True)
                                speak(full_sentence_buffer, streamtts)
                                full_sentence_buffer = ""
                    
                    if full_sentence_buffer and not stop_event.is_set():
                        print(full_sentence_buffer, end="", flush=True)
                        speak(full_sentence_buffer, streamtts)
                    
                    if complete_assistant_response:
                        conversation_history.append({"role": "assistant", "content": complete_assistant_response})

                    with user_input_queue.mutex:
                        user_input_queue.queue.clear()

                    print("\n<Ready>\n") 

                except Exception as e:
                    print(f"LLM Error: {e}")
