# RTX AI LAB
## Screenshots
![RTX AI Lab Screenshot](https://github.com/isangtao/rtxailab/blob/main/rtxailab.gif)
## Objectives
* to provide an environment where researchers can easily experiment with, compare and combine models to innovate quickly.
* to provide minimalist source code for developers to copy and chain together in their own applications.
* [Please see LLM_POC_Overview_1.0.pdf for details](https://github.com/isangtao/rtxailab/blob/main/LLM_POC_Overview_1.0.pdf)
## Description
* This application combines the following modes into one UI.
  * Model comparison
  * Internet Search - RAG1
  * Personas & Living FAQs
  * Real-time Image Generation
  * Vision
  * Voice Cloning
* Roadmapped Features
  * PDF to Vector Database - RAG2 (TBD)
  * Voice Dialog STT-LLM-TTS (TBD)
  * T2V - Sora or next Open Model (TBD)
  * Text-to-3D Asset (TBD)
  * Function Calling (TBD)
  * Motion generation - Virtual Robotics (TBD)
  * AI Driven Physics (TBD)
  * AI World Rendering - Gaussian Splatting (TBD)
  * IsangTao i.e. One-person dev team employing true AI agents (TBD)
* This application has been developed and tested on Ubuntu 22.04 with an RTX4070 12GB and 32GB of RAM. This has not been tested on Windows or Mac.
## Setup:
* Download [rtxailab.py](https://github.com/isangtao/rtxailab/blob/main/rtxailab.py)
* Install CUDA
  * Ref: https://developer.nvidia.com/cuda-downloads
* Create and activate a new python environment
  * ```python -m venv rtxailab```
  * ```source rtxailab/bin/activate```
  * You can also use Conda if that is your preference.
* Install dependencies 
  * ```pip install streamlit ollama openai duckduckgo_search streamlit-keyup diffusers torch transformers tts```
  * You may need to exit your terminal, log back in and reactivate the rtxailab environment to register streamlit for the first time.
* Install Ollama
  * Ref: https://ollama.com/
  * Ollama is available for Linux, Mac and Windows and supports the OpenAI API standard. The Linux install command is shown below.
  * ```curl -fsSL https://ollama.com/install.sh | sh```
* Download local LLMs
  * ```ollama pull dolphin-mistral``` (4.1GB uncensored)
  * ```ollama pull stablelm-zephyr``` (1.6GB censored)
  * ```ollama pull tinyllama``` (637MB uncensored)
  * ```ollama pull solar``` (6.1GB censored)
  * ```ollama run qwen:0.5b``` (394MB fast function calling)
  * ```ollama pull llava``` (4.7GB vision)
  * Feel free to add any new models to the code.
* Run application
  * ```streamlit run rtxailab.py```
