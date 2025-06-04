from .model import ChatbotModel
import os

class Chatbot:
    """Main chatbot class to handle user interactions."""
    
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GROQ_API_KEY")
            print(f"Loaded API Key: {api_key}")  # Debug print, remove later
        if not api_key:
            raise ValueError("API key for Groq LLM is not set!")
        self.model = ChatbotModel(api_key)

    def ask(self, question):
        """Ask a question to the chatbot model."""
        return self.model.ask_chatbot(question)

    