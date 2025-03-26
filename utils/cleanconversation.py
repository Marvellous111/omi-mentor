def append_segment_to_transcript():
  pass

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