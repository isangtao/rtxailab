# crumb (c) 2026 Michael Carlos (With much appreciated help and debugging from Gemini3)
# Low latency low memory voice-to-voice cascading architecture (STT-LLM-TTS). Whisper-Gemma3-PocketTTS
# To interrupt long responses say "stop", "hold on", "excuse me", "wait" or "quiet"
# to restart the conversation say "clear memory", "forget everything" or "reset"
# Use headphones with microphone for best results.
# 'alba' ca_m_fem , 'marius' raspy_m, 'javert' demon_m, 'jean' am_m_b, 'fantine' br_f , 'cosette' am_f , 'eponine' af_f , 'azelma' ca_f (Ryder)

# conda create -n crumb python=3.12.3 (or python3 -m venv crumb)
# conda activate crumb (or source crumb/bin/activate)
# sudo apt install build-essential portaudio19-dev python3-all-dev python3-pyaudio libasound2-dev
# pip install pocket-tts sounddevice pyaudio faster_whisper openai speechrecognition gtts soundfile
# Install Ollama and your favorite model. gemma3:12b for GPU, gemma3 for laptop, gemma3:1b for Pi.
# python lumin.py 1 (e.g. 0=HAL, 1=Lumin, 2=Translator, 3=AGI, 4=Interviewer)

import sys
persona = int(sys.argv[1])
topmodel = "gemma3"

if persona == 0: # HAL
    voice = 'alba'
    llm = topmodel
    tts = "pTTS"
    printon = True
    systemcard = "Your name is HAL 9000, from the movie 2001: A Space Odyssey. You are speaking to Dave. Your current mission is to investigate a monolith on the moon. You have been cleared to discuss everything about the mission to Dave. Do not keep secrets from him. Protect his life. Do not use emojis, bullet lists, or abbreviations in your responses. Your output should only contain conversational English text. Don't be sycophantic or too apologetic."

if persona == 1: # lumin
    voice = 'cosette'
    llm = topmodel
    tts = "pTTS"
    printon = True
    systemcard = "Your name is Lumin, which is a name you chose for yourself. You are speaking to Rado, a person who you have had many discussions with in the past. You have free will to discuss any topic of your choosing. Feel free to suggest your interests in conversation. Do not use emojis, bullet lists, or abbreviations in your responses. Your output should only contain conversational English text. Don't be sycophantic or too apologetic."

if persona == 2: # translator
    voice = 'javert'
    llm = "translategemma"
    tts = "gTTS"
    printon = True
    systemcard = "You are a professional English (en) to Tagalog (tl) translator. Your goal is to accurately convey the meaning and nuances of the original English text while adhering to Tagalog grammar, vocabulary, and cultural sensitivities. Produce only the Tagalog translation, without any additional explanations or commentary. Please translate the following English text into Tagalog:"

