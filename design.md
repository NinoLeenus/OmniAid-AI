# System Design – OmniAid AI (Reddit MVP)

## Architecture Overview
The system uses a Retrieval-Augmented Generation (RAG) pipeline to ingest Reddit messages, classify them, and assist volunteers with structured guidance and draft responses.

## Components

### 1. Message Ingestion Layer
- Reddit API (PRAW)
- Periodic fetch of DMs and posts

### 2. Processing Engine
- Text cleaning
- Language detection
- Case classification
- Urgency detection

### 3. Knowledge Base (Vector Database)
Stores:
- NGO SOPs
- Legal guidelines
- Past resolved cases
- Response templates

Vector DB:
- FAISS or ChromaDB

### 4. AI Engine
- Open-source LLM (Llama 3 / Mistral)
Functions:
- Summarization
- Recommendation
- Draft response generation

### 5. Dashboard Interface
- Streamlit-based UI
- Displays prioritized messages
- Shows suggested responses
- Allows editing and approval

### 6. Safety & Ethics Layer
- Prompt rules to avoid legal advice
- No automatic replies
- Human approval mandatory
- Personal data masking

## Data Flow
1. Reddit messages fetched
2. AI classifies and summarizes
3. Relevant knowledge retrieved
4. Suggested response generated
5. Volunteer reviews and sends reply

## Technology Stack
- Backend: Python
- Reddit API: PRAW
- LLM: Llama 3 / Mistral
- Vector DB: FAISS
- Framework: LangChain
- UI: Streamlit
- Translation: IndicTrans2

## Security
- OAuth authentication
- Encrypted storage
- Role-based access

## Ethical Considerations
- AI assists, not replaces humans
- Transparent recommendations
- Privacy preservation
