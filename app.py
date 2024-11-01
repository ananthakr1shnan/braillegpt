import streamlit as st
import os
from dotenv import load_dotenv
import logging
from Speech import record_text
from groq_api import generate_answer

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s"
)


class VoiceSearchApp:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv("API_KEY")

        # Validate API key
        if not self.api_key:
            st.error("❌ API Key not found. Please set up your .env file.")

    def run(self):
        """Main Streamlit application"""
        # Page configuration
        st.set_page_config(
            page_title="Voice Search AI",
            page_icon="🎤",
            initial_sidebar_state="collapsed",
        )

        # Custom CSS
        st.markdown(
            """
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 15px 25px;
            border-radius: 8px;
            width: 100%;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        # App header
        st.title("🎤 Voice Search AI")
        st.markdown("### Speak your question and get AI-powered answers")

        # Voice input section
        col1, col2 = st.columns([4, 1])

        with col1:
            if st.button("🎤 Start Speaking", key="voice_input"):
                try:
                    # Record speech
                    st.info("🎧 Listening... Please speak your question clearly")
                    user_text = record_text()

                    if user_text != "Could not understand the audio.":
                        # Show recognized text
                        st.success(f"Recognized Text: {user_text}")

                        # Get AI response
                        try:
                            response = generate_answer(user_text)

                            # Store in session state
                            if "conversation" not in st.session_state:
                                st.session_state.conversation = []

                            st.session_state.conversation.append(
                                {"question": user_text, "answer": response}
                            )

                        except Exception as api_error:
                            st.error(f"Error generating response: {api_error}")
                            logging.error(f"API Error: {api_error}")
                    else:
                        st.warning("⚠️ Could not understand. Please try again.")

                except Exception as voice_error:
                    st.error(f"Voice Recognition Error: {voice_error}")
                    logging.error(f"Voice Error: {voice_error}")

        with col2:
            if st.button("🗑️ Clear", key="clear_history"):
                st.session_state.conversation = []
                st.rerun()

        # Display conversation history
        if "conversation" in st.session_state and st.session_state.conversation:
            st.header("Conversation History")
            for item in st.session_state.conversation:
                with st.container():
                    st.markdown(f"**🗣️ Question:** {item['question']}")
                    st.markdown(f"**💡 Answer:** {item['answer']}")
                    st.divider()
        else:
            st.info("Speak your question to start the conversation!")


def main():
    app = VoiceSearchApp()
    app.run()


if __name__ == "__main__":
    main()
