from pydantic import BaseModel
from fastapi import FastAPI, Request, Body
from typing import List, Optional

from Logcode import *


class Segment(BaseModel):
  text: str
  speaker: str
  speaker_id: int
  is_user: bool
  person_id: Optional[int]
  start: float
  end: float
  
class RequestModel(BaseModel):
  session_id: str
  segments: List[Segment]