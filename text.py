import speech_recognition as sr
from groq import Groq
from langchain_groq import ChatGroq
import sys
import logging
from typing import Optional, Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure system encoding
sys.stdout.reconfigure(encoding='utf-8')

class VoiceAssistant:
    def __init__(self, api_key: str):
        """Initialize the voice assistant with necessary components."""
        self.api_key = api_key
        self.recognizer = sr.Recognizer()
        self.conversation_history: List[Dict[str, str]] = []
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=self.api_key,
            model_name="llama-3.1-70b-versatile"
        )

        # Configure speech recognizer
        self.recognizer.energy_threshold = 4000
        self.recognizer.pause_threshold = 0.8
        self.recognizer.dynamic_energy_threshold = True

    def record_speech(self) -> Optional[str]:
        """
        Record and transcribe speech to text.
        Returns:
            str: Transcribed text or None if failed
        """
        try:
            with sr.Microphone() as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                logger.info("Listening...")
                audio = self.recognizer.listen(source, 
                                             timeout=10,
                                             phrase_time_limit=10)
                
                logger.info("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Recognized text: {text}")
                return text

        except sr.RequestError as e:
            logger.error(f"API Error: {str(e)}")
            return None
        except sr.UnknownValueError:
            logger.error("Speech was not understood")
            return None
        except Exception as e:
            logger.error(f"Error during speech recognition: {str(e)}")
            return None

    def generate_response(self, text: str) -> Optional[str]:
        """
        Generate response using Groq API.
        Args:
            text (str): Input text to generate response for
        Returns:
            str: Generated response or None if failed
        """
        try:
            # Add user message to conversation history
            user_message = {"role": "user", "content": text}
            self.conversation_history.append(user_message)

            # Generate response
            response = self.llm.invoke(self.conversation_history)

            # Add system response to conversation history
            system_message = {"role": "system", "content": str(response)}
            self.conversation_history.append(system_message)

            return str(response.content)

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return None

    def run(self):
        """Main loop for the voice assistant."""
        logger.info("Starting voice assistant...")
        
        while True:
            try:
                # Record speech
                text = self.record_speech()
                if not text:
                    logger.warning("No speech detected. Try again.")
                    continue

                print(f"\nYou said: {text}")

                # Generate response
                response = self.generate_response(text)
                if not response:
                    logger.warning("Failed to generate response. Try again.")
                    continue

                print(f"AI Response: {response}\n")

            except KeyboardInterrupt:
                logger.info("Shutting down voice assistant...")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                continue

def main():
    # Your Groq API key
    API_KEY = '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'
    
    try:
        assistant = VoiceAssistant(API_KEY)
        assistant.run()
    except Exception as e:
        logger.error(f"Failed to initialize voice assistant: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()