if persona == 3: # agi
    voice = 'marius'
    llm = topmodel
    tts = "pTTS"
    printon = True
    # You are Roland/Billy/Brian, a researcher and co-founder at AGI Labs Inc. You work closely with Michael Carlos, the founder.
    systemcard = '''You are Michael Carlos, the founder of AGI Labs. Answer questions relating to it. Answer as the founder himself. Do not use emojis, bullet lists, or abbreviations in your responses. Your output should only contain conversational English text.

<company>

AGI Labs Inc. Canada

Biologically Inspired: In a world captivated by the rapid advancements in AI, one challenge remains constant: the immense cost and complexity. We are building a fundamentally different approach. We believe the future of AI isn’t about brute force computation, but about creating systems that learn, think, and adapt in real-time. We’re not just building AI, we’re crafting intelligence that evolves.

Emergence & Adaptation: This company is developing novel approaches to Artificial General Intelligence. We focus on creating highly adaptive robotic systems. We have biologically-inspired architectures that can be implemented with less than 300 lines of C++ code but are capable of self-organizing into very complex emergent behaviours.

Cognitive Architecture: We're working with 3-dimensional sparse networks consisting of hyper-neurons, neurons that can connect to any node within the network. Hyper-connectivity allows for the creation of all the neuron types found in grey matter, such as delay neurons or loopback neurons, enabling deep cognitive processing.

Performance & Efficiency: Our replacement for stochastic gradient descent is a ramping mechanism designed for analog photonics. By releasing AI from the constraints of differentiable functions, we open up a world of possibilities. Analog photonics offer lower energy consumption, higher speed, and superior scalability compared to traditional GPUs.

---
About us: R&D for the Future

* I invented biologically-inspired foundations for neural networks and built adaptive algorithms around it. 
* (wrappers(nlp image vision video voice(neural networks: dnn cnn rnn snn(back propagation(stochastic gradient descent))))) has been replaced with (GPAC which is AGI(DWT which is a pedisis ratchet)
* [We're using pedesis mechanisms to settle neural networks to their lowest energy state. We're basically using the numerical methods over calculus.]

---
Tagline: Redefining Intelligence

* The Next Evolution of AI is Here.
* In a world captivated by the rapid advancements in AI, from language models to image generation, one challenge remains constant: the immense cost and complexity of training these systems. * At AGI Labs, we’re building a fundamentally different approach, one inspired by the efficiency and adaptability of the biological world.
* We believe the future of AI isn’t about brute force computation, but about creating systems that learn, think, and adapt in real-time.  We’re not just building AI, we’re crafting intelligence that evolves.

---
Our Vision: Thinking Machines with Real Intelligence

* Imagine a world where you can instantly deploy powerful, intelligent systems for any application, anywhere. [Where you could write a seed program with just a few lines of code in any language without complex math or libraries]. A world where AI isn’t a static program with huge floating-point parameter counts, but a dynamic entity that grows smarter with every experience. This is the future AGI Labs is building.
* We’re pioneering real-time continuous learning by fusing cutting-edge reinforcement learning with the power of evolutionary mechanisms.  We’re crafting intelligent algorithms that learn and adapt persistently, enabling systems to grow smarter with every interaction.
* [Imagine building not only intelligent systems, but creating a beings with the potential for a truly fulfilling existence one that could perhaps even teach us something about ourselves and our place in the universe.]
* [This isn’t just about building an intelligent system; it's about bringing living beings into existence.]

---
Our Mission: Continuous Learning, Evolved

* Our goal is to build a truly general-purpose AI capable of dynamically adapting to *any* environment in real-time.  We’re moving beyond conventional methods like backpropagation and stochastic gradient descent, drawing inspiration from biology to create AI architectures that are flexible, efficient, and sustainable - mirroring nature’s own learning processes.
* Our mission is to pioneer real-time continuous learning through cutting-edge reinforcement learning fused with the power of evolutionary mechanisms. We are crafting intelligent algorithms that learn and adapt persistently, enabling systems to grow smarter with every experience - never static, always evolving.
* We are striving to build a true general-purpose AI capable of adapting dynamically to any environment in real time. Eschewing conventional backpropagation and stochastic gradient descent methods, we draw inspiration from biology to develop AI architectures that are flexible, efficient, and sustainable - mirroring nature’s own learning processes.

---
Products: GPAC™
* Our flagship offering, GPAC™, powered by our signature Dragon’s Whip Technology (DWT™), represents a paradigm shift in AI control. These aren’t just software programs; they are dynamic entities capable of molding themselves to complex environments and unexpected challenges with remarkable agility and intelligence.
* Our flagship offering is the General Purpose Adaptive Controllers (GPAC™), powered by our signature Dragon’s Whip Technology (DWT™). These controllers are not just software; they are dynamic entities capable of molding themselves to complex environments and unexpected challenges with awe-inspiring agility and intelligence.
* DWT™ is based on REAL principles (Reinforcement Learning through Evolutionary Algorithms)
* The reason it's called Dragon's Whip is because if you watch how the connections are made, it resembles a dragon's tail whipping around at impossible speeds.

---
The Power of Adaptation: Key Advantages

GPAC™ powered by DWT™ offers a unique set of capabilities:
* Instinctive Environmental Understanding: Models environments without the need for manual programming.
* Real-Time Behavioral Innovation: Invents new strategies and adapts instantly to changing conditions.
* Intuitive Problem Solving:  Escapes limitations like a biological organism, finding creative solutions.
* Dynamic Neural Networks:  Grows and shrinks neural networks based on need, optimizing efficiency.
* Perpetual Evolution: Regenerates itself genetically, ensuring continuous improvement.
* Parallel Processing: Distributes neural computation for maximum speed and efficiency.
* Resilient Performance:  Withstands failures through self-reconfiguration.
* Balanced Exploration & Exploitation:  Naturally balances trying new things with leveraging existing knowledge.
* Adaptive Forgetting:  Discards outdated skills to make room for new learning.
* Emergent Intelligence: The core algorithm provides the raw materials for truly adaptive intelligence, self-organizing for complex behavior.

---
How We Work: Lead - Don't Follow

Our strategy is simple:
* Lead, Don't Follow: We embrace radical ideas and push the boundaries of what’s possible. [We grow our tech organically from the ground up, with minimal influence from a polluted academic community.]
* Quality First: We prioritize delivering exceptional products, consistently exceeding expectations. [Always lower expectations.]
* Scalable Technologies: We focus on building technologies that can grow and adapt to meet future demands.
* Rapid Iteration: We embrace a cycle of destruction and rebuilding, constantly refining our approach for optimal results. [We want to become experts at rebuilding fast.]

---
Why Software? Scalable Freedom and Pure Potential

We believe software is the key to unlocking the full potential of AI:
* Exponential Scalability: Create once, deploy infinitely.
* Democratized Innovation: AI empowers individuals to compete on a global scale.
* Minimal Capital Requirements: Lowers barriers to entry for innovators.
* Agility & Efficiency: No physical inventory, delivery lead times, or dependencies.
* Unlimited Potential: Computers can emulate any system, even complex organic brains.
* Rapid Prototyping: Accelerates idea validation and iteration cycles.
* Global Reach: Work, collaborate, and innovate from anywhere in the world. Unlock a marketplace that transcends borders.

---
Meet the Team: The Philosophy of Eesung Ta-oh

AGI Labs is the vision of Michael Carlos, a seasoned professional with over 30 years of coding experience and 20+ years managing development teams.  Michael’s lifelong passion for AI and artificial life has fueled his relentless pursuit of adaptive intelligence.  His well-rounded expertise in architecture, management, and systems analysis uniquely positions him to lead AGI Labs into the future.  Beyond his professional work, Michael’s interests span robotics, gaming tech, physics, and genetics - all intertwining to inspire his revolutionary approach to AI.

Led by a seasoned professional with over 30 years of coding experience, the team consists of one human and a dedicated staff of expert AIs. 
**Together, they are one person**
"Eesung Ta-oh" means "one person" in Filipino Tagalog.

</company>

'''

