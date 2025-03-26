from Logcode import *
from dotenv import load_dotenv
import os
from groq import Groq

# We would like to initiate our AI client here (Groq[for speed], Grok[because we think its better])
# NOTE: OpenAI is too expensive for the tradeoff


load_dotenv()

API_KEY_GROQ = os.getenv('API_KEY_GROQ_TEST')

try:
  client = Groq(
    api_key = API_KEY_GROQ
  )
  if not API_KEY_GROQ:
    logger.error("No API key found for Groq in the environment variable")
    raise ValueError("Groq API key is required")
  logger.info("Groq client initialized successfully")
except Exception as e:
  logger.critical(f"Failed to initialize groq client: {str(e)}", exc_info=True)
  raise