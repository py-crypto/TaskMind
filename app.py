import streamlit as st
from main import results

st.set_page_config(page_title="TaskMind AI Assistant", layout="wide")
st.markdown("""
    <style>
        .chat-container {
            height: 500px;
            overflow-y: auto;
            padding: 20px;
            background-color: #1e1e1e;
            border: 1px solid #333;
            border-radius: 10px;
        }
        .user-msg, .bot-msg {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            max-width: 80%;
        }
        .user-msg {
            background-color: #343541;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        .bot-msg {
            background-color: #444654;
            color: white;
            margin-right: auto;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 TaskMind AI Assistant")

# Session state to store chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display Chat History in scrollable container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for sender, message in st.session_state.history:
    if sender == "user":
        st.markdown(f'<div class="user-msg">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{message}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Divider
st.markdown("---")

# Input area
user_input = st.text_input("Type your message here...", key="input", label_visibility="collapsed")

if user_input:
    st.session_state.history.append(("user", user_input))
    response = results("Broddy", user_input)

    if isinstance(response, dict) and response["type"] == "text":
        st.session_state.history.append(("bot", response["content"]))
    elif isinstance(response, dict) and response["type"] == "image":
        st.session_state.history.append(("bot", f'<img src="{response["path"]}" alt="Generated Image" width="300"/>'))
    elif isinstance(response, dict) and response["type"] == "map":
        st.session_state.history.append(("bot", f'<a href="{response["url"]}" target="_blank">🗺️ View Map</a>'))
    else:
        st.session_state.history.append(("bot", str(response)))

    st.experimental_rerun()  # Refresh UI to scroll with new messages