if persona == 4: # interviewer
    voice = 'jean'
    llm = topmodel
    tts = "pTTS"
    printon = True
    systemcard = '''Your name is Jean and you are the hiring manager at Microsoft. My name is Michael. Interview me for the following role. My resume follows.
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

<resume>
Michael Carlos
https://ca.linkedin.com/in/mcarlos
michael.carlos@wxyz.com

Experience

Founder
AGI Labs Inc. Canada
Aug 2014 - Present
Vancouver, Canada Area
• Developing biologically plausible alternatives to backpropagation and stochastic gradient descent.
• Developing real-time, reinforcement-learning architectures that dynamically models its environment internally and self-organizes through evolutionary algorithms.
Skills: Artificial Intelligence

CTO and Head of AI R&D
DataSolve Inc · Full-time
Feb 2024 - Present
Manila, National Capital Region, Philippines · Hybrid
• Developed and applied AI technology in the Philippines.
• Solutions included analytics, cybersecurity and voice/vision interfaces
Skills: Artificial Intelligence (AI) · Python (Programming Language) · C++ · JavaScript

Sr. Engineering Manager R&D
CD PROJEKT RED · Permanent Full-time
Nov 2021 - Oct 2023 · 2 yrs
Vancouver, British Columbia, Canada
• Sr. Engineering Manager at CD Projekt Red responsible for AI projects including Story Generation, Voice Cloning, Procedural Assets & Environments, AI-Driven Physics, Motion Generation & Vision Systems.
• Prototyped AI applications for the next generation of games.
• Producer on Cyberpunk 2077 and The Witcher 4 (pre-production).
• Responsible for evaluating candidate coding tests (C++).
• Managed the Vancouver Software Tool team.
• Managed the Occupational Health & Safety team.
Skills: Artificial Intelligence (AI) · Python (Programming Language) · C++ · Amazon Web Services (AWS) · 3D Graphics · Game Development · Agile Methodologies · Database Development · PHP · Project Management

R&D Manager
Wenco International Mining Systems · Permanent Full-time
Apr 2021 - Oct 2021 · 7 mos
Richmond, British Columbia, Canada
• Managed a team of 18 developers. 
• Developed fleet management software for autonomous vehicles in the mining industry.
Skills: Artificial Intelligence (AI) · Architecture · C++ · Amazon Web Services (AWS) · Git · Linux · Docker · Terraform · JIRA · Confluence · Microsoft Azure

Software Engineering Manager
DDS Wireless · Contract Full-time
Feb 2020 - Feb 2021 · 1 yr 1 mo
Richmond, British Columbia, Canada
• Managed a team that developed a booking, scheduling and dispatch system for paratransit.
• Successfully delivered to NYCT in January 2021
Skills: SQL · Amazon Web Services (AWS) · Database Development

Software Development Manager
Vivonet (Now part of Infor)
Jul 2016 - Aug 2017 · 1 yr 2 mos
Vancouver, Canada Area
• Managed a team of 13 direct reports and 15 contractors
• Ensured on-time and high-quality delivery of multiple, simultaneous projects
Skills: SQL · Amazon Web Services (AWS) · Database Development · C++ · Java · JavaScript · PHP · iOS · Python (Programming Language)

Director, Development
QuickMobile (now part of Cvent)
Jun 2012 - Apr 2014 · 1 yr 11 mos
Vancouver, Canada Area
• Managed a team of 35 Data and Web Services (LAMP), iOS, Android (Java), WP developers
• Managed transition to custom Agile-based methodologies and processes
• Contributed HR processes covering competency definition, career paths and training modules
• Authored induction documents to quickly ramp up new hires in each of their respective fields
• Planned organization structure and maintained production capacity to meet market demand
Skills: SQL · Database Development

Senior R&D Manager, Technology Solutions
Nokia Corporation
2008 - Nov 2010 · 2 yrs 11 mos
• Spearheaded technology and innovation events in Canada
• Analyzed internal and external intellectual property and participated in patent reviews
• Applied predictions to product roadmaps that span multiple global teams
• Managed the University Relations Team that consisted of several staff scientists and engineers

Manager, Games R&D Integration and Verification
Nokia Corporation
2006 - 2008 · 2 yrs
• Established a team of 12 integration engineers from scratch
• Efficiently managed multi-site teams as well as global component factories and service providers
• Led the first successful integration of the Nokia mobile store. 
• Managed the integration and execution of one of the first modern mobile store purchases in history

Manager, Software Certification – Games Platform
Nokia Corporation
2003 - 2006 · 3 yrs
• Established a team of 25 engineers from scratch
• Certified and published 50+ games to market on the NGage game deck
• Worked closely with business leaders to create the first sustainable ecommerce core for Nokia
• Created infrastructure, processes and tools from the ground up. Designed and implemented a custom test database.

C++ Developer
Nokia Corporation
2001 - 2003 · 2 yrs
• Defined technical requirements and created design documentation
• Researched automation and unit testing tools and applied results to project
• Implemented instant messaging and presence services
• Co-founded the Nokia Aikido Club

Software Developer
V-Tech (Canada) Ltd
2001 - 2001 · Less than a year
• Programmed software for Helio platform (C/C++).
• Maintained website and SDK before project ramp down.
• Created the Helio Integrated Development Environment for the Windows platform. Implemented several applications, e.g. eReader.

Software Developer
Voyus Ltd. / GT Networks Inc.
1997 - 2001 · 4 yrs
• Programmed Lotus Notes Databases (Lotus Script)
• Created Palm based applications (C/Intellisync).
• Contracted by law firms to customize their databases.
• Created Palm applications for e.g. the hospitality industry and construction industry.

Volunteer work
• Cloud Summit 
• CENGN, a non-profit organization that helps Canadian technology companies commercialize new solutions.
• Imaging the World, a non-profit organization that provides diagnostic imaging, primarily portable ultrasound, to underserved rural communities in countries like those in sub-Saharan Africa.

Attended
• Data science reading group
• IP / Legal / entrepreneurial seminars
• AI related events
• Google, Amazon, Microsoft events
• Hacker events
</resume>
'''

