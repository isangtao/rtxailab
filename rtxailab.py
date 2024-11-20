# RTX AI Lab
# © 2023-2024 Michael Carlos
# Version: 0.3.1
# Date: 20241118
# To do: voice2voice (GLM-4-voice), stt/llm/tts (Vosk,Whisper,Festival,espeak,gtts,xtts), RAG and Video Generation (Sora). Add functions for personas to call. 

# Setup:
# install cuda and miniconda
# conda create -n rtxai python=3.9
# conda activate rtxai
# pip install streamlit ollama openai duckduckgo_search streamlit-keyup diffusers torch transformers tts
# curl -fsSL https://ollama.com/install.sh | sh
# ollama pull moondream, llama3.2:latest, llama3.2:1b, qwen2.5-coder:latest & qwen2.5-coder:1.5b
# streamlit run rtxailab.py

import streamlit as st
import time
import ollama
from openai import OpenAI
from duckduckgo_search import DDGS
from st_keyup import st_keyup
from diffusers import AutoPipelineForText2Image
import torch
from TTS.api import TTS # only works in 3.9

@st.cache_resource
def get_pipe():
    pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sd-turbo" , torch_dtype=torch.float16, variant="fp16")
    pipe.to("cuda")
    return pipe

provider = ''
model = ''
api_key = ''
max_tokens = ''
temp = ''
top_p = ''

def set_llm():
    global provider
    global model
    global api_key
    global max_tokens
    global temp
    global top_p
    provider = ''

    provider = st.radio ("Provider", ('ollama', 'openrouter'))
    if provider == 'ollama':
        model = st.radio ("Models", ('llama3.2:latest', 'llama3.2:1b', 'qwen2.5-coder:latest', 'qwen2.5-coder:1.5b'))
    if provider == 'openrouter':
        api_key = st.text_input("Enter your OpenRouter key","")
        model = st.radio ("Models", ('mistralai/mistral-7b-instruct', 'huggingfaceh4/zephyr-7b-beta', 'openchat/openchat-7b'))
    max_tokens = st.slider("Max Tokens", 100, 8192, 512, help = "Configures the maximum number of tokens in the generated response.")
    temp = st.slider("Temperature", 0.0, 1.0, 0.5, help = "Large language models use probability to construct the words in a sequence. For any given sequence, there is a probability distribution of options for the next word in the sequence. When you set the temperature closer to zero, the model tends to select the higher-probability words. When you set the temperature further away from zero, the model may select a lower-probability word. In technical terms, the temperature modulates the probability density function for the next tokens, implementing the temperature sampling technique. This parameter can deepen or flatten the density function curve. A lower value results in a steeper curve with more deterministic responses, and a higher value results in a flatter curve with more random responses.")
    top_p = st.slider("Top-P", 0.1, 1.0, 0.5, help = "Top P defines a cut off based on the sum of probabilities of the potential choices. If you set Top P below 1.0, the model considers the most probable options and ignores less probable ones. Top P is similar to Top K, but instead of capping the number of choices, it caps choices based on the sum of their probabilities.")

def call_ollama(model, prompt):
    client = OpenAI( base_url="http://localhost:11434/v1", api_key='1234')
    msg = st.empty()
    response = ""
    start_time = time.time()
    stream = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt,},],stream = True)
    for chunk in stream:
        if chunk.choices[0].delta:
            response += chunk.choices[0].delta.content
            msg.markdown(response)
    elapsed_time = (time.time()-start_time)
    with st.expander("Prompt Info"):
        st.write("---")
        st.write(prompt)
        st.write("---")
        st.write(f"Prompt tokens: ~{round(len(prompt)/4)}") # ~4characters/token (per OpenAI)
        st.write(f"Response tokens: ~{round(len(response)/4)}")
        st.write(f"Elapsed time (seconds): {round(elapsed_time,2)}")
        st.write(f"provider: {provider}")
        st.write(f"model: {model}")
        st.write(f"max_tokens: {max_tokens}")
        st.write(f"temperature: {temp}")
        st.write(f"top_p: {top_p}")

