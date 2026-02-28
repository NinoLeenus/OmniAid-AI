# OmniAid AI – Volunteer Message Intelligence System

AI system to help NGOs manage distress messages using open-source LLMs.

## Stack
- Llama3 (Ollama)
- FAISS Vector DB
- Streamlit UI
- SQLite
- Hosted on AWS EC2

## Setup

1. Install Ollama:
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3

2. Create .env file:
REDDIT_CLIENT_ID=xxx
REDDIT_CLIENT_SECRET=xxx

3. Install dependencies:
pip install -r requirements.txt

4. Run app:
streamlit run app.py --server.address 0.0.0.0

## Ethics
Human-in-the-loop, no auto replies, privacy-first.


# How to deploy it on ec2 #####
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker

docker build -t omniaid-ai .
docker run -p 8501:8501 omniaid-ai