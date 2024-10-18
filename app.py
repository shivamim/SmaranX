import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables from .env file for local development (optional)
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with SmaranX!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Access Google API Key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# CSS for styling
st.markdown("""
    <style>
    body {
        background-image: url('https://drive.google.com/file/d/1vt_1p0QZk3AyrKZtGXeKIn8NINwovsvH/view?usp=sharing');  /* Replace with your image URL */
        background-size: cover;
        background-repeat: no-repeat;
        color: white;  /* Text color */
        font-family: 'Arial', sans-serif;
    }
    .chat-container {
        padding: 20px;
        border-radius: 10px;
        background-color: rgba(0, 0, 0, 0.7);  /* Semi-transparent background */
    }
    h1 {
        text-align: center;
        margin-bottom: 20px;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }
    .st-chat-message {
        margin-bottom: 10px;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Display the chatbot's title on the page
st.title("🤖 SmaranX - ChatBot")

# Chat container for messages
with st.container():
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask SmaranX...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
