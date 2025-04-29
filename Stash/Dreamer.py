# Setup:
# python -m venv ai
# source ai/bin/activate
# pip install streamlit openai 
# Update API info below (or install Ollama e.g. curl -fsSL https://ollama.com/install.sh | sh && ollama pull llama3.2)
# streamlit run Dreamer.py

import streamlit as st
from openai import OpenAI

api_url = 'http://localhost:11434/v1'
api_key = '1234'
api_model = 'llama3.2'

st.set_page_config(layout="wide")
client = OpenAI(base_url = api_url, api_key=api_key)

with st.sidebar:
	st.title("Dreamer \n© 2025 Michael Carlos")
	name = st.text_input("Protagonist's name", "Michael Carlos")
	ethnicity = st.text_input("Ethnicity", "Filipino")
	gender = st.text_input("Gender", "Male")
	age = st.text_input("Age", "55")
	height = st.text_input("Height", "5ft 10in")
	interests = st.text_input("Interests", "robotics, motorcycling, aikido, archery, hiking, kayaking, snorkeling")
	occupation = st.text_input("Occupation", "AI Researcher")
	country = st.text_input("Country of residence", "Canada")
	city = st.text_input("City of residence", "Vancouver")
	other = st.text_input("Other", "Founded A G I Labs Inc, a company focused on Artificial General Intelligence. He developed a real-time, reinforcement-learning architecture that self-organizes through evolutionary algorithms.")
	additional = st.text_area("Additional Instructions", "Give the story a happy ending. Set it in a utopian downtown Vancouver in the near future with sunshine and warm weather. Depict Robots as decent, helpful and protective. Do not address Michael Carlos as Dr. or Mike.")
	style = st.selectbox("Style", ("Adult novel", "Teen adventure", "Childrens' book"))
	plot_type = st.selectbox("Type", ("Science fiction", "Suspense", "Thriller", "Action", "Adventure", "Fantasy", "Horror", "Mystery"))
	context = f"Details about the protagonist of a story follows. \n\nName: {name}\n\nEthnicity: {ethnicity}\n\nGender: {gender}\n\nAge: {age}\n\nHeight: {height}\n\nInterests: {interests}\n\nOccupation: {occupation}\n\nCountry of residence: {country}\n\nCity of residence: {city}\n\nOther:{other}\n\n"

if st.button("Generate"):
	plot_prompt = f"{context}Provide an unusual {plot_type} plot based on the information above. {additional} Don't explain or preamble. Just state the plot summary in one sentence."
	completion = client.chat.completions.create(model=api_model, messages=[{"role": "user", "content": plot_prompt}], temperature=0.9)
	plot = completion.choices[0].message.content
	template_combined = f"{context}\n\nPlot:{plot}\n\nIn the style of a {plot_type} {style}, write a story based on the plot. {additional} Provide no explanation or preamble. Just state the title and jump into the story.\n\n"
	with st.expander("Prompt Info"):
		st.write(template_combined)
	stream = client.chat.completions.create(model=api_model, messages=[{"role": "user", "content": template_combined}], temperature=0.9, stream = True)
	with st.spinner():
		msg = st.empty()
		response = ""
		for chunk in stream:
			if chunk.choices[0].delta:
				response += chunk.choices[0].delta.content
				msg.markdown(response)
		st.write("Generate 10 images for the story above. Do not include text. Do not depict children. https://copilot.microsoft.com/ https://aistudio.google.com/prompts/new_chat")
