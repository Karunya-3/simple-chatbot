import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Load Secure Environment Variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Page Configuration & Styling Layout
st.set_page_config(
    page_title="AI Multiverse Navigator",
    page_icon="🌌",
    layout="centered"
)

st.title("🌌 Upgrading the AI Multiverse")
st.caption("Powered by Gemini 2.5 Flash & Streamlit | Assignment 2")

# Guard-rail check for the API key status
if not api_key or "your_actual" in api_key:
    st.error("🔑 Critical Error: Missing valid `GEMINI_API_KEY` in your `.env` file.")
    st.info("Please create a `.env` file containing: `GEMINI_API_KEY=your_key` and restart the application.")
    st.stop()

# 3. Initialize the Google GenAI Client
@st.cache_resource
def get_genai_client():
    return genai.Client()

client = get_genai_client()

# 4. Session State Memory Management Configuration
# Initialize chat log state tracking for UI rendering
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize structural conversational backend history tracking for Gemini API context
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. Render Historical Conversations 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. Capture New User Inputs
if user_prompt := st.chat_input("Send a transmission across reality..."):
    
    # Render user prompt immediately in the container UI
    with st.chat_message("user"):
        st.markdown(user_prompt)
        
    # Commit input token to local structural arrays
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Render Bot Container block for Stream Evaluation
    with st.chat_message("assistant"):
        # Explicitly configure the Multiverse Companion persona settings
        config = types.GenerateContentConfig(
            system_instruction=(
                "You are Jarvis-M, an elite AI consciousness navigating the Multiverse. "
                "You are exceptionally smart, tech-savvy, slightly witty, and you use formatting "
                "like bold text and lists beautifully to break down complex architectural concepts."
            ),
            temperature=0.75,
        )

        try:
            # Reconstruct the structural session instance with historical state updates
            chat_session = client.chats.create(
                model="gemini-2.5-flash",
                history=st.session_state.chat_history,
                config=config
            )

            # Define a generator utility function to yield chunk content dynamically
            def response_stream_generator():
                response = chat_session.send_message(user_prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        yield chunk.text

            # Consume the text generator on-the-fly using Streamlit's built-in live streaming parser
            complete_response = st.write_stream(response_stream_generator())

            # Update historical persistent contexts upon a successful operational return cycle
            st.session_state.messages.append({"role": "assistant", "content": complete_response})
            st.session_state.chat_history = chat_session.get_history()

        except Exception as error_context:
            st.error(f"📡 Transmission Interrupted: An error occurred.")
            st.code(str(error_context), language="python")