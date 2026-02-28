# OmniAid AI – Volunteer Decision Support System (AWS)

This project uses AWS Generative AI and AWS infrastructure to help NGO volunteers manage large volumes of distress messages.

## AWS Services Used
- Amazon Bedrock (Claude 3)
- DynamoDB (processed messages)
- S3 (raw message storage)
- EC2 (Streamlit app hosting)

## Features
- Reddit message ingestion
- AI classification & urgency detection
- NGO knowledge retrieval (FAISS)
- Volunteer dashboard
- Human-in-the-loop

## Setup
1. Create DynamoDB table: processed_messages (PK: message_id)
2. Create S3 bucket: omniaid-raw-messages
3. Enable Bedrock access
4. Set .env with Reddit credentials
5. Run:
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