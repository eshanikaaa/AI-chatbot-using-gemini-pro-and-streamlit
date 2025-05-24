import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini 2.0 Flash!", # Updated page title
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
# --- CHANGE IS HERE ---
# Changed to 'gemini-2.5-flash' for the Gemini 2.5 Flash model
# You might also use a specific preview version like 'gemini-2.5-flash-preview-05-20'
# if you need to pin to a particular release.
model = gen_ai.GenerativeModel('gemini-2.0-flash')
# --------------------


# Function to translate roles between Gemini and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("🤖 Gemini 2.5 Flash - ChatBot") # Updated chatbot title

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini 2.0 Flash...") # Updated prompt
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini 2.5 Flash and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini 2.5 Flash's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
