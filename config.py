# config.py
import os 
import pvporcupine

# --- Audio Stream Configuration ---
SAMPLE_RATE = 16000
CHANNELS = 1
DEVICE_ID = None
DTYPE = 'int16'

# --- Wake Word Engine (Porcupine) ---
# Get your free key from: https://console.picovoice.ai/
PICOVOICE_ACCESS_KEY = r'yiQmmK5TzMwWrPgkPh4A+CJN2MsxCm2Vz5UzvXNok1vLS/coKoBiXQ=='

# For now, we'll use a built-in keyword.
# To create your own "Genesis" keyword, visit the Picovoice Console.
WAKE_WORD_MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'genesis_wake_word.ppn')
KEYWORD_PATHS = [r"C:\Users\parth\OneDrive\Documents\Genesis\models\it--s-me_en_windows_v3_0_0.ppn"]
WAKE_WORD_NAME = "it's me"



#-------ollama / Planner configuration ----------------#
OLLAMA_API_BASE_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL_NAME = "gemma:2b" # Or "gemma:7b" 

CONVERSATION_SYSTEM_PROMPT = """You are Genesis, a friendly and helpful AI assistant.
Your goal is to have a natural, engaging conversation with the user.
Respond directly to the user's question or statement in a clear and concise way.

User: {user_command}
Genesis:
"""
