#Python builtin modules imports
from Logcode import *
import os
from pathlib import Path
import json

# Python installed packages imports
from dotenv import load_dotenv

#File/Modules imports
from client import client

load_dotenv()

def extract_topics(discussion_text: str) -> list:
  """Extract topics from the discussion using grok"""
  logger.info("Starting topic extraction")
  logger.debug(f"Discussion text length: {len(discussion_text)} characters")
  try:
    logger.debug("Sending request to groq(qwen-qwq-32b) API")
    response = client.chat.completions.create(
      model = "qwen-qwq-32b",
      messages=[
        {
          "role": "system",
          "content": "You are a topic extraction specialist. Extract all RELEVANT topics from the conversation. Return ONLY a JSON array of topic strings, NOTHING ELSE. Example format: [\"topic1\", \"topic2\"]"
        },
        {
          "role": "user",
          "content": f"Extract all the RELEVANT topics from this conversation: \n{discussion_text}"
        }
      ],
      max_tokens=150,
      temperature=0.3,
      response_format={ "type": "json_object" }
    )
    #Lets parse the response text as JSON
    response_text = response.choices[0].message.content #We may not need to strip if the response type is json
    topics = json.loads(response_text)
    logger.info(f"Successfully extracted {len(topics)} topics: {topics}")
  except json.JSONDecodeError as e:
    logger.error(f"Failed to parse OpenAI response as JSON: {str(e)}", exc_info=True)
    return []
  except Exception as e:
    logger.error(f"Error extracting topics: {str(e)}", exc_info=True)
    return []