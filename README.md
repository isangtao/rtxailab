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
  * Agents i.e. Personas
  * Image Generation
  * Vision
  * Voice Cloning
  * RAG (TBD)
  * STT - LLM - TTS (TBD)
  * T2V (TBD)
  * Text-to-3D Asset (TBD)
  * Function Calling (TBD)
  * Motion generation (TBD)
  * AI Driven Physics (TBD)
  * AI World Rendering (TBD)
  * Isang Tao i.e. One-person dev team employing true AI agents (TBD)
* This application has been developed and tested on Ubuntu. It should work on Windows and Mac natively although these have not been tested.
## Setup:
* Install CUDA
  * Ref: https://developer.nvidia.com/cuda-downloads
* Create and activate a new python environment
  * ```python -m venv ai```
  * ```source ai/bin/activate```
* Install dependencies 
  * ```pip install streamlit ollama openai duckduckgo_search streamlit-keyup diffusers torch transformers tts```
* Install Ollama
  * Ref: https://ollama.com/
  * ```curl -fsSL https://ollama.com/install.sh | sh```
  * ```ollama pull tinyllama, solar, qwen & llava```
* Run application
  * ```streamlit run rtxlab.py```
