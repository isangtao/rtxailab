# python -m venv ai
# source ai/bin/activate
# pip install streamlit openai
# Update API info below (or install Ollama e.g. curl -fsSL https://ollama.com/install.sh | sh && ollama pull gemma3:1b)
# streamlit run AgentPromptLab.py

import streamlit as st
from openai import OpenAI
from io import StringIO

string_data = ''
client = OpenAI(base_url = 'http://localhost:11434/v1', api_key='1234')

with st.sidebar:
	st.title("Prompt Lab \n© 2025 Michael Carlos")
	uploaded_file = st.file_uploader("Choose a text file")
	if uploaded_file:
		stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
		string_data = stringio.read()

prompt = st.chat_input()
if prompt:
	template_combined = f"<context>\n\n{string_data}\n\n</context>\n\n{prompt}"
	with st.chat_message("user"):
		st.write("```" + template_combined + "```")
	stream = client.chat.completions.create(model='gemma3:1b', messages=[{"role": "user", "content": template_combined,},],stream = True)
	with st.chat_message("assistant"):
		with st.spinner():
			msg = st.empty()
			response = ""
			for chunk in stream:
				if chunk.choices[0].delta:
					response += chunk.choices[0].delta.content
					msg.markdown(response)
