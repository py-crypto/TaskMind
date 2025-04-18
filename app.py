import streamlit as st
from main import results, Username

st.set_page_config(page_title="TaskMind Chatbot", layout="centered")

st.title("🤖 TaskMind - Your Personal AI Assistant")
st.markdown("Ask me anything or tell me to perform a task!")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Input box
user_input = st.chat_input("Type your message here...")

# Display chat history
for entry in st.session_state.chat:
    if entry["type"] == "text":
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])
    elif entry["type"] == "image":
        with st.chat_message(entry["role"]):
            st.image(entry["path"])
    elif entry["type"] == "map":
        with st.chat_message(entry["role"]):
            st.markdown(f"[🗺️ Click here to view the map]({entry['url']})")

# Process new input
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat.append({"role": "user", "type": "text", "content": user_input})

    with st.spinner("Thinking..."):
        response = results(Username, user_input)

    if response["type"] == "text":
        st.chat_message("assistant").markdown(response["content"])
        st.session_state.chat.append({"role": "assistant", "type": "text", "content": response["content"]})

    elif response["type"] == "image":
        st.chat_message("assistant").image(response["path"])
        st.session_state.chat.append({"role": "assistant", "type": "image", "path": response["path"]})

    elif response["type"] == "map":
        st.chat_message("assistant").markdown(f"[🗺️ Click here to view the map]({response['url']})")
        st.session_state.chat.append({"role": "assistant", "type": "map", "url": response["url"]})
