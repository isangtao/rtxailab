# python -m venv ai
# source ai/bin/activate
# pip install streamlit openai
# Update API info below (or install Ollama e.g. curl -fsSL https://ollama.com/install.sh | sh && ollama pull gemma3:1b)
# streamlit run Dreamer.py

import streamlit as st
from openai import OpenAI

api_url = 'http://localhost:11434/v1'
api_key = '1234'
api_model = 'gemma3:1b'

client = OpenAI(base_url = api_url, api_key=api_key)

with st.sidebar:
	st.title("Dreamer \n© 2025 Michael Carlos")
	name = st.text_input("Protagonist's name", "Michael")
	gender = st.text_input("Gender", "Male")
	age = st.text_input("Age", "45")
	height = st.text_input("Height", "5ft 10in")
	interests = st.text_input("Interests", "motorcycling, Aikido, archery, hiking, kayaking, snorkeling")
	occupation = st.text_input("Occupation", "AI Researcher")
	country = st.text_input("Country", "Canada")
	city = st.text_input("City", "Vancouver")
	other = st.text_input("Other", "Owns a company focused on AGI research")
	style = st.selectbox("Style", ("Adult novel", "Teen adventure", "Children's book"))
	plot_select = st.selectbox("Select a plot summary", ("Travels to the Philippines and starts a new life", "After a battle on an alien world, meets a beautiful enemy alien girl and befriends her.", "Learns to levitate and fly", "Creates an AI that mimics biological intelligence"))
	plot = st.text_input("Or create your own", plot_select)

if st.button("Generate"):
	prompt_context = f"Here are some details about the protagonist: \nName:{name} \nGender:{gender}\nAge:{age}\nHeight:{height}\nInterests:{interests}\nOccupation:{occupation}\nCountry:{country}\nCity:{city}\nOther:{other}\n"
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
