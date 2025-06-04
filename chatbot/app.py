import os
import traceback
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from logger import CustomLogger
from chatbot import Chatbot
from dotenv import load_dotenv

load_dotenv()  # Load .env file

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    logger = CustomLogger().get_logger()

    @app.route('/', methods=['GET', 'POST'])
    def index():
        error_message = None

        if request.method == 'POST':
            # Instead of manually entering API key, we'll use .env variable
            # But if you want to allow manual input, you can keep this logic and override env
            api_key = request.form.get('api_key') or os.getenv('GROQ_API_KEY')
            try:
                session['groq_api_key'] = api_key
                chatbot_instance = Chatbot(api_key)
                logger.info("API Key set successfully.")
                return redirect(url_for('chat'))
            except Exception as e:
                logger.error(f"Error setting API Key: {e}")
                logger.error(traceback.format_exc())
                error_message = "Error setting API Key. Please try again."

        return render_template('index.html', error_message=error_message)

    @app.route('/chat')
    def chat():
        if 'groq_api_key' not in session:
            # If no session key, use env variable as fallback
            if os.getenv('GROQ_API_KEY'):
                session['groq_api_key'] = os.getenv('GROQ_API_KEY')
            else:
                return redirect(url_for('index'))
        return render_template('chat.html')

    @app.route('/ask', methods=['POST'])
    def ask():
        question = request.json.get('question')

        try:
            api_key = session.get('groq_api_key') or os.getenv('GROQ_API_KEY')
            if not api_key:
                return jsonify({"response": "API Key is not set."}), 500

            chatbot_instance = Chatbot(api_key)
            response = chatbot_instance.ask(question)
            logger.info(f"User asked: {question}")
            return jsonify({"response": response})

        except Exception as e:
            logger.error(f"Error processing question '{question}': {e}")
            logger.error(traceback.format_exc())
            return jsonify({"response": "An error occurred while processing your request."}), 500

    @app.route('/logout', methods=['POST'])
    def logout():
        session.pop('groq_api_key', None)
        session.pop('chatbot_instance', None)
        logger.info("API Key and Chatbot instance cleared.")
        return redirect(url_for('index'))

    return app
