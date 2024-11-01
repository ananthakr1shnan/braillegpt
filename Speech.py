import speech_recognition as sr


def record_text():
    """
    Record speech and convert to text for search functionality.
    Returns:
        str: Recognized text or error message
    """
    # Initialize recognizer
    recognizer = sr.Recognizer()

    try:
        # Use default microphone
        with sr.Microphone() as source:
            # Configure recognition settings
            recognizer.energy_threshold = 4000  # Increased for better voice detection
            recognizer.pause_threshold = 0.8  # Shorter pause for search queries

            print("Adjusting for background noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            print("Processing speech...")
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            return text

    except sr.RequestError:
        return "Could not understand the audio."
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except Exception as e:
        print(f"Error: {e}")
        return "Could not understand the audio."
