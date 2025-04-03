#Python builtin modules imports
import os
from pathlib import Path
import json
from typing import Dict

# Python installed packages imports
from dotenv import load_dotenv

#File/Modules imports
from prompt.client import client
from Logcode import *
from prompt.notification import create_notification_prompt

load_dotenv()

def get_advice(notification_prompt: dict):
  """
  Generate a prompt based on the notification prompt template and sends to the user
  """
  logger.info("Creating advice for the user")
  
  try:
    system_prompt = notification_prompt.get('prompt')
    topics = notification_prompt.get('context')['filters']['topics']
    total_prompt = f"{system_prompt}\nUse the {topics} as a good way to know what the user is talking about as well when giving your advice. Don't forget straight to the point advice. NOTHING ELSE."
    response = client.chat.completions.create(
      model = "llama-3.3-70b-versatile",
      messages = [
        {
          "role": "system",
          "content": total_prompt
        },
        {
          "role": "user",
          "content": f"Give me advice please, use the {topics} to know what I am talking about as well"
        }
      ],
      max_tokens=150,
      temperature=0.3
    )
    logger.info("Getting advice from llama using groq")
    response_text = response.choices[0].message.content
    logger.debug(f"Response from groq API: {response_text}")
    logger.info(f"Successfully extracted advice for user.")
    return response_text
  except Exception as e:
    logger.error(f"An error occured when getting advice from groq, error: {str(e)}", exc_info=True)
    return