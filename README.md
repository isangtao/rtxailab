# RTX AI LAB
## Screenshot
![RTX AI Lab Screenshot](https://github.com/isangtao/rtxailab/blob/main/Screenshot%20from%202024-02-22%2020-10-16.png?raw=true)
## Objective
* The objective is to provide an environment where researchers and developers can easily experiment with, compare and combine models to create new innovations quickly.
* [Please see LLM_POC_Overview_1.0.pdf for details](https://github.com/isangtao/rtxailab/blob/main/LLM_POC_Overview_1.0.pdf)
## Description
* This application combines the following modes into one UI.
  * Model comparison
  * Internet Search
  * Agents/Personas
  * Image Generation
  * Vision
  * Voice Cloning
  * RAG (TBD)
  * STT - LLM - TTS (TBD)
  * T2V (TBD)
  * Function Calling (TBD)
  * Motion generation (TBD)
  * AI Driven Physics (TBD)
  * AI World Rendering (TBD)
  * Isang Tao i.e. one-person dev team (TBD)
## Setup:
* install cuda
* python -m venv ai
* source ai/bin/activate
* pip install streamlit ollama openai duckduckgo_search streamlit-keyup diffusers torch transformers tts
* curl -fsSL https://ollama.com/install.sh | sh
* ollama pull tinyllama, solar, qwen & llava
* streamlit run rtxlab.py