def call_openrouter(model, prompt):
    client = OpenAI( base_url="https://openrouter.ai/api/v1", api_key=api_key)
    msg = st.empty()
    response = ""
    start_time = time.time()
    stream = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt,},],stream = True)
    for chunk in stream:
        if chunk.choices[0].delta:
            response += chunk.choices[0].delta.content
            msg.markdown(response)
    elapsed_time = (time.time()-start_time)
    with st.expander("Prompt Info"):
        st.write("---")
        st.write(prompt)
        st.write("---")
        st.write(f"Prompt tokens: ~{round(len(prompt)/4)}")
        st.write(f"Response tokens: ~{round(len(response)/4)}")
        st.write(f"Elapsed time (seconds): {round(elapsed_time,2)}")
        st.write(f"provider: {provider}")
        st.write(f"model: {model}")
        st.write(f"max_tokens: {max_tokens}")
        st.write(f"temperature: {temp}")
        st.write(f"top_p: {top_p}")

mode = "Select Mode"
with st.sidebar:
    st.title("RTX AI Lab \n© 2024 Michael Carlos")
    mode = st.radio ("Modes", ('Image Generation', 'Chat', 'Internet Search', 'Persona', 'Vision', 'Voice Cloning', 'Source')) 
    help = "help tbd"
    if mode == 'Chat':
        help = "This version of chat employs the stock version of the language model. Chat history is not retained between prompts. This mode was included for prompt experimentation, performance benchmarking and quality comparison. Vector stores and agents are not used and there is no calls outside of its network. You can give it instructions such as: \n * Write a poem about Manila. \n * Explain Quantum Entanglement to me like I was a cat. \n * Write helloworld in C++." 
        # \n *The user is asking 'What is the latest news about the Philippines?' Select the best function from the following list to respond to the user's request: weather, calculator, search, image, music. Output only the function name."
        set_llm()
    if mode == 'Internet Search':
        help = "(ChatWeb) Information is retreived from DuckDuckGo and used in the query template as context for a prompt. This works for any current topic and differs from a regular search by allowing creative prompts such as: \n * Write a story about the latest Large Language Models like you're a newscaster breaking news."
        set_llm()
    if mode == 'Persona':
        help = "Super-smart assistants. Living F.A.Q.s. For the example ask the assistant to: \n\n * Describe the property."
        set_llm()
    if mode == "Image Generation":
        help = " * chrome gold skull, carved intricate, set in a forest \n\n * full-body photo of a chrome cyborg in a lab, beautiful face, long hair \n\n * photo of mestizo man, bald, short full-faced beard, thick eyebrows, muscular, sunset, beach"
    if mode == 'Vision':
        help = "Upload a jpeg or png and ask the model to: \n\n * Describe this. \n\n * Write a poem about the scene. \n\n * Write a poem about the subject in the image."
    if mode == 'PDF':
        help = "(ChatPDF) tbd"  # I need to research latest tech. Vector stores and embeddings have changed since the last time I implemented this. Also, is this still required with the current large context windows?
    if mode == 'Voice Cloning':
        help = "Upload a voice sample (3-10sec 22050hz 16bit wav) and enter some text to generate sentences in that voice. Here are some samples: \n\n * Hello! My name is John Smith. \n\n * Large language models use probability to construct the words in a sequence. For any given sequence, there is a probability distribution of options for the next word. \n\n * This version of chat employs the stock version of the language model. Chat history is not retained between prompts. This mode was included for prompt experimentation, performance benchmarking and quality comparison. "
    if mode == 'Documentation':
        help = "This displays the live source code"

def chat():
    prompt = st.chat_input()
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner():
                if provider == 'ollama':
                    call_ollama(model, prompt)
                if provider == 'openrouter':
                    call_openrouter(model, prompt)

