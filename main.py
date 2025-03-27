#Framework imports
from fastapi import FastAPI, Request
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

#Python packages imports
from pprint import pprint
import logging
import os
from pathlib import Path
import requests
import time
from datetime import datetime
import threading

#File/Module imports
from prompt.notification import *
from Logcode import *
from data.constants import *
from utils.notifications import *
from utils.Buffer import MessageBuffer
from utils.cleanconversation import create_context, clean_context
from utils.gettime import get_transcript_on_time
from data.context import context_list, transcript_segment, unclean_context_list

app = FastAPI()

origins = [
  "http://localhost:8000",
  "http://localhost"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"], #origins
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)


'''
NOTE: We are relying on the example given to us with a lot of tweaks since it is a good entry point.
Further work on this app will slowly move away from the example to a more concrete work.
comments tagged with (from example) are gotten from example
comments tagged with (not example) are novel (Some novel comments aren't tagged too)
comments tagged with (perhaps example) are edited example code
'''


# logger.info("Starting Mentor notification service")


message_buffer = MessageBuffer()
logger.info(f"Analysis interval set to {END_OF_CONVERSATION_IN_SECONDS} seconds")

'''IMPORTANT NOTE: The thread below hijacks the main thread and stops the app from running. This is not ideal and should be fixed.
FIX: A simple fix would be to ensure it runs in the background AFTER the app has started.
A condition could be after a segment is gotten from the transcript, then the thread starts.
This way, the app can run and the thread can run in the background.
At the moment though we can remove the notifications for now.
'''
# # This starts the reminder check loop in the background, message_buffer MUST be initialized first though
# reminder_thread = threading.Thread(target=reminder_check_loop(message_buffer), daemon=True)
# reminder_thread.start()


@app.post("/webhook")
def webhook():
  logger.info("Recieved webhook POST request")
  if Request.method == 'POST':
    try:
      data = Request.json
      session_id = data.get('session_id')
      segments = data.get('segments', [])
      message_id = data.get('message_id')
      
      print(segments)
      
      # message_id should be generated if it isnt provided
      if not message_id:
        message_id = f"{session_id}_{int(time.time())}"
        logger.info(f"Generated message_id: {message_id}")
      
      logger.info(f"Processing webhook for session_id: {session_id}, message_id: {message_id}, segments count: {len(segments)}, aid: {APP_ID}")
      
      if not session_id:
        logger.error("No session_id provided in request")
        return {"message": "No session_id provided"}
      
      current_time = time.time()
      buffer_data = message_buffer.get_buffer(session_id)
      
      #Process new messages
      logger.info(f"Processing {len(segments)} segments for session {session_id}")
      for segment in segments:
        if not segment.get('text'):
          logger.debug("skipping empty segment")
          continue
        
        text = segment['text'].strip()
        if text:
          timestamp = segment.get('start', 0) or current_time
          is_user = segment.get('is_user', False)
          logger.info(f"Processing segment - is_user: {is_user}, timestamp: {timestamp}, text: {text[:50]}...")
          
          #Count words after silence
          if buffer_data['silence_detected']:
            words_in_segment = len(text.split())
            buffer_data['words_after_silence'] += words_in_segment
            logger.info(f"Words after silence: {buffer_data['words_after_silence']}/{message_buffer.min_words_after_silence} needed")
            
            #If we have enough words, start fresh conversation
            if buffer_data['words_after_silence'] >= message_buffer.min_words_after_silence:
              logger.info(f"Silence period ended for session {session_id}, starting fresh conversation")
              buffer_data['silence_detected'] = False
              buffer_data['last_analysis_time'] = current_time  # Reset analysis timer
              
          can_append = (
            buffer_data['messages'] and 
            abs(buffer_data['messages'][-1]['timestamp'] - timestamp) < 2.0 and
            buffer_data['messages'][-1].get('is_user') == is_user
          )
          
          if can_append:
            logger.info(f"Appending to existing message. Current length: {len(buffer_data['messages'][-1]['text'])}")
            buffer_data['messages'][-1]['text'] += ' ' + text
          else:
            logger.info(f"Creating new message. Buffer now has {len(buffer_data['messages']) + 1} messages")
            buffer_data['messages'].append({
              'text': text,
              'timestamp': timestamp,
              'is_user': is_user
            })
            
      # Check if it's time to analyze
      time_since_last_analysis = current_time - buffer_data['last_analysis_time']
      logger.info(f"Time since last analysis: {time_since_last_analysis:.2f}s (threshold: {END_OF_CONVERSATION_IN_SECONDS}s)")
      logger.info(f"Current message count: {len(buffer_data['messages'])}")
      logger.info(f"Silence detected: {buffer_data['silence_detected']}")
      
      if ((time_since_last_analysis >= END_OF_CONVERSATION_IN_SECONDS or buffer_data['last_analysis_time'] == 0) and
        buffer_data['messages'] and 
        not buffer_data['silence_detected'] and
        message_id):  # Only proceed if we have a message_id
                
        logger.info("Starting analysis of messages")
        # Sort messages by timestamp
        sorted_messages = sorted(buffer_data['messages'], key=lambda x: x['timestamp'])
                
        # Create notification with formatted discussion
        notification = create_notification_prompt(sorted_messages)
                
        buffer_data['last_analysis_time'] = current_time
        buffer_data['messages'] = []  # Clear buffer after analysis

        # Track notification time for reminders with message_id
        message_buffer.set_last_notification_time(session_id, message_id)

        logger.info(f"Sending notification with prompt template for session {session_id}, message {message_id}")
        return notification
      
      logger.debug("No analysis needed at this time")
      return {}
    except Exception as e:
      logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
      return {"error": "Internal server error"}              
    
  return {"message": f"Transcript: {segments}"}

@app.get('/webhook/setup-status')
def setup_status():
  logger.debug("Received setup-status GET request")
  return {"is_setup_completed": True}

@app.get('/status')
def status():
  logger.debug("Received status GET request")
  active_sessions = len(message_buffer.buffers)
  uptime = time.time() - start_time
  logger.info(f"Status check - Active sessions: {active_sessions}, Uptime: {uptime:.2f}s")
  return {
    "active_sessions": active_sessions,
    "uptime": uptime
  }

# Add start time tracking
start_time = time.time()
logger.info(f"Application initialized. Start time: {datetime.fromtimestamp(start_time)}")

if __name__ == '__main__':
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8000)