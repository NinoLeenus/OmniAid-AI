import streamlit as st
from telegram_fetcher import fetch_messages, send_approved_reply
from bedrock_processor import analyze_message
from vector_store import load_vector_db
from dynamodb import is_processed, mark_processed
from s3_storage import store_raw_message

db = load_vector_db()

st.set_page_config(layout="wide")
st.title("🟢 OmniAid AI – Volunteer Decision Support System (AWS)")

if "pending_messages" not in st.session_state:
    st.session_state.pending_messages = []
if "analysis_by_id" not in st.session_state:
    st.session_state.analysis_by_id = {}

if st.button("Fetch Telegram Messages"):
    try:
        messages = fetch_messages()
    except ValueError as exc:
        st.error(
            f"{exc}. Set TELEGRAM_BOT_TOKEN in environment or .env and restart Streamlit."
        )
        st.stop()

    pending_messages = []
    for msg in messages:
        if is_processed(msg["id"]):
            continue
        store_raw_message(msg)
        pending_messages.append(msg)

    st.session_state.pending_messages = pending_messages
    st.session_state.analysis_by_id = {}
    st.success(f"Fetched {len(pending_messages)} new Telegram messages")

if not st.session_state.pending_messages:
    st.info("No pending Telegram messages. Click 'Fetch Telegram Messages' to load new messages.")

for msg in st.session_state.pending_messages:
    message_id = msg["id"]

    st.subheader(f"From: {msg['author']}")
    st.write(msg["body"])

    if message_id not in st.session_state.analysis_by_id:
        docs = db.similarity_search(msg["body"], k=2)
        context = "\n".join([d.page_content for d in docs])
        with st.spinner("Analyzing with Amazon Bedrock..."):
            st.session_state.analysis_by_id[message_id] = analyze_message(msg["body"], context)

    result = st.session_state.analysis_by_id[message_id]
    ticket_id = f"TICKET-{message_id}"
    st.markdown("### Ticket Details")
    st.write(f"**Ticket Number:** {ticket_id}")
    st.write(f"**Case Type:** {result['case_type']}")
    st.write(f"**Urgency:** {result['urgency']}")
    st.markdown(f"**Summary:** {result.get('summary', '')}")
    st.markdown(f"**Response:** {result.get('response', '')}")

    if st.button(f"Approve & Mark Done ({message_id})", key=f"approve_{message_id}"):
        try:
            send_approved_reply(
                msg,
                result.get("summary", ""),
                result.get("response", ""),
            )
            mark_processed(message_id)

            st.session_state.pending_messages = [
                m for m in st.session_state.pending_messages if m["id"] != message_id
            ]
            st.session_state.analysis_by_id.pop(message_id, None)

            st.success("Replied in Telegram and marked as processed")
            st.rerun()
        except Exception as exc:
            st.error(f"Failed to reply/mark processed: {exc}")
