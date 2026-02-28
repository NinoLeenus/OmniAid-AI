import sqlite3

conn = sqlite3.connect("messages.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS processed_messages (
    message_id TEXT PRIMARY KEY
)
""")
conn.commit()

def is_processed(msg_id):
    c.execute("SELECT 1 FROM processed_messages WHERE message_id=?", (msg_id,))
    return c.fetchone() is not None

def mark_processed(msg_id):
    c.execute("INSERT OR IGNORE INTO processed_messages VALUES (?)", (msg_id,))
    conn.commit()
    