# OmniAid AI – Reddit Message Intelligence Prototype

AI system to help NGOs manage large volumes of Reddit distress messages.

## Features
- Fetch Reddit messages
- AI classification & urgency detection
- Summary & draft response
- Volunteer dashboard (human-in-loop)

## Setup

1. Install dependencies:
pip install -r requirements.txt

2. Create Reddit App:
https://www.reddit.com/prefs/apps

3. Create .env file:
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret

4. Run app:
streamlit run app.py

## Ethics
AI does not auto-send messages. Human approval required.

### How to run in local
git clone your-repo
cd omniaid-ai-prototype
pip install -r requirements.txt
streamlit run app.py

http://localhost:8501

### How to deploy on AWS EC2 instance
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

http://EC2_PUBLIC_IP:8501