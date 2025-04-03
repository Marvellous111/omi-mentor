## Imported inbuilt python modules
#import time
import os # Dunno if necessary

## Imported python packages
from data.constants import *
from data.context import *

from utils.Buffer import MessageBuffer


def create_context(target_transcript: dict, target_context_list: list) -> list:
  '''Append a target context list with a target transcript dict with the same session_id
  '''
  session_id = target_transcript["session_id"]
  for segment in target_transcript:
    session_id = segment["session_id"]
    speaker = segment["speaker"]
    text = segment["text"]
    transcript_dict = {
      "session_id": session_id,
      "speaker": speaker,
      "text": text
    }
  target_context_list.append(transcript_dict)
  return target_context_list

def clean_context(target_context_list: list) -> list:
  '''Remove the context in a target context list that is not needed
  NOTE: This feature means that the first session_id captured will be the session_id we will run with.
  '''
  for conversation_contexts in range(0, len(target_context_list)):
    if target_context_list[conversation_contexts]["session_id"] != conversation_contexts[0]["session_id"]:
      target_context_list.remove(target_context_list[conversation_contexts])
  return target_context_list

class Conversations:
  """Conversation class to save conversations for the AI as context without outrightly using a db
  It works by continously storing the trasncripts inside a list and checking the server requests
  If a delay is noticed passed the silence time then it simply saves the data it has gotten
  It then uses the data as context for a message for the AI.
  
  Perhaps it should also feature an interruption method? to get the context of an argument and interrupt where necessary
  """
  def __init__(self):
    self.conversations = conversations_list
    self.silence_time = END_OF_CONVERSATION_IN_SECONDS
    self.conversation = ""
    
    
  def save_conversations(self, conversations_text: str):
    """Add conversations to the conversations list for context

    Args:
        conversations_text (str): This is the transcript text for the conversation gotten from omi
    """
    self.conversations.append(conversations_text)
    
    
    
# [##### ##### ##### #### #### ##### ##### #####] ...
# 1 - 4 6 - 7 8-9   11-14 19... time of transcript being taken, can be scrapped

# Server has breaks apparently

'''
I can thread the function in main.py so that we can then get control over the time stopping if needed
Since we have the time intervals

We can check if the time intervals between two segments gotten is greater than silence time.
We can stop the appending to the list
'''
    