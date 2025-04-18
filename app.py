import streamlit as st
import asyncio
from main import results  # Your main.py logic

st.set_page_config(page_title="TaskMind AI Assistant", layout="wide")
st.title("🤖 TaskMind AI Assistant")

# User input for name
username = st.text_input("Your name:", value="Broddy")

# Initialize chat history for each unique user
if f"history_{username}" not in st.session_state:
    st.session_state[f"history_{username}"] = []

# Input box for chat
user_input = st.text_input("You:", key="input")

# Process input when user submits
if user_input:
    st.session_state[f"history_{username}"].append(("user", user_input))

    # Call results with both user and prompt
    response = asyncio.run(results(username, user_input))

    # Handle different response types
    if isinstance(response, dict) and response["type"] == "text":
        st.session_state[f"history_{username}"].append(("bot", response["content"]))
    elif isinstance(response, dict) and response["type"] == "image":
        st.session_state[f"history_{username}"].append(("bot", "[image]"))
        st.image(response["path"], caption="Generated Image")
    elif isinstance(response, dict) and response["type"] == "map":
        map_link = f"[🗺️ View Map of {user_input}]({response['url']})"
        st.session_state[f"history_{username}"].append(("bot", map_link))
        st.markdown(map_link, unsafe_allow_html=True)
    else:
        st.session_state[f"history_{username}"].append(("bot", str(response)))

# Display the chat history
for sender, message in st.session_state[f"history_{username}"]:
    with st.chat_message(sender):
        st.markdown(message)
