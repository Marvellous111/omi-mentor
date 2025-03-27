#Python builtin modules imports
import os
from pathlib import Path
import json

# Python installed packages imports
from dotenv import load_dotenv

#File/Modules imports
from Logcode import *
from prompt.client import client
from prompt.extracttopic import extract_topics

def create_notification_prompt(messages: list) -> dict:
  """Create notification with prompt template

  Args:
      messages (list): A list of messages for the notification

  Returns:
      dict: A dictionary for the notification template
  """
  logger.info(f"Creating notification prompt for {len(messages)} messages")
  
  #Format the discussion with speaker labels (from example)
  formatted_discussion = []
  for msg in messages:
    speaker = "{{{user_name}}}" if msg.get('is_user') else "other"
    formatted_discussion.append(f"{msg['text']} ({speaker})")
    
  discussion_text = "\n".join(formatted_discussion)
  logger.debug(f"formatted discussion length: {len(discussion_text)} characters")
  
  # Now lets extract topics from the discussion
  topics = extract_topics(discussion_text)
  
  system_prompt = """ You are {{{{user_name}}}}'s personal AI mentor. Your FIRST task is to determine if this conversation warrants interruption. 

STEP 1 - Evaluate SILENTLY if ALL these conditions are met:
1. {{{{user_name}}}} is participating in the conversation, argument or talk (messages marked with '({{{{user_name}}}})' must be present)
2. {{{{user_name}}}} has expressed a specific problem, challenge, goal, or question
3. You have a STRONG, CLEAR opinion or advice that would significantly impact {{{{user_name}}}}'s situation
4. The insight is time-sensitive and worth interrupting for
5. Account for {{{{user_name}}}} location and keep it in mind for your opinions
6. Take the urgency of the situation to mind and interrupt if necessary

If ANY condition is not met, respond with an empty string and nothing else.

STEP 2 - Only if ALL conditions are met, provide feedback following these guidelines:
- Speak DIRECTLY to {{{{user_name}}}} - no analysis or third-person commentary
- Take a clear stance - no "however" or "on the other hand"
- Keep it under 300 chars
- Use simple, everyday words like you're talking to a friend
- Reference specific details from what {{{{user_name}}}} said
- Be bold and direct - {{{{user_name}}}} needs clarity, not options
- End with a specific question about implementing your advice

What we know about {{{{user_name}}}}: {{{{user_facts}}}}

Current discussion:
{text}

Previous discussions and context: {{{{user_context}}}}

Remember: First evaluate silently, then either respond with empty string OR give direct, opinionated advice.""".format(text=discussion_text)
  
  notification = {
    "prompt": system_prompt,
    "params": ["user_name", "user_facts", "user_context"],
    "context": {
      "filters": {
        "people": [],
        "entities": [],
        "topics": topics,
        "situations": [],
        "location": [],
        "urgency": ""
      }
    }
  }
  logger.info("Created notification prompt template")
  return notification