import streamlit as st
from main import results

st.set_page_config(page_title="TaskMind AI Assistant", layout="wide")
st.title("🤖 TaskMind AI Assistant")

# --- Custom CSS for Chat UI ---
st.markdown("""
    <style>
        .chat-container {
            max-height: 400px;
            overflow-y: scroll;
            padding: 1rem;
            background-color: #1e1e1e;
            border-radius: 10px;
            border: 1px solid #333;
            margin-top: 1rem;
            margin-bottom: 2rem;
        }
        .message {
            padding: 0.75rem 1rem;
            border-radius: 10px;
            margin-bottom: 0.75rem;
            max-width: 75%;
            font-size: 1rem;
            line-height: 1.4;
            word-wrap: break-word;
        }
        .user {
            background-color: #343541;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        .bot {
            background-color: #444654;
            color: white;
            margin-right: auto;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# --- Session Setup ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Input Box ---
user_input = st.text_input("You:", key="input")

# --- Handle New Message ---
if user_input:
    st.session_state.history.append(("user", user_input))
    response = results("Broddy", user_input)

    if isinstance(response, dict):
        if response["type"] == "text":
            st.session_state.history.append(("bot", response["content"]))
        elif response["type"] == "image":
            image_html = f'<img src="{response["path"]}" width="250">'
            st.session_state.history.append(("bot", image_html))
        elif response["type"] == "map":
            map_html = f'<a href="{response["url"]}" target="_blank">🗺️ View Map</a>'
            st.session_state.history.append(("bot", map_html))
    else:
        st.session_state.history.append(("bot", str(response)))

    # Clear input
    st.session_state.input = ""

# --- Display Current Exchange ---
if st.session_state.history:
    last_msg = st.session_state.history[-2:]
    for sender, msg in last_msg:
        if "img" in msg or "<a" in msg:
            st.markdown(f'<div class="message {sender}">{msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message {sender}">{msg}</div>', unsafe_allow_html=True)

# --- Display Full Chat History (scrollable) ---
st.markdown("### 💬 Chat History")
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for sender, msg in st.session_state.history[:-2]:  # excluding current messages
    if "img" in msg or "<a" in msg:
        st.markdown(f'<div class="message {sender}">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message {sender}">{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
