from pydantic import BaseModel
from fastapi import FastAPI, Request, Body

from Logcode import *


class Segments(BaseModel):
  text: str
  speaker: str
  speaker_id: str
  is_user: bool
  person_id: int | None = None
  start: float
  end: float