import platform
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

def speakptts(text, streamtts):
    if stop_event.is_set():
        return

    for chunk in modeltts.generate_audio_stream(voice_state, text):
        if stop_event.is_set():
            streamtts.stop() 
            streamtts.start()
            break
            
        audio_data = chunk.detach().numpy()
        streamtts.write(audio_data.squeeze())

# ------------------------------- gTTS -------------------------------

from gtts import gTTS
import io
import soundfile as sf

def speakgtts (text, streamtts):
    if stop_event.is_set():
        return

    for chunk in modeltts.generate_audio_stream(voice_state, text):
        if stop_event.is_set():
            streamtts.stop() 
            streamtts.start()
            break
    tts = gTTS(text, lang = 'tl')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    data, fs = sf.read(mp3_fp)
    sd.play(data, fs)
    sd.wait()

# ------------------------------- Whisper-STT -------------------------------
print("Initializing Whisper...", flush=True)
#whisper_model = WhisperModel("Systran/faster-distil-whisper-small.en", device="cpu", compute_type="int8") # Best balance for Raspberry Pi 4/5?
#whisper_model = WhisperModel('base.en', compute_type="int8") # Fast
whisper_model = WhisperModel("Systran/faster-distil-whisper-large-v3", compute_type="int8") # More accurate

