import streamlit as st
from reddit_fetcher import fetch_messages
from llm_processor import analyze_message

st.set_page_config(page_title="OmniAid AI", layout="wide")

st.title("🟢 OmniAid AI – Volunteer Message Intelligence System (Reddit MVP)")
st.write("AI that helps volunteers handle distress messages")

if st.button("Fetch Reddit Messages"):
    messages = fetch_messages()

    for i, msg in enumerate(messages):
        st.subheader(f"Message {i+1} from {msg['author']}")
        st.text(msg["body"])

        with st.spinner("Analyzing message with AI..."):
            ai_result = analyze_message(msg["body"])

        st.markdown("### 🤖 AI Analysis")
        st.write(ai_result)

        response = st.text_area("✍️ Edit Draft Response", ai_result, key=i)

        if st.button(f"Approve & Mark Reviewed {i}"):
            st.success("Response approved (manual send to Reddit)")