import streamlit as st
from reddit_fetcher import fetch_messages
from bedrock_processor import analyze_message
from vector_store import load_vector_db
from dynamodb import is_processed, mark_processed
from s3_storage import store_raw_message

db = load_vector_db()

st.set_page_config(layout="wide")
st.title("🟢 OmniAid AI – Volunteer Decision Support System (AWS)")

if st.button("Fetch Reddit Messages"):
    messages = fetch_messages()

    for msg in messages:
        if is_processed(msg["id"]):
            continue

        store_raw_message(msg)

        st.subheader(f"From: {msg['author']}")
        st.write(msg["body"])

        docs = db.similarity_search(msg["body"], k=2)
        context = "\n".join([d.page_content for d in docs])

        with st.spinner("Analyzing with Amazon Bedrock..."):
            result = analyze_message(msg["body"], context)

        st.markdown("### 🤖 AI Analysis")
        st.text(result)

        if st.button(f"Approve & Mark Done ({msg['id']})"):
            mark_processed(msg["id"])
            st.success("Marked as processed")
            