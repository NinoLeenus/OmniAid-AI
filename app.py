import streamlit as st
from telegram_fetcher import fetch_messages, send_approved_reply
from bedrock_processor import analyze_message
from vector_store import load_vector_db
from dynamodb import is_processed, mark_processed
from s3_storage import store_raw_message

db = load_vector_db()

st.set_page_config(layout="wide")
st.title("🟢 OmniAid AI – Volunteer Decision Support System (AWS)")

if st.button("Fetch Telegram Messages"):
    messages = fetch_messages()
    print(f"Fetched {len(messages)} Telegram messages")

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

        ticket_id = f"TICKET-{msg['id']}"
        st.markdown("### Ticket Details")
        st.write(f"**Ticket Number:** {ticket_id}")
        st.write(f"**Case Type:** {result['case_type']}")
        st.write(f"**Urgency:** {result['urgency']}")
        st.markdown(f"**Summary:** {result.get('summary','')}")
        st.markdown(f"**Response:** {result.get('response','')}")

        if st.button(f"Approve & Mark Done ({msg['id']})"):
            try:
                send_approved_reply(
                    msg,
                    result.get("summary", ""),
                    result.get("response", ""),
                )
                mark_processed(msg["id"])
                st.success("Replied in Telegram and marked as processed")
            except Exception as exc:
                st.error(f"Failed to reply/mark processed: {exc}")
            