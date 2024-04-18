# Basic setup for Flowise (Local)

# Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull stablelm-zephyr
ollama pull nomic-embed-text

# Flowise
sudo apt update
sudo apt install -y npm
sudo npm install -g flowise
npx flowise start --FLOWISE_USERNAME=user --FLOWISE_PASSWORD=1234
