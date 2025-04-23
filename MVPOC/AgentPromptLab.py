# python -m venv ai
# source ai/bin/activate
# pip install streamlit openai
# curl -fsSL https://ollama.com/install.sh | sh
# ollama pull gemma3:1b
# streamlit run AgentPromptLab.py

import streamlit as st
from openai import OpenAI
from io import StringIO

string_data = ''
api_url = 'http://localhost:11434/v1'
api_key = '1234'
api_model = 'gemma3:1b'

client = OpenAI(base_url = api_url, api_key=api_key)

with st.sidebar:
	st.title("Agent Prompt Lab \n© 2025 Michael Carlos")
	uploaded_file = st.file_uploader("Choose a text file")
	if uploaded_file:
		stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
		string_data = stringio.read()
	api_url = st.text_input("API URL", api_url)
	api_key = st.text_input("API key", api_key)
	api_model = st.text_input("Model", api_model)

prompt = st.chat_input()
if prompt:
	prompt_context = f"\n\nUse this context to answer the user's query below: \n<context>\n{string_data}\n</context>"
	prompt_query = f"\n\nAnswer the following query: \n{prompt}"
	template_combined = prompt_context + prompt_query + "\n"
	with st.chat_message("user"):
		st.write("```" + template_combined + "```")
	stream = client.chat.completions.create(model=api_model, messages=[{"role": "user", "content": template_combined,},],stream = True)
	with st.chat_message("assistant"):
		with st.spinner():
			msg = st.empty()
			response = ""
			for chunk in stream:
				if chunk.choices[0].delta:
					response += chunk.choices[0].delta.content
					msg.markdown(response)
