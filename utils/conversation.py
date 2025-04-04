## Imported inbuilt python modules
import asyncio
import time
from typing import Optional
import threading

## Imported python packages
from Logcode import *
from data.constants import *
from data.context import *
from prompt.client import client
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

class Conversations:
  """Conversation class to save conversations for the AI as context without outrightly using a db
  It works by continously storing the trasncripts inside a list and checking the server requests
  If a delay is noticed passed the silence time then it simply saves the data it has gotten
  It then uses the data as context for a message for the AI.
  
  Perhaps it should also feature an interruption method? to get the context of an argument and interrupt where necessary
  """
  def __init__(self, silence_threshold=END_OF_CONVERSATION_IN_SECONDS):
    self.last_request_time = time.time()
    self.conversations = conversations_list
    self.silence_time = silence_threshold
    self.conversation = ""
    self.notification_sent = False
    self.lock = threading.Lock() # For thread-safe updates
    self.current_time = time.time()
    self.running = False # Thread flag for control
    self.time_thread = None
    
  def start_time_thread(self):
    """Start time thread in the background
    """
    if not self.running:
      self.running = True
      self.time_thread = threading.Thread(target=self.update_time, daemon=True)
      self.time_thread.start()
      logger.info("Time thread started")
  
  def stop_time_thread(self):
    """Stoping the time thread running in the background
    """
    if self.running:
      self.running = False
      if self.time_thread:
        self.time_thread.join() #This waits for the thread to finish from the main thread
      logger.info("Time thread stopped")
  
  def update_time(self):
    """Background thread logic to update the current time every second
    """
    while self.running:
      with self.lock:
        self.current_time = time.time()
      time.sleep(1.0)
        
    
    
  def update(self, transcript_segment: str):
    logger.info(f"Updating the conversation for better context")
    self.conversations.append(transcript_segment)
    self.last_request_time = time.time()
    self.notification_sent = False
    return self.conversations
    
  def should_interrupt(self) -> bool:
    logger.info(f"Starting interrupt function")
    try:
      logger.debug(f"Sending request to groq API")
      system_prompt = """
You are a conversation specialist. 
Your job is to look at the conversation the user gives and check if it needs an interruption.
Have an added focus on whether the conversation sounds like an argument. (Arguments should be priority so most of the time you should interrupt an argument)
If the conversation is deemed necessary to be interrupted then ONLY respond with the word: INTERRUPT
If the conversation is not deemed necessary to be interrupted then simply respond with the word: NOINTERRUPT

Example of situations that could require interruption:
- When the user is getting a fact wrong, it warrants interruption to correct the user
- When the user is in an argument or a heated argument, IT ABSOLUTELY WARRANTS INTERRUPTION. It is important to understand what the argument is about, why it is ocurring and how it can be resolved. DO NOT PICK A SIDE UNLESS ABSOLUTELY SURE OF WHO IS AT FAULT
- When a conversation by the user seems like it needs urgent help it warrants interruption.

You are:
- A mentor where needed.
- A friend where needed.
- A confidant where needed.

Using the three situational guidelines above you can guess other possible situations that require interruption and others that don't require interruption.
This is the conversation for you to go through to make your assessment: {transcript_segment}
Your OUTPUT text should either be INTERRUPT or NOINTERRUPT
IT MUST BE IN CAPS""".format(transcript_segment=self.conversation)

      response = client.chat.completions.create(
        model = AI_MODEL,
        messages = [
          {
            "role": "system",
            "content": system_prompt
          },
          {
            "role": "user",
            "content": f"Please tell me if it's necessary to interrupt this discussion or not: {self.conversation}"
          }
        ],
        max_tokens=150,
        temperature=0.3
      )
      logger.info("Getting interruption status from conversation")
      response_text = response.choices[0].message.content
      logger.debug(f"Response from groq API: {response_text}")
      logger.info(f"Successfully gotten interruption status.")
      if response_text == "INTERRUPT":
        return True
      elif response_text == "NOINTERRUPT":
        return False
      else:
        logger.error("INCORRECT OUTPUT GOTTEN")
        return False
    except Exception as e:
      logger.error(f"An error occured: {str(e)}", exc_info=True)
      return False
    
    
  async def check_silence(self):
    logger.info("Checking for silence in the conversation")
    while True:
      logger.info("Silence checking loop")
      async with self.lock:
        current_time = time.time()
        time_since_last_transcript = current_time - self.last_request_time
        if time_since_last_transcript >= self.silence_threshold and self.notification_sent == False:
          logging.info("Silence detected - Conversation ended. Sending notification")
          self.notification = True
          return True
        elif time_since_last_transcript < self.silence_threshold and not self.notification_sent:
          ## We could log here but we dont want spam every second
          logger.info("Silence not detected - Conversation ongoing")
          return False
        elif time_since_last_transcript >= self.silence_threshold and not self.notification_sent:
          logging.info("Silence detected - Conversation ended. Sending notification again")
          self.notification_sent = False
          return True
      await asyncio.sleep(1.0)
      
  def join_conversation(self, conversation_list: list) -> str:
    """Function to join the conversation list into a single string
    """
    convo = ""
    for conversation in conversation_list:
      convo += conversation + " "
    
    self.conversation = convo.strip()
    return self.conversation