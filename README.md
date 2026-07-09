# Upgrading the AI Multiverse: Streamlit Chatbot

An advanced, conversational chat interface powered by Google's **Gemini 2.5 Flash** model. It features a custom multiverse persona, real-time response streaming, and stateful multi-turn conversation memory.

## 🚀 Features
- **Multiverse Persona Tuning:** Hardcoded custom system instructions via standard `types.GenerateContentConfig`.
- **Streaming Response Integration:** Real-time token delivery utilizing Streamlit's native `st.write_stream`.
- **Session State Persistence:** Remembers conversation context flawlessly across app refreshes.

