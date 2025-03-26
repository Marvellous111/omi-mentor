import timeit
def get_transcript_on_time(transcript: dict, time_constant: int) -> bool:
  '''Get the transcript on time
  '''
  start_time = timeit.default_timer()
  while int(timeit.default_timer()) - int(start_time) < time_constant:
    if transcript:
      return True
  return False