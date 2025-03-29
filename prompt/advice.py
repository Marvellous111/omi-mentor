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
  system_prompt = notification_prompt.get('prompt')
  params = notification_prompt.get('params')
  