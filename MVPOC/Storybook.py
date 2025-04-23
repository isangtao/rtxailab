# python -m venv ai
# source ai/bin/activate
# pip install streamlit openai
# curl -fsSL https://ollama.com/install.sh | sh
# ollama pull gemma3:1b
# streamlit run AgentPromptLab.py

import streamlit as st
from openai import OpenAI

string_data = ''
api_url = 'http://localhost:11434/v1'
api_key = '1234'
api_model = 'gemma3:1b'

client = OpenAI(base_url = api_url, api_key=api_key)

with st.sidebar:
	st.title("Storybook maker \n© 2025 Michael Carlos")
	name = st.text_input("Protagonist's name", "Michael")
	gender = st.selectbox("Gender", ("Male", "Female", "Other"))
	age = st.text_input("Age", "54")
	interests = st.text_input("Interests", "motorcycling, martial arts, archery, hiking, kayaking, snorkeling")
	occupation = st.text_input("Occupation", "Software Developer")
	country = st.text_input("Country", "Canada")
	city = st.text_input("City", "Vancouver")
	other = st.text_input("Other", "n/a")
	style = st.selectbox("Style", ("Children's book", "Teen adventure", "Adult novel"))
	plot = st.text_input("High level plot summary", "Travels to the Philippines and starts a new life")

if st.button("Generate"):
	prompt_context = f"Here are some details about the protagonist: \nName:{name} \nGender:{gender}\nAge:{age}\nInterests:{interests}\nOccupation:{occupation}\nCountry:{country}\nCity:{city}\nOther:{other}\n"
	prompt_query = f"\nIn the style of a(n) {style}, write a story based on the following plot. Do not explain what you are doing, just jump into the story: {plot}"
	template_combined = prompt_context + prompt_query + "\n"
	stream = client.chat.completions.create(model=api_model, messages=[{"role": "user", "content": template_combined,},],stream = True)
	with st.spinner():
		msg = st.empty()
		response = ""
		for chunk in stream:
			if chunk.choices[0].delta:
				response += chunk.choices[0].delta.content
				msg.markdown(response)