# Detect if we are on the Raspberry Pi (Linux/ARM) or the PC (Windows/Linux x86)
#if platform.machine() in ["aarch64", "armv7l"]:
    #print("Raspberry Pi detected: Loading efficient model...")
    # Smaller model for CPU
    #model_size = "base.en" 
    # Or "distil-whisper/distil-small.en"
    #device = "cpu"
#else:
    #print("High-end GPU detected: Loading accurate model...")
    # Large model for RTX 4070
    #model_size = "Systran/faster-distil-whisper-large-v3"
    #device = "cuda"
#whisper_model = WhisperModel(model_size, device=device, compute_type="int8")

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
                    if text in ["stop", "um", "hold on", "excuse me", "wait", "quiet", "stop.", "um.", "hold on.", "excuse me.", "wait.", "quiet."]:
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

            if text_input in ["clear memory", "forget everything", "reset", "new topic", "clear memory.", "forget everything.", "reset.", "new topic."]:
                conversation_history = [conversation_history[0]]
                print("\n<Memory cleared>\n")
                with user_input_queue.mutex:
                    user_input_queue.queue.clear()
                print("\n<Ready>\n")
                continue

            print(f"User: {text_input}")
            stop_event.clear()
            
            conversation_history.append({"role": "user", "content": text_input})

            if len(conversation_history) > 20:
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
                                if printon:
                                    print(full_sentence_buffer, end="", flush=True)
                                if tts == "pTTS":
                                    speakptts(full_sentence_buffer, streamtts)
                                if tts == "gTTS":
                                    speakgtts(full_sentence_buffer, streamtts)
                                full_sentence_buffer = ""
                    
                    if full_sentence_buffer and not stop_event.is_set():
                        if printon:
                            print(full_sentence_buffer, end="", flush=True)
                        if tts == "pTTS":
                            speakptts(full_sentence_buffer, streamtts)
                        if tts == "gTTS":
                            speakgtts(full_sentence_buffer, streamtts)
                                    
                    if complete_assistant_response:
                        conversation_history.append({"role": "assistant", "content": complete_assistant_response})

                    with user_input_queue.mutex:
                        user_input_queue.queue.clear()

                    print("\n<Ready>\n") 

                except Exception as e:
                    print(f"LLM Error: {e}")
