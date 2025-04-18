import streamlit as st
from main import results  # your main.py logic

st.set_page_config(page_title="Jarvis AI Assistant", layout="wide")
st.title("🤖 Jarvis AI Assistant")

# For storing chat history in Streamlit session
if "history" not in st.session_state:
    st.session_state.history = []

# Input
user_input = st.text_input("You:", key="input")

# Process Input
if user_input:
    st.session_state.history.append(("user", user_input))

    # Correct synchronous call to results()
    response = results("Broddy", user_input)

    # Handle different response types
    if isinstance(response, dict) and response["type"] == "text":
        st.session_state.history.append(("bot", response["content"]))
    elif isinstance(response, dict) and response["type"] == "image":
        st.session_state.history.append(("bot", "[image]"))
        st.image(response["path"], caption="Generated Image")
    elif isinstance(response, dict) and response["type"] == "map":
        st.session_state.history.append(("bot", f"[Map]({response['url']})"))
        st.markdown(f"[🗺️ View Map]({response['url']})", unsafe_allow_html=True)
    else:
        st.session_state.history.append(("bot", str(response)))

# Display chat history
for sender, message in st.session_state.history:
    with st.chat_message(sender):
        st.markdown(message)
