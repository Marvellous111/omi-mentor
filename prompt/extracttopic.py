#Python builtin modules imports
import os
from pathlib import Path
import json

# Python installed packages imports
from dotenv import load_dotenv

#File/Modules imports
from prompt.client import client
from Logcode import *

load_dotenv()

def extract_topics(discussion_text: str) -> list:
  """Extract topics from the discussion using groq"""
  logger.info("Starting topic extraction")
  logger.debug(f"Discussion text length: {len(discussion_text)} characters")
  try:
    logger.debug("Sending request to groq(llama-3.1-8b-instant) API")
    response = client.chat.completions.create(
      model = "qwen-2.5-32b", ## Ensure you stay away from models that think
      messages=[
        {
          "role": "system",
          "content": "You are a topic extraction specialist. Extract all RELEVANT topics from the conversation. Return ONLY a JSON array of topic strings, NOTHING ELSE, NO NEED TO TYPE ANYTHING ELSE BESIDES WHAT TO BE RETURNED. Example format: [\"topic1\", \"topic2\"]"
        },
        {
          "role": "user",
          "content": f"Extract all the RELEVANT topics from this conversation: \n{discussion_text}"
        }
      ],
      max_tokens=150,
      temperature=0.3
    )
    #Lets parse the response text as JSON
    response_text = response.choices[0].message.content.strip() #We may not need to strip if the response type is json
    logger.debug(f"Response from groq API: {response_text}")
    print(response_text)
    topics = json.loads(response_text)
    logger.info(f"Successfully extracted {len(topics)} topics: {topics}")
    return topics
  except json.JSONDecodeError as e:
    logger.error(f"Failed to parse Groq response as JSON: {str(e)}", exc_info=True)
    return []
  except Exception as e:
    logger.error(f"Error extracting topics: {str(e)}", exc_info=True)
    return []