def isearch():
    prompt = st.chat_input()
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        with DDGS() as ddgs: # News
            context = ''
            ddgs_news_gen = ddgs.news(prompt, region="wt-wt", safesearch="off", timelimit="m", max_results=10)
            for r in ddgs_news_gen:
                context += str(r['body'])
        prompt_context = f"\n\nHere is the context for the user's query: \n{context}"
        prompt_query = f"\n\nAnswer the following query: \n{prompt}"
        template_combined = prompt_context + prompt_query + "\n"
        with st.chat_message("assistant"):
            with st.spinner():
                if provider == 'ollama':
                    call_ollama(model, template_combined)
                if provider == 'openrouter':
                    call_openrouter(model, template_combined)

def persona():
    with st.expander("System Prompt"):
        persona = st.text_area(label = "Persona", key = "persona", value = "You are an enthusiastic realtor. You answer client questions accurately, professionally and politely.")
        context = st.text_area(label = "Context", key = "context", value = "300m^2. Located close to the university. Shopping mall in walking distance. Hospital within 3km.")
        extra = st.text_area(label = "Extra information (Feed vision output into here)", key = "extra", value = "The house is a beautiful spanish-style villa, next to a sunset beach with fruit trees and palm trees located on the property.")
    prompt = st.chat_input()
    if prompt:
        prompt_context = f"\n\nHere is the context for the user's query: {context} {extra}"
        prompt_query = f"\n\nAnswer the following query: {prompt}"
        template_combined = persona + "\n" + prompt_context + prompt_query + "\n"
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner():
                if provider == 'ollama':
                    call_ollama(model, template_combined)
                if provider == 'openrouter':
                    call_openrouter(model, template_combined)

def pictures():
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
    prompt = st_keyup("Enter Prompt e.g. photo, beach, blue sky, sunshine, Philippines", debounce=500, key="2")
    if prompt:
        negative_prompt = st.text_input("Negative Prompt e.g. extra fingers, extra arms, extra head, extra eyes")
        num_inference_steps = st.slider('Inference Steps', 1, 10, 1)
        image = get_pipe()(prompt = prompt, negative_prompt = negative_prompt, height = 512, width = 512, seed = 0, num_inference_steps = num_inference_steps, guidance_scale = 0.0).images[0]
        st.image(image)

def vision():
    image_file_path = st.file_uploader("Upload your image here", accept_multiple_files=False)
    if image_file_path:
        st.image(image_file_path)
        image_list = [image_file_path]
        prompt = st.chat_input()
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                with st.spinner():
                    msg = st.empty()
                    response = ""
                    stream = ollama.chat(model='moondream', messages=[{'role': 'user','content': prompt,'images': image_list}], stream=True,)
                    for chunk in stream:
                        response += chunk['message']['content']
                        msg.markdown(response)

def voice():
    wav_file = st.file_uploader("Upload your voice sample here (3-10sec 22050hz 16bit wav)", accept_multiple_files=False)
    if wav_file:
        prompt = st.chat_input()
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                with st.spinner():
                    device = "cuda" if torch.cuda.is_available() else "cpu"
                    #tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
                    tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=True).to(device)
                    #wav = tts.tts(text="Hello world!", speaker_wav=wav_file, language="en")
                    tts.tts_to_file(text=prompt, speaker_wav=wav_file, language="en", file_path="output.wav")
                    st.audio("output.wav")
                    #st.audio(wav, format="wav")

def source():
    with open('rtxailab.py', "r") as g:
        st.markdown("``` py\n" + g.read() + "\n```")

st.title(mode, help=help)
if mode == 'Chat':
    chat()
if mode == 'Internet Search':
    isearch()
if mode == 'Persona':
    persona()
if mode == 'Image Generation':
    pictures()
if mode == 'Vision':
    vision()
if mode == 'Voice Cloning':
    voice()
if mode == 'Source':
    source()
