from Logcode import *
import os
from pathlib import Path
import json
import requests
import time

from dotenv import load_dotenv

from utils.Buffer import MessageBuffer
from data.constants import APP_ID, REMINDER_MESSAGE, REMINDER_CHECK_INTERVAL_IN_SECONDS

load_dotenv()

logger.info("Starting Mentor notification service")

def send_reminder_notification(session_id, message_id):
  """Send a reminder notification to the main app"""
  logger.info(f"Attempting to send reminder for session {session_id}, message {message_id}")
  
  api_base_url = os.getenv('API_BASE_URL') # Don't exactly know what the base_url here is.
  # Will check docs for any base url, if none then there is no need since omi notifications are returns for fastAPI as shown in video
  # Hence the code will be edited
  API_KEY = os.getenv('API_KEY_NOTIFICATION')
  
  if not api_base_url:
    logger.error("API_BASE_URL enviroment variable not set")
    return
  
  notification_url = f"{api_base_url.rstrip('/')}/v2/integrations/{APP_ID}/notification"
  
  try:
    # We want to use bearer token authentication
    headers = {
      'Authorization': f'Bearer {API_KEY}'
    }
    
    params = {
      "uid": session_id,
      "message": REMINDER_MESSAGE
    }
    
    logger.info(f"Sending reminder notification to {notification_url} for session {session_id}, message {message_id} with aid {APP_ID}")
    response = requests.post(notification_url, headers=headers, params=params)
    if response.status_code == 200:
      logger.info(f"Successfully sent reminder notification for session {session_id}, message {message_id}")
    else:
      logger.error(f"Failed to send reminder notification. Status code: {response.status_code}, Response: {response.text}")
  except Exception as e:
    logger.error(f"Error sending reminder notification: {str(e)}", exc_info=True)
    
def reminder_check_loop(message_buffer: MessageBuffer): #This will be here so we can easily call it in the main.py file without having circular imports
  """Background task to check and send reminders"""
  while True:
    try:
      logger.info("Checking for messages needing reminders...")
      messages = message_buffer.get_sessions_needing_reminder()
      if messages:
        logger.info(f"Found {len(messages)} messages needing reminders: {messages}")
        for session_id, message_id in messages:
          send_reminder_notification(session_id, message_id)
      else:
        logger.debug("No messages need reminders at this time") # Very important logger here
    except Exception as e:
      logger.error(f"Error in reminder check loop: {str(e)}", exc_info=True)
    
    logger.debug(f"Sleeping for {REMINDER_CHECK_INTERVAL_IN_SECONDS} seconds before next reminder check")
    time.sleep(REMINDER_CHECK_INTERVAL_IN_SECONDS)