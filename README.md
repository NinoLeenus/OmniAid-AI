# OmniAid AI – Volunteer Decision Support System (AWS)

This project uses AWS Generative AI and AWS infrastructure to help NGO volunteers manage large volumes of distress messages.

## AWS Services Used
- Amazon Bedrock (amazon.titan-text-lite-v1)
- DynamoDB (processed messages)
- S3 (raw message storage)
- EC2 (Streamlit app hosting)

## Features
- Telegram message ingestion
- AI classification & urgency detection
- NGO knowledge retrieval (FAISS)
- Volunteer dashboard
- Human-in-the-loop

## Setup
1. Create DynamoDB table: OmniAidMessages (PK: message_id)
2. Create S3 bucket: omniaid-raw-messages
3. Enable Bedrock access
4. Set `.env` with Telegram bot credentials (`TELEGRAM_BOT_TOKEN`)
5. Run:
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0

## Ethics
No automated replies. All responses reviewed by volunteers.

How AWS services are use
Function	AWS Service
LLM reasoning	Amazon Bedrock
Message storage	Amazon S3
Duplicate detection	DynamoDB
Hosting	EC2
Security	IAM
Logs	CloudWatch

## To run in EC2
Download pem keyfile and keep it in codespace
chmod 600 OminiAI-EC2.pem
ssh -i yourkey.pem ubuntu@<EC2_PUBLIC_IP>
sudo apt update && sudo apt install python3.12-venv
✅ Step 1: Verify you are on EC2 (not Codespace)

Run in your terminal:

whoami

If it shows:

ubuntu

or similar → you are on EC2 ✅

Check IP:

curl ifconfig.me

That should show your EC2 public IP.

✅ Step 2: Clone your repo on EC2

On EC2 terminal:

git clone https://github.com/<your-username>/OmniAid-AI.git
cd OmniAid-AI

(or if already copied, just cd into folder)


✅ Step 3: Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

You should see:

(venv) ubuntu@ip-xxx

✅ Step 4: Install dependencies
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

✅ Step 5: Run Streamlit app
streamlit run app.py --server.address 0.0.0.0 --server.port 8501

to kill port usage
lsof -ti:8501 | xargs kill -9

You should see:

Running on:
http://0.0.0.0:8501

http://3.104.64.179:8501