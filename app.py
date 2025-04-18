import streamlit as st
from main import results

st.set_page_config(page_title="TaskMind AI Assistant", layout="wide")
st.title("🤖 TaskMind AI Assistant")

# Initialize history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Input area
user_input = st.text_input("You:", key="input")

# Containers for current response and chat history
current_response_container = st.container()
chat_history_container = st.container()

# Process input
if user_input:
    st.session_state.history.append(("user", user_input))
    response = results("Broddy", user_input)

    with current_response_container:
        st.markdown("**You:**")
        st.markdown(user_input)

        st.markdown("**TaskMind:**")
        if isinstance(response, dict) and response["type"] == "text":
            st.markdown(response["content"])
            st.session_state.history.append(("bot", response["content"]))
        elif isinstance(response, dict) and response["type"] == "image":
            st.markdown("[image]")
            st.image(response["path"], caption="Generated Image")
            st.session_state.history.append(("bot", "[image]"))
        elif isinstance(response, dict) and response["type"] == "map":
            st.markdown(f"[🗺️ View Map]({response['url']})", unsafe_allow_html=True)
            st.session_state.history.append(("bot", f"[Map]({response['url']})"))
        else:
            st.markdown(str(response))
            st.session_state.history.append(("bot", str(response)))

# Divider and scrollable history
st.markdown("---")
st.markdown("### 💬 Chat History")

# Scrollable area
with chat_history_container:
    st.markdown(
        """
        <div style="height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
        """,
        unsafe_allow_html=True
    )
    for sender, message in st.session_state.history:
        bubble_color = "#f1f1f1" if sender == "user" else "#e0f7fa"
        st.markdown(
            f"""
            <div style="background-color: {bubble_color}; padding: 10px; margin-bottom: 10px; border-radius: 10px;">
                <strong>{sender.capitalize()}:</strong><br>{message}
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
