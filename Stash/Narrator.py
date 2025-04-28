# Setup:
# install miniconda 
# conda create -n ai python=3.11
# conda activate ai
# pip install streamlit openai coqui-tts torch torchvision torchaudio
# Update API info below (or install Ollama e.g. curl -fsSL https://ollama.com/install.sh | sh && ollama pull llama3.2)
# tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 --text "The quick brown fox jumps over the lazy dog." --speaker_wav sample.wav --language_idx en
# streamlit run Narrator.py

import streamlit as st
from openai import OpenAI
import torch
from TTS.api import TTS

api_url = 'http://localhost:11434/v1'
api_key = '1234'
api_model = 'llama3.2'

st.set_page_config(layout = "wide")
client = OpenAI(base_url = api_url, api_key = api_key)

@st.cache_resource
def get_tts():
	gpu_flag = True if torch.cuda.is_available() else False
	tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu = gpu_flag)
	return tts

with st.sidebar:
	st.title("Narrator \n© 2025 Michael Carlos")
	name = st.text_input("Protagonist's name", "Michael Carlos")
	ethnicity = st.text_input("Ethnicity", "Filipino")
	gender = st.text_input("Gender", "Male")
	age = st.text_input("Age", "55")
	height = st.text_input("Height", "5ft 10in")
	interests = st.text_input("Interests", "robotics, motorcycling, aikido, archery, hiking, kayaking, snorkeling")
	occupation = st.text_input("Occupation", "AI Researcher")
	country = st.text_input("Country of residence", "Canada")
	city = st.text_input("City of residence", "Vancouver")
	other = st.text_input("Other", "Founded A G I Labs Inc, a company focused on Artificial General Intelligence. He developed a real-time, reinforcement-learning algorithm that grows exponentially.")
	additional = st.text_area("Additional Instructions", "Make it a happy story with sunshine and warm weather. Set it near a utopian downtown Vancouver in the near future. Depict Robots as decent, helpful and protective.")
	style = st.selectbox("Style", ("Adult novel", "Teen adventure", "Childrens' book"))
	plot_type = st.selectbox("Type", ("Science fiction", "Suspense", "Thriller", "Action", "Adventure", "Fantasy", "Horror", "Mystery"))
	context = f"Details about the protagonist of a story follows. \n\nName: {name}\n\nEthnicity: {ethnicity}\n\nGender: {gender}\n\nAge: {age}\n\nHeight: {height}\n\nInterests: {interests}\n\nOccupation: {occupation}\n\nCountry of residence: {country}\n\nCity of residence: {city}\n\nOther:{other}\n\n"

if st.button("Generate"):
	plot_prompt = f"{context}Provide an unusual {plot_type} plot based on the information above. {additional} Don't explain or preamble. Just state the plot summary in one sentence."
	completion = client.chat.completions.create(model=api_model, messages=[{"role": "user", "content": plot_prompt ,},])
	plot = completion.choices[0].message.content
	template_combined = f"{context}\n\nPlot:{plot}\n\nIn the style of a {plot_type} {style}, write a story based on the plot. {additional} Provide no explanation or preamble. Just state the title and jump into the story.\n\n"
	with st.expander("Prompt Info"):
		st.write(template_combined)
	stream = client.chat.completions.create(model=api_model, messages=[{"role": "user", "content": template_combined,},], stream = True)
	with st.spinner():
		msg = st.empty()
		response = ""
		for chunk in stream:
			if chunk.choices[0].delta:
				response += chunk.choices[0].delta.content
				msg.markdown(response)
		st.write("Generate 10 images based on the story above. https://aistudio.google.com/prompts/new_chat \n\nGenerating audio...")
		get_tts().tts_to_file(text=response, speaker_wav="sample.wav", language="en", file_path="output.wav")
		st.audio("output.wav")
