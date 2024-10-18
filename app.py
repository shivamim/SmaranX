import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables (if needed)
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with SmaranX!",
    page_icon="🤖",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Access Google API Key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# CSS for styling with background image
st.markdown(
    """
    <style>
    body {
        background-image: url('https://drive.google.com/uc?id=1vt_1p0QZk3AyrKZtGXeKIn8NINwovsvH');  /* Background image */
        background-size: contain;  /* Adjust size to contain */
        background-position: center;  /* Center the background image */
        background-repeat: no-repeat;  /* Do not repeat the background image */
        height: 100vh;  /* Full viewport height */
        width: 100vw;  /* Full viewport width */
        overflow: hidden;  /* Prevent scrolling */
        font-family: 'Arial', sans-serif;  /* Font style */
        color: #333;  /* Text color */
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
        backdrop-filter: blur(5px);  /* Optional: Adds a blur effect behind the chat container */
    }
    .chat-message {
        border-radius: 15px;
        padding: 10px;
        margin: 5px 0;
        max-width: 60%;
        transition: background-color 0.3s;
    }
    .user {
        background-color: #0084ff;  /* Blue for user messages */
        color: white;
        align-self: flex-end;
    }
    .assistant {
        background-color: #e0e0e0;  /* Light grey for assistant messages */
        color: black;
        align-self: flex-start;
    }
    .stTitle {
        text-align: center;
        font-size: 32px;
        margin: 20px 0;
        color: #0084ff;  /* Blue color for title */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# JavaScript for added interactivity
st.markdown(
    """
    <script>
    // Function to scroll to the bottom of the chat
    function scrollToBottom() {
        const chatContainer = document.querySelector('.chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Scroll to bottom after a message is sent
    window.addEventListener('load', function() {
        scrollToBottom();
    });
    </script>
    """,
    unsafe_allow_html=True
)

# Chat container to allow scrolling
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display the chatbot's title on the page
st.title("🤖 SmaranX - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask SmaranX...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Check if the user asked "Who are you?"
    if "who are you" in user_prompt.lower():
        response = "Hello, I am SmaranX."
    else:
        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        response = gemini_response.text

    # Display the response
    with st.chat_message("assistant"):
        st.markdown(response)

# Close the chat container
st.markdown('</div>', unsafe_allow_html=True)
