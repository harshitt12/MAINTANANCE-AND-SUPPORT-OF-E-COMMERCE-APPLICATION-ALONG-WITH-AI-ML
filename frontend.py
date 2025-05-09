import streamlit as st
import app  # Import your backend file

# Streamlit Page Configuration
st.set_page_config(page_title="Chatbot", layout="wide")

# Styling improvements
st.markdown(
    """
    <style>
        .user-message {
            background-color: #A7FFEB;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            max-width: 70%;
            color: black;
            font-weight: bold;
        }
        .bot-message {
            background-color: #E0E0E0;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            max-width: 70%;
            color: black;
            font-weight: bold;
        }
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 10px;
            border-radius: 10px;
            background-color: #1E1E1E;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [("Bot", "Hello! How can I assist you today?")]

st.title("🤖 Chatbot")
st.markdown("Ask me anything about products!")

# Chat history display
st.container()
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for sender, message in st.session_state.messages:
        css_class = "user-message" if sender == "User" else "bot-message"
        st.markdown(f'<div class="{css_class}"><b>{sender}:</b> {message}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# User input field
user_input = st.text_input("Type your message...", key="user_input")

# Submit button
if st.button("Send"):
    if user_input.strip():
        # Store user message
        st.session_state.messages.append(("User", user_input))
        
        # Fetch response from backend (app.py)
        response = app.chat_with_bot(user_input)  # Call backend function
        
        # Store bot response immediately
        st.session_state.messages.append(("Bot", response))
        
        # Clear input field (Fixes delayed response issue)
        st.rerun()

