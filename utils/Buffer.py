#Python builtin package import
from Logcode import *
import threading
from collections import defaultdict
import time

#File/Module import
from data.constants import *

# As gotten from example this class is for outlining methods for buffering transcripts
# or messages gotten from the user (from example)
class MessageBuffer:
  def __init__(self):
    logger.info("Initializing MessageBuffer")
    self.buffers = {}
    self.lock = threading.Lock()
    self.cleanup_interval = 300  # 5 minutes
    self.last_cleanup = time.time()
    self.silence_threshold = 120  # 2 minutes silence threshold
    self.min_words_after_silence = 5  # minimum words needed after silence
    self.last_notification_times = defaultdict(dict)  # Track last notification time per message per session
    self.last_reminder_times = defaultdict(dict)  # Track last reminder time per message per session
    logger.debug(f"MessageBuffer initialized with cleanup_interval={self.cleanup_interval}, silence_threshold={self.silence_threshold}")
    
  def get_buffer(self, session_id):
    logger.debug(f"Getting buffer for session_id: {session_id}")
    current_time = time.time()
        
    # Cleanup old sessions periodically
    if current_time - self.last_cleanup > self.cleanup_interval:
      logger.info("Triggering cleanup of old sessions")
      self.cleanup_old_sessions()
        
    with self.lock:
      if session_id not in self.buffers:
        logger.info(f"Creating new buffer for session_id: {session_id}")
        self.buffers[session_id] = {
          'messages': [],
          'last_analysis_time': time.time(),
          'last_activity': current_time,
          'words_after_silence': 0,
          'silence_detected': False
        }
      else:
        # Check for silence period
        time_since_activity = current_time - self.buffers[session_id]['last_activity']
        if time_since_activity > self.silence_threshold:
          logger.info(f"Silence period detected for session {session_id}. Time since activity: {time_since_activity:.2f}s")
          self.buffers[session_id]['silence_detected'] = True
          self.buffers[session_id]['words_after_silence'] = 0
          self.buffers[session_id]['messages'] = []  # Clear old messages after silence
                
          self.buffers[session_id]['last_activity'] = current_time
                
    return self.buffers[session_id]
  def cleanup_old_sessions(self):
    logger.info("Starting cleanup of old sessions")
    current_time = time.time()
    with self.lock:
      initial_count = len(self.buffers)
      expired_sessions = [
        session_id for session_id, data in self.buffers.items()
        if current_time - data['last_activity'] > 3600  # Remove sessions older than 1 hour
      ]
      for session_id in expired_sessions:
        logger.info(f"Removing expired session: {session_id}")
        del self.buffers[session_id]
        if session_id in self.last_notification_times:
          del self.last_notification_times[session_id]
        if session_id in self.last_reminder_times:
          del self.last_reminder_times[session_id]
      final_count = len(self.buffers)
      current_time = time.time() # We have to do this current time here so we can get accurate clean up time
      self.last_cleanup = current_time
      logger.info(f"Cleanup complete. Removed {len(expired_sessions)} sessions. Active sessions: {final_count}, Previous total sessions: {initial_count}")
  
  def set_last_notification_time(self, session_id: str, message_id: str):
    with self.lock:
      self.last_notification_times[session_id][message_id] = time.time()
  
  def get_sessions_needing_reminder(self):
    current_time = time.time()
    messages_to_remind = []
    with self.lock:
      logger.info(f"Checking reminders. Active notification sessions: {list(self.last_notification_times.keys())}")
      sessions_to_remove = []
      messages_to_remove = []
      
      for session_id, message_dict in self.last_notification_times.items():
        for message_id, last_time in message_dict.items():
          last_reminder = self.last_reminder_times.get(session_id, {}).get(message_id, 0)
          time_since_notification = current_time - last_time
          time_since_reminder = current_time - last_reminder
          
          logger.info(f"Session {session_id}, Message {message_id}:")
          logger.info(f"  - Time since last notification: {time_since_notification:.1f}s (threshold: {REMINDER_INTERVAL_IN_SECONDS}s)")
          logger.info(f"  - Time since last reminder: {time_since_reminder:.1f}s (threshold: {REMINDER_INTERVAL_IN_SECONDS}s)")
          
          if time_since_notification >= REMINDER_INTERVAL_IN_SECONDS and last_reminder == 0:  # Only if no reminder sent yet
            logger.info(f"  -> Adding message {message_id} from session {session_id} to reminder list")
            messages_to_remind.append((session_id, message_id))
            self.last_reminder_times[session_id][message_id] = current_time
            if session_id not in sessions_to_remove:
              sessions_to_remove.append(session_id)
              messages_to_remove.append((session_id, message_id))
          else:
            logger.info("  -> Not yet time for reminder or reminder already sent")
      
      # Remove messages that have been reminded
      for session_id, message_id in messages_to_remove:
        logger.info(f"Removing message {message_id} from notification tracking after scheduling reminder")
        if message_id in self.last_notification_times[session_id]:
          del self.last_notification_times[session_id][message_id]
        # Clean up empty session entries
        if not self.last_notification_times[session_id]:
          del self.last_notfiication_times[session_id]
      # Though it may make log cluttered but it is important
      logger.info(f"Final messages to remind: {messages_to_remind}")
      
    return messages_to_remind
