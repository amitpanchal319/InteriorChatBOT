from dotenv import load_dotenv
import os

from groq import Groq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from chatbot.prompt import CUSTOM_PROMPT

# Load environment variables from .env file
load_dotenv()

class ChatbotModel:
    """Chatbot model class to manage the LLM and interactions."""

    def __init__(self, api_key=None):
        # Use passed api_key or fallback to environment variable
        if api_key is None:
            api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("API key for Groq LLM is not set!")

        # Initialize memory for conversation history
        self.memory = ConversationBufferMemory(
            input_key="question",
            memory_key="history",
            chat_memory=ChatMessageHistory()
        )

        # Initialize Groq LLM with correct keyword argument
        self.llm = ChatGroq(
            groq_api_key=api_key,  # ✅ Corrected from 'api_key'
            model="llama3-8b-8192",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        # Setup prompt template
        self.prompt = PromptTemplate(
            template=CUSTOM_PROMPT,
            input_variables=["context", "history", "question"]
        )

        # Create the chain: prompt -> llm -> output parser
        self.chain = self.prompt | self.llm | StrOutputParser()

    def ask_chatbot(self, question):
        """Process user input and return chatbot response."""
        inputs = {
            "context": "",  # Replace with real context if needed
            "history": self.memory.load_memory_variables({}).get("history", ""),
            "question": question
        }

        response = self.chain.invoke(inputs)

        # Save interaction to memory
        self.memory.save_context(
            {"question": question},
            {"answer": response}
        )

        